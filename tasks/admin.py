from django.contrib import admin
from .models import Category, Priority, Task, Note, SubTask

# Requirement: CategoryAdmin & PriorityAdmin [cite: 55]
# Display just the name field and make them searchable [cite: 57]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',) # [cite: 57]
    search_fields = ('name',) # [cite: 57]

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',) # [cite: 57]
    search_fields = ('name',) # [cite: 57]

# Requirement: TaskAdmin [cite: 46]
# Display title, status, deadline, priority, category [cite: 47]
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'priority', 'category') # [cite: 47]
    list_filter = ('status', 'priority', 'category') # 
    search_fields = ('title', 'description') # 

# Requirement: SubTaskAdmin [cite: 50]
# Display title, status, and a custom field parent_task_name 
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'parent_task_name') # [cite: 51]
    list_filter = ('status',) # [cite: 53]
    search_fields = ('title',) # [cite: 54]

    # Custom field to display the parent task's name [cite: 52]
    def parent_task_name(self, obj):
        return obj.parent_task.title
    parent_task_name.short_description = 'Parent Task'

# Requirement: NoteAdmin [cite: 58]
# Display task, content, and created_at [cite: 59]
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('task', 'content', 'created_at') # [cite: 59]
    list_filter = ('created_at',) # [cite: 60]
    search_fields = ('content',) # [cite: 61]