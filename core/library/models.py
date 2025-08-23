from django.db import models


class Book(models.Model):
    # Основные поля для учебника
    title = models.CharField(
        max_length=255,
        verbose_name="Название учебника",
        help_text="Полное название учебного пособия"
    )
    author = models.CharField(
        max_length=255,
        verbose_name="Автор",
        help_text="Автор или редактор учебника"
    )

    # Учебные характеристики
    subject = models.CharField(
        max_length=100,
        verbose_name="Предмет/Дисциплина",
        help_text="Учебная дисциплина, к которой относится учебник"
    )
    education_level = models.CharField(
        max_length=50,
        choices=[
            ('school', 'Школьный'),
            ('college', 'Колледж'),
            ('bachelor', 'Бакалавриат'),
            ('master', 'Магистратура'),
        ],
        default='bachelor',
        verbose_name="Уровень образования",
        help_text="Для какого уровня обучения предназначен учебник"
    )

    # Практические поля для LMS
    isbn = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="ISBN",
        help_text="Международный стандартный номер книги"
    )
    file = models.FileField(
        upload_to='books/',
        blank=True,
        null=True,
        verbose_name="Файл учебника",
        help_text="Электронная версия учебника"
    )
    external_link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Внешняя ссылка",
        help_text="Ссылка на онлайн-ресурс или магазин"
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name="Обязательная литература",
        help_text="Обязателен ли учебник для изучения"
    )

    def __str__(self):
        return f"{self.title} ({self.subject})"

    class Meta:
        verbose_name = "Учебник"
        verbose_name_plural = "Учебники"
        ordering = ["subject", "title"]


class CourseBook(models.Model):
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="course_books",
        verbose_name="Курс",
        help_text="Курс, для которого предназначен учебник"
    )
    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        related_name="course_books",
        verbose_name="Учебник",
        help_text="Учебник, связанный с курсом"
    )

    # Учебные параметры
    reading_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок изучения",
        help_text="Порядковый номер для последовательности изучения"
    )
    recommended_chapters = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Рекомендуемые разделы",
        help_text="Главы или разделы, обязательные для изучения"
    )
    study_hours = models.PositiveIntegerField(
        default=0,
        verbose_name="Часы на изучение",
        help_text="Рекомендуемое количество часов для изучения"
    )

    class Meta:
        unique_together = ("course", "book")
        verbose_name = "Учебник курса"
        verbose_name_plural = "Учебники курсов"
        ordering = ["course", "reading_order"]

    def __str__(self):
        return f"{self.course.name} - {self.book.title}"