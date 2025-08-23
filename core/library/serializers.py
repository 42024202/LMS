from rest_framework import serializers
from .models import Book, CourseBook
from course.models import Course


class BookSerializer(serializers.ModelSerializer):
    # Вычисляемое поле для отображения
    education_level_display = serializers.CharField(
        source='get_education_level_display',
        read_only=True
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'subject', 'education_level',
            'education_level_display', 'isbn', 'file', 'external_link',
            'is_required'
        ]
        read_only_fields = ['id']

    def validate_title(self, value):
        """Валидация названия учебника"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название слишком короткое")
        return value.strip()

    def validate_subject(self, value):
        """Валидация названия предмета"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название предмета слишком короткое")
        return value.strip()


class CourseBookSerializer(serializers.ModelSerializer):
    # Для чтения - полные данные учебника
    book = BookSerializer(read_only=True)

    # Для чтения - название курса
    course_name = serializers.CharField(
        source='course.name',
        read_only=True
    )

    # Для записи - только ID курса
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True,
        source='course'
    )

    class Meta:
        model = CourseBook
        fields = [
            'id', 'course_id', 'course_name', 'book',
            'reading_order', 'recommended_chapters', 'study_hours'
        ]
        read_only_fields = ['id']

    def validate_reading_order(self, value):
        """Валидация порядка изучения"""
        if value < 0:
            raise serializers.ValidationError("Порядок изучения не может быть отрицательным")
        return value

    def validate_study_hours(self, value):
        """Валидация часов на изучение"""
        if value < 0:
            raise serializers.ValidationError("Часы на изучение не могут быть отрицательными")
        if value > 1000:
            raise serializers.ValidationError("Слишком много часов на изучение")
        return value

    def validate(self, data):
        """Общая валидация"""
        # Проверяем, что учебник соответствует уровню курса
        course = data.get('course')
        book = self.instance.book if self.instance else None

        if course and book:
            # Здесь можно добавить логику проверки соответствия
            # Например: if course.level != book.education_level:
            pass

        return data