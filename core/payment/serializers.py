from rest_framework import serializers
from .models import Payment
from user.models import User
from course.models import Course


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

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
            'amount', 'payment_method', 'status', 'transaction_id',
            'created_at', 'confirmed_at'
        ]
        read_only_fields = ['id', 'status', 'transaction_id', 'created_at', 'confirmed_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма платежа должна быть положительной")
        return value