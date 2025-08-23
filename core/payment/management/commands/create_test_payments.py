from django.core.management.base import BaseCommand
from payment.models import Payment
from user.models import User
from course.models import Course
import random


class Command(BaseCommand):
    help = 'Создает тестовые платежи для демонстрации'

    def handle(self, *args, **options):
        # Берем первых 5 пользователей и 3 курса
        users = User.objects.all()[:5]
        courses = Course.objects.all()[:3]
        if not users or not courses:
            self.stdout.write(self.style.WARNING('Нет пользователей или курсов для создания платежей'))
            return

        statuses = ['pending', 'completed', 'failed', 'refunded']

        self.stdout.write('Создание тестовых платежей...')

        for i, user in enumerate(users):
            for j, course in enumerate(courses):
                payment = Payment.objects.create(
                    user=user,
                    course=course,
                    amount=random.randint(500, 5000),
                    payment_method=random.choice(['card', 'cash', 'bank_transfer']),
                    status=random.choice(statuses)
                )
                self.stdout.write(
                    f'Создан платеж {i * len(courses) + j + 1}: '
                    f'{user.username} - {course.title} - {payment.amount} KGS'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {len(users) * len(courses)} тестовых платежей!'
            )
        )