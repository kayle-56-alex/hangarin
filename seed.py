import random
from django.utils import timezone
from faker import Faker
from tasks.models import Task, Category, Priority, Note, SubTask

fake = Faker()

def run():
    # Fetch the categories and priorities you manually added
    categories = list(Category.objects.all())
    priorities = list(Priority.objects.all())

    if not categories or not priorities:
        print("Error: Please add Categories and Priorities in the Admin panel first!")
        return

    # Generate 10 Tasks
    for _ in range(10):
        task = Task.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            deadline=timezone.make_aware(fake.date_time_this_month()),
            status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
            category=random.choice(categories),
            priority=random.choice(priorities)
        )

        # Generate a Note for each task
        Note.objects.create(
            task=task,
            content=fake.paragraph(nb_sentences=2)
        )

        # Generate 2 SubTasks for each task
        for _ in range(2):
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )

    print("Successfully seeded 10 tasks with notes and subtasks!")