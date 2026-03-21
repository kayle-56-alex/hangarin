import os
import django
import random
from django.utils import timezone
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin.settings')
django.setup()

from tasks.models import Task, Category, Priority, Note, SubTask

fake = Faker()

def populate(n=10):
    # Ensure we have categories and priorities to link to
    categories = list(Category.objects.all())
    priorities = list(Priority.objects.all())

    if not categories or not priorities:
        print("Error: Please add Categories and Priorities in Admin first!")
        return

    print(f"Starting to populate {n} tasks...")

    for _ in range(n):
        # 1. Generate Task (Requirements: sentence for title, paragraph for description)
        title = fake.sentence(nb_words=5) # [cite: 96, 99]
        description = fake.paragraph(nb_sentences=3) # 
        
        # Requirement: timezone.make_aware() for deadlines
        deadline = timezone.make_aware(fake.date_time_this_month()) # [cite: 42-44]
        
        # Requirement: random_element for status
        status = fake.random_element(elements=["Pending", "In Progress", "Completed"]) # 

        task = Task.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            status=status,
            category=random.choice(categories),
            priority=random.choice(priorities)
        )

        # 2. Generate Notes for this task (Requirement: populate Note model)
        for _ in range(random.randint(1, 3)):
            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2)
            )

        # 3. Generate SubTasks (Requirement: populate SubTask model)
        for _ in range(random.randint(2, 5)):
            SubTask.objects.create(
                parent_task=task,
                title=fake.sentence(nb_words=4),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
            )

    print("Population complete! Check your dashboard.")

if __name__ == '__main__':
    populate(15) # Change this number to add more or fewer tasks
