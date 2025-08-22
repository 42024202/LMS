import time
import random
from django.utils import timezone


class MockPaymentGateway:
    """Простая симуляция платежного шлюза для тестирования"""

    def process_payment(self, payment):
        """Симулируем обработку платежа"""
        print(f"🔄 Обрабатываем платеж {payment.id} на сумму {payment.amount}...")

        # Имитируем задержку обработки (2-5 секунд)
        processing_time = random.uniform(2.0, 5.0)
        time.sleep(processing_time)

        # 80% шанс успешного платежа, 20% - неудачного
        if random.random() < 0.8:
            payment.status = 'completed'
            payment.confirmed_at = timezone.now()
            payment.save()
            print(f"✅ Платеж {payment.id} успешно завершен!")
            return True
        else:
            payment.status = 'failed'
            payment.save()
            print(f"❌ Платеж {payment.id} не прошел!")
            return False

    def get_payment_status(self, payment):
        """Возвращает текущий статус платежа"""
        status_messages = {
            'pending': 'Ожидает обработки',
            'completed': 'Успешно завершен',
            'failed': 'Не удался',
            'refunded': 'Возвращен'
        }
        return status_messages.get(payment.status, 'Неизвестный статус')