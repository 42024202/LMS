from django.apps import AppConfig
import logging
import sys

logger = logging.getLogger(__name__)


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    verbose_name = 'Платежная система'

    def ready(self):
        # Не загружать сигналы во время миграций
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv:
            logger.info("Пропуск загрузки сигналов during migrations")
            return

        # Регистрируем сигналы
        try:
            import payment.signals
            logger.info("Сигналы payment успешно загружены")
        except ImportError as e:
            logger.error(f"Ошибка импорта сигналов payment: {e}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке сигналов payment: {e}")