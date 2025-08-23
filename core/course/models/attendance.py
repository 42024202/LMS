from __future__ import annotations
from django.db import models
from .shedule_session import SheduleSession
from course.course_choises import AttendanceStatus
from course.models.course_student import CourseStudent


class Attendance(models.Model):
    shedule_session = models.ForeignKey(
            SheduleSession,
            on_delete=models.CASCADE,
            related_name='attendances',
            verbose_name='Занятие'
            )

    student = models.ForeignKey(
            CourseStudent,
            on_delete=models.CASCADE,
            related_name="attendances",
            verbose_name="Студент курса"
            )

    status = models.CharField(
            choices=AttendanceStatus.choices,
            verbose_name='Статус'
            )

    comment = models.TextField(
            verbose_name='Комментарий'
            )

    def __str__(self):
        return f"{self.student.student.fisrtname} {self.shedule_session}"

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

        constraints = [
            models.UniqueConstraint(
                fields=["student", "shedule_session"],
                name="uniq_attendance"
            )
        ]

