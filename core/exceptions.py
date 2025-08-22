from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Стандартная обработка
    response = exception_handler(exc, context)

    if response is not None:
        # Кастомизируем ответ
        custom_response = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': 'Произошла ошибка',
                'details': response.data
            }
        }
        response.data = custom_response

    return response