import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin.settings')
django.setup()

from tasks.models import Task, SubTask, Note, Priority, Category
from django.utils import timezone

fake = Faker()

def run():
    priorities = list(Priority.objects.all())
    categories = list(Category.objects.all())

    for _ in range(10):  # create 10 tasks
        task = Task.objects.create(
            title=fake.sentence(),
            description=fake.paragraph(),
            deadline=timezone.make_aware(fake.date_time_this_month()),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
            priority=random.choice(priorities),
            category=random.choice(categories)
        )

        # create subtasks
        for _ in range(3):
            SubTask.objects.create(
                title=fake.sentence(),
                status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
                task=task
            )

        # create notes
        for _ in range(2):
            Note.objects.create(
                task=task,
                content=fake.paragraph()
            )

if __name__ == "__main__":
    run()