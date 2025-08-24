from django.contrib import admin
from .models import Book, CourseBook

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "subject", "education_level", "is_required")
    list_filter = ("subject", "education_level", "is_required")
    search_fields = ("title", "author", "subject", "isbn")
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "author", "subject", "education_level")
        }),
        ("Дополнительная информация", {
            "fields": ("isbn", "file", "external_link", "is_required")
        }))
     

@admin.register(CourseBook)
class CourseBookAdmin(admin.ModelAdmin):
    list_display = ("course", "book", "reading_order", "study_hours")
    list_filter = ("course", "book__subject")
    search_fields = ("course__name", "book__title")
    raw_id_fields = ("course", "book")  # Для удобства выбора при большом количестве
