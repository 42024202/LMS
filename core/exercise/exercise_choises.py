from django.db import models


class ExerciseStatus(models.TextChoices):
    ACTIVE = 'active','Активен'
    INACTIVE = 'inactive','Неактивен'

class SubmissionsStatus(models.TextChoices):
    SUBMITTED = 'submitted','Отправлено'
    GRADED = 'graded','Оценено'
    NEEDS_REVISION = 'get_revision','Нужно доработать' 
    RESUBMITTED = 'resubmitted','Пересдано'

