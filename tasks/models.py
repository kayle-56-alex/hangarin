from django.db import models

# Requirement: Inherit BaseModel with created_at and updated_at [cite: 65]
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Requirement: Grammar refactor for Categories [cite: 85-92]
class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name # [cite: 93-94]

# Requirement: Grammar refactor for Priorities [cite: 85-87]
class Priority(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name

class Task(BaseModel):
    # Requirement: Status field choices [cite: 71-76]
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="Pending" # [cite: 77]
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tasks")
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title

    # NEW: Progress Calculation Logic
    def get_progress(self):
        total = self.subtasks.count()
        if total == 0:
            return 100 if self.status == "Completed" else 0
        completed = self.subtasks.filter(status="Completed").count()
        return int((completed / total) * 100)

class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notes")
    content = models.TextField()

    def __str__(self):
        return f"Note for {self.task.title}"

class SubTask(BaseModel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=50, 
        choices=Task.STATUS_CHOICES, # [cite: 67]
        default="Pending"
    )

    def __str__(self):
        return self.title