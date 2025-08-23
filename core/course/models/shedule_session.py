from __future__ import annotations
from django.db import models
from .course import Course 
from .modules import Module 
from .lessons import Lesson 
from course.course_choises import SessionType
from user.models import MyUser


class SheduleSession(models.Model):
    course = models.ForeignKey(
            Course,
            on_delete=models.CASCADE,
            related_name='shedules',
            verbose_name='Курс'
            )

    module = models.ForeignKey(
            Module,
            on_delete=models.CASCADE,
            related_name='shedules',
            verbose_name='Тема курса'
            )

    lesson = models.ForeignKey(
            Lesson,
            on_delete=models.CASCADE,
            related_name='shedules',
            verbose_name='Урок'
            )

    instructor = models.ForeignKey(
            MyUser,
            on_delete=models.CASCADE,
            related_name='shedules',
            verbose_name='Инструктор'
            )

    starts_at = models.DateTimeField(
            verbose_name='Начало урока'
            )

    end_at = models.DateTimeField(
            verbose_name='Конец урока'
            )

    session_type = models.CharField(
            choices=SessionType,
            verbose_name='Тип урока'
            )
    
    def __str__(self):
        return f'{self.course.title} - {self.module.title} - {self.lesson.title}'

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

