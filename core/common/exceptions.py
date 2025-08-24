from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений для DRF
    """
    # Логируем все исключения
    logger.error(f"Exception: {exc}", exc_info=True)
    logger.error(f"Context: {context}")

    try:
        # Стандартная обработка DRF
        response = exception_handler(exc, context)

        if response is not None:
            # Кастомизируем формат ответа
            error_message = get_error_message(response.status_code)

            custom_response = {
                'success': False,
                'error': {
                    'code': response.status_code,
                    'message': error_message,
                    'details': response.data
                }
            }
            response.data = custom_response
        else:
            # Обработка не пойманных DRF исключений
            response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            custom_response = {
                'success': False,
                'error': {
                    'code': 500,
                    'message': 'Внутренняя ошибка сервера',
                    'details': str(exc)
                }
            }
            response.data = custom_response

        return response

    except Exception as e:
        # Аварийный fallback
        logger.critical(f"Critical error in exception handler: {e}")
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'success': False,
                'error': {
                    'code': 500,
                    'message': 'Критическая ошибка сервера',
                    'details': None
                }
            }
        )


def get_error_message(status_code):
    """Возвращает понятное сообщение об ошибке по коду статуса"""
    messages = {
        400: 'Неверные данные запроса',
        401: 'Требуется авторизация',
        403: 'Доступ запрещен',
        404: 'Ресурс не найден',
        405: 'Метод не разрешен',
        409: 'Конфликт данных',
        500: 'Внутренняя ошибка сервера',
    }
    return messages.get(status_code, 'Произошла ошибка')
