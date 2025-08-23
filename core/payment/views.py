from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import api_view, permission_classes
from .services import MockPaymentGateway
from django.db.models import Sum


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at', 'amount', 'status']
    ordering = ['-created_at']
    filterset_fields = ['status', 'payment_method', 'user']
    pagination_class = None

    def get_queryset(self):
        queryset = Payment.objects.all() if self.request.user.is_staff \
            else Payment.objects.filter(user=self.request.user)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def perform_create(self, serializer):
        # Автоматически сохраняем текущего пользователя
        serializer.save(user=self.request.user, status='pending')

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_payment(request, pk):
    """Обработка платежа через симуляцию"""
    try:
        payment = Payment.objects.get(pk=pk, user=request.user)

        # Проверяем, что платеж еще не обработан
        if payment.status != 'pending':
            return Response(
                {'error': 'Платеж уже обработан', 'current_status': payment.status},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Симулируем обработку платежа
        gateway = MockPaymentGateway()
        success = gateway.process_payment(payment)

        if success:
            return Response(
                {
                    'status': 'success',
                    'message': 'Платеж успешно обработан',
                    'transaction_id': payment.transaction_id,
                    'amount': payment.amount
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'status': 'error',
                    'message': 'Ошибка обработки платежа',
                    'transaction_id': payment.transaction_id
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    except Payment.DoesNotExist:
        return Response(
            {'error': 'Платеж не найден'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_status(request, pk):
    """Проверка статуса платежа"""
    try:
        payment = Payment.objects.get(pk=pk, user=request.user)
        gateway = MockPaymentGateway()

        return Response({
            'payment_id': payment.id,
            'transaction_id': payment.transaction_id,
            'status': payment.status,
            'status_message': gateway.get_payment_status(payment),
            'amount': payment.amount,
            'course': payment.course.title,
            'created_at': payment.created_at,
            'confirmed_at': payment.confirmed_at
        })

    except Payment.DoesNotExist:
        return Response(
            {'error': 'Платеж не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def payment_stats(request):
    total = Payment.objects.count()
    completed = Payment.objects.filter(status='completed').count()
    revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))

    return Response({
        'total_payments': total,
        'completed_payments': completed,
        'total_revenue': revenue['amount__sum'] or 0
    })


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def refund_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)

        # Проверяем, можно ли сделать возврат
        if payment.status != 'completed':
            return Response(
                {'error': 'Возврат возможен только для завершенных платежей'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = 'refunded'
        payment.save()
        return Response({'status': 'refunded'})

    except Payment.DoesNotExist:
        return Response(
            {'error': 'Платеж не найден'},
            status=status.HTTP_404_NOT_FOUND
        )
