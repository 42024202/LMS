from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Payment, PaymentStatusHistory
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Payment)
def create_payment_history(sender, instance, **kwargs):
    """Создание истории изменений статуса платежа"""
    if not instance.pk:  # Новый объект
        return

    try:
        old_payment = Payment.objects.get(pk=instance.pk)
        if old_payment.status != instance.status:
            PaymentStatusHistory.objects.create(
                payment=instance,
                old_status=old_payment.status,
                new_status=instance.status,
                changed_by=None
            )
            logger.info(f"Status changed for payment {instance.id}: {old_payment.status} → {instance.status}")
    except Payment.DoesNotExist:
        logger.warning(f"Payment {instance.pk} not found for history tracking")


@receiver(post_save, sender=Payment)
def send_payment_email(sender, instance, created, **kwargs):
    """Отправка email при изменении статуса платежа"""

    if created:  # Пропускаем для новых объектов
        return

    subject = None
    message = None

    if instance.status == 'completed':
        subject = 'Платеж успешно завершен'
        message = f'''
        Здравствуйте, {instance.user.username}!

        Ваш платеж на сумму {instance.amount} KGS за курс "{instance.course.title}" 
        успешно завершен.

        Номер транзакции: {instance.transaction_id}
        '''
    elif instance.status == 'failed':
        subject = 'Платеж не прошел'
        message = f'''
        Здравствуйте, {instance.user.username}!

        Ваш платеж на сумму {instance.amount} KGS за курс "{instance.course.title}" 
        не прошел. Пожалуйста, попробуйте еще раз или обратитесь в поддержку.

        Номер транзакции: {instance.transaction_id}
        '''
    elif instance.status == 'refunded':
        subject = 'Возврат средств'
        message = f'''
        Здравствуйте, {instance.user.username}!

        По вашему платежу на сумму {instance.amount} KGS за курс "{instance.course.title}" 
        был выполнен возврат средств.

        Номер транзакции: {instance.transaction_id}
        '''

    if subject and message:
        try:
            send_mail(
                subject,
                message,
                'noreply@lms.com',
                [instance.user.email],
                fail_silently=False,
            )
            logger.info(f"Email sent to {instance.user.email} about payment {instance.id}")
        except Exception as e:
            logger.error(f"Failed to send email for payment {instance.id}: {e}")