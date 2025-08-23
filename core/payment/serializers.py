from rest_framework import serializers
from .models import Payment
from user.models import User
from course.models import Course

class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    amount_with_currency = serializers.SerializerMethodField(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True,
        source='course'
    )

    class Meta:
        model = Payment
        fields = [
            'id', 'user_id', 'user_email', 'course_id', 'course_title',
            'amount', 'amount_with_currency', 'payment_method', 'status',
            'transaction_id', 'created_at', 'confirmed_at'
        ]
        read_only_fields = ['id', 'status', 'transaction_id', 'created_at', 'confirmed_at']

    def get_amount_with_currency(self, obj):
        return f"{obj.amount} KGS"

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма платежа должна быть положительной")
        if value > 1000000:
            raise serializers.ValidationError("Сумма платежа слишком большая")
        return value

    def validate(self, data):
        """Общая валидация данных"""
        if data.get('payment_method') == 'card' and data.get('amount', 0) > 100000:
            raise serializers.ValidationError(
                "Максимальная сумма для оплаты картой: 100 000 KGS"
            )
        return data