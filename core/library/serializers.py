from rest_framework import serializers
from .models import Book, CourseBook
from django.utils import timezone
from course.models import Course


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class CourseBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True
    )

    class Meta:
        model = CourseBook
        fields = ["id", "course", "book", "title", "author", "name", "genre", "year_of_publication", "url"]

    def validate_year_of_publication(self, value):
        if value and value > timezone.now().year:
            raise serializers.ValidationError("Год публикации не может быть в будущем")
        if value and value < 1000:
            raise serializers.ValidationError("Год публикации слишком ранний")
        return value

    def validate_title(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название слишком короткое")
        return value.strip()

    # Общая валидация объекта
    def validate(self, data):
        if data.get('genre') == 'Научная фантастика' and data.get('year_of_publication') < 1900:
            raise serializers.ValidationError("Научная фантастика не могла быть опубликована до 1900 года")
        return data