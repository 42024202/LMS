from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookListCreateView.as_view(), name="book-list-create"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),

    # Новые URLs для книг по курсу
    path('courses/<int:course_id>/books/', views.CourseBooksListView.as_view(), name='course-books'),
    path('courses/<int:course_id>/books-detailed/', views.CourseBooksDetailedView.as_view(),
         name='course-books-detailed'),
]