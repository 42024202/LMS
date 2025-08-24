from django.db import models
from user.models import MyUser

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

    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Курс"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='card',
        verbose_name="Метод оплаты"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name="ID транзакции"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )
    confirmed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Подтвержден"
    )

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.amount}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            import uuid
            self.transaction_id = f"txn_{uuid.uuid4().hex[:10]}"
        super().save(*args, **kwargs)

    def simulate_payment_processing(self):
        from .services import MockPaymentGateway
        gateway = MockPaymentGateway()
        return gateway.process_payment(self)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']

class PaymentStatusHistory(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="status_history",
        verbose_name="Платеж"
    )
    old_status = models.CharField(
        max_length=20,
        verbose_name="Предыдущий статус"
    )
    new_status = models.CharField(
        max_length=20,
        verbose_name="Новый статус"
    )
    changed_by = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="changed_statuses",
        verbose_name="Кем изменен"
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Когда изменен"
    )

    def __str__(self):
        return f"{self.payment} - {self.old_status} → {self.new_status}"

    class Meta:
        verbose_name = 'История статуса платежа'
        verbose_name_plural = 'Истории статусов платежей'
        ordering = ['-changed_at']

