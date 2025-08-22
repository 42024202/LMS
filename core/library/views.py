from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Book, CourseBook
from .serializers import BookSerializer, CourseBookSerializer
from .permissions import IsAdminOrReadOnly
from core.pagination import CustomPagination


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'author', 'year_of_publication']
    search_fields = ['title', 'author', 'genre']
    ordering_fields = ['title', 'author', 'year_of_publication', 'created_at']

    def perform_create(self, serializer):
        serializer.save()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]  # Только админы могут изменять/удалять


class CourseBookListCreateView(generics.ListCreateAPIView):
    queryset = CourseBook.objects.all()
    serializer_class = CourseBookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'book']
    search_fields = ['book__title', 'book__author', 'course__name']


class CourseBookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseBook.objects.all()
    serializer_class = CourseBookSerializer
    permission_classes = [permissions.IsAdminUser]  # Только админы