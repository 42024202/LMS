import random
from django.utils import timezone

class MockPaymentGateway:
    def process_payment(self, payment):
        if random.random() < 0.8:
            payment.status = 'completed'
            payment.confirmed_at = timezone.now()
            payment.save()
            return True
        else:
            payment.status = 'failed'
            payment.save()
            return False

    def get_payment_status(self, payment):
        status_messages = {
            'pending': 'Ожидает обработки',
            'completed': 'Успешно завершен',
            'failed': 'Не удался',
            'refunded': 'Возвращен'
        }
        return status_messages.get(payment.status, 'Неизвестный статус')
