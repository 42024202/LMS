from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    year_of_publication = models.PositiveIntegerField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.author}"


class CourseBook(models.Model):
    course = models.ForeignKey("course.Course", on_delete=models.CASCADE, related_name="course_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="course_books")

    class Meta:
        unique_together = ("course", "book")

    def __str__(self):
        return f"{self.course.name} - {self.book.title}"
