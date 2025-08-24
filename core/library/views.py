from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, CourseBook
from .serializers import BookSerializer, CourseBookSerializer
from .permissions import IsAdminOrReadOnly
from common.pagination import CustomPagination

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'education_level', 'is_required']
    search_fields = ['title', 'author', 'subject']
    ordering_fields = ['title', 'author', 'subject', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        education_level = self.request.query_params.get('education_level')
        if education_level:
            queryset = queryset.filter(education_level=education_level)
        is_required = self.request.query_params.get('is_required')
        if is_required:
            queryset = queryset.filter(is_required=is_required.lower() == 'true')
        return queryset

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

class CourseBookListCreateView(generics.ListCreateAPIView):
    queryset = CourseBook.objects.all()
    serializer_class = CourseBookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'book']  # Убрал is_required
    search_fields = ['book__title', 'book__author', 'course__name', 'recommended_chapters']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # Уточни название поля связи с студентами
            queryset = queryset.filter(course__students=self.request.user)
        return queryset

class CourseBookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseBook.objects.all()
    serializer_class = CourseBookSerializer
    permission_classes = [permissions.IsAdminUser]
