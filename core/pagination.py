from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'first': self.get_first_link(),
                    'last': self.get_last_link(),
                },
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
            },
            'results': data
        })

    def get_first_link(self):
        """Ссылка на первую страницу"""
        if self.page.number == 1 or not self.page.paginator.num_pages:
            return None
        return self.build_absolute_uri('?page=1')

    def get_last_link(self):
        """Ссылка на последнюю страницу"""
        if self.page.number == self.page.paginator.num_pages or not self.page.paginator.num_pages:
            return None
        return self.build_absolute_uri(f'?page={self.page.paginator.num_pages}')

    def paginate_queryset(self, queryset, request, view=None):
        """Обработка неверных номеров страниц"""
        try:
            return super().paginate_queryset(queryset, request, view)
        except Exception as e:
            raise NotFound("Неверный номер страницы или размера страницы")