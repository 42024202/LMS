from __future__ import annotations
from django.db import models
from course.models.course import Course
from course.course_choises import StudentStatus
from user.models import MyUser


class CourseStudent(models.Model):
    course = models.ForeignKey(
            Course,
            on_delete=models.CASCADE,
            related_name='students',
            verbose_name='Курс'
            )

    user = models.ForeignKey(
            MyUser,
            on_delete=models.CASCADE,
            related_name='courses',
            verbose_name='Студент'
            )
    
    status = models.CharField(
            choices=StudentStatus,
            default=StudentStatus.ACTIVE,
            max_length=50,
            verbose_name='Статус'
            )

    enrolled_at = models.DateTimeField(
            auto_now_add=True,
            verbose_name='Дата записи'
            )

    completed_at = models.DateTimeField(
            verbose_name='Дата окончания'
            )

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'
    
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

        constraints = [
            models.UniqueConstraint(
                fields=["course", "user"],
                name="uniq_course_user"
            )
        ]

