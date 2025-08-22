from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('completed', 'Завершено'),
        ('failed', 'Неудачно'),
        ('refunded', 'Возвращено'),
    ]

    PAYMENT_METHODS = [
        ('card', 'Банковская карта'),
        ('cash', 'Наличные'),
        ('bank_transfer', 'Банковский перевод'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='card')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name} - {self.amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            # Генерируем простой ID транзакции
            import uuid
            self.transaction_id = f"txn_{uuid.uuid4().hex[:10]}"
        super().save(*args, kwargs)

    def simulate_payment_processing(self):
        """Автоматическая симуляция обработки платежа"""
        from .services import MockPaymentGateway
        gateway = MockPaymentGateway()
        return gateway.process_payment(self)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']