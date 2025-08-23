from django.db import models


class StudentStatus(models.TextChoices):
    ACTIVE = "active", "Активный"
    COMPLETED = "completed", "Завершен"
    DROPPED = "dropped", "Отчислен" 


class SessionType(models.TextChoices):
    LECTION = 'lection', 'Лекция'
    SEMINAR = 'seminar', 'Семинар'


class AttendanceStatus(models.TextChoices):
    PRESENT = 'present', 'Присутствует'
    ABSENT = 'absent', 'Отсутствует'

