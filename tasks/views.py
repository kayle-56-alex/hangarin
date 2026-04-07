from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField, Q
from .models import Task, SubTask, Category, Priority

# Reusable Priority Hierarchy Logic 
def get_priority_order():
    return Case(
        When(priority__name__iexact='Critical', then=Value(1)),
        When(priority__name__iexact='High', then=Value(2)),
        When(priority__name__iexact='Medium', then=Value(3)),
        When(priority__name__iexact='Low', then=Value(4)),
        When(priority__name__iexact='Optional', then=Value(5)),
        default=Value(6),
        output_field=IntegerField(),
    )

@login_required
def home(request):
    query = request.GET.get('q')
    priority_order = get_priority_order()
    
    if query:
        # UPDATED SEARCH: Checks Title, Category name, and Priority name [cite: 443]
        tasks = Task.objects.filter(
            Q(title__icontains=query) | 
            Q(category__name__icontains=query) |
            Q(priority__name__icontains=query)
        ).order_by(priority_order, 'deadline').distinct()
    else:
        tasks = Task.objects.all().order_by(priority_order, 'deadline')
        
    pending_count = Task.objects.filter(status='Pending').count()
    return render(request, 'home.html', {
        'tasks': tasks, 
        'query': query, 
        'pending_count': pending_count
    })

@login_required
def add_task(request):
    categories = Category.objects.all()
    if request.method == "POST":
        priority_name = request.POST.get('priority')
        priority_obj = Priority.objects.filter(name__iexact=priority_name).first()

        new_task = Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            priority=priority_obj,
            category_id=request.POST.get('category') or None,
            deadline=request.POST.get('deadline') or None,
            status='Pending'
        )
        
        subtask_titles = request.POST.getlist('subtasks[]')
        for title in subtask_titles:
            if title.strip():
                SubTask.objects.create(task=new_task, title=title, status='Pending')
        return redirect('home')
    return render(request, 'tasks/task_form.html', {'categories': categories})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    categories = Category.objects.all()
    
    if request.method == "POST":
        priority_name = request.POST.get('priority')
        priority_obj = Priority.objects.filter(name__iexact=priority_name).first()

        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = priority_obj
        task.category_id = request.POST.get('category') or None
        task.deadline = request.POST.get('deadline') or None
        task.save()

        subtask_titles = request.POST.getlist('subtasks[]')
        for title in subtask_titles:
            if title.strip():
                SubTask.objects.create(task=task, title=title, status='Pending')
        return redirect('home')
    
    return render(request, 'tasks/task_form.html', {'task': task, 'categories': categories})

@login_required
def notifications(request):
    priority_order = get_priority_order()
    # Filters only Pending tasks sorted by hierarchy
    pending_tasks = Task.objects.filter(status='Pending').order_by(priority_order, 'deadline')
    return render(request, 'notifications.html', {'pending_tasks': pending_tasks})

@login_required
def delete_task(request, task_id):
    get_object_or_404(Task, id=task_id).delete()
    return redirect('home')

@login_required
def toggle_subtask(request, subtask_id):
    sub = get_object_or_404(SubTask, id=subtask_id)
    sub.status = 'Completed' if sub.status == 'Pending' else 'Pending'
    sub.save()
    return redirect('home')

@login_required
def tables(request):
    query = request.GET.get('q')
    priority_order = get_priority_order()
    
    if query:
        # UPDATED SEARCH: Search enabled for Table view as well
        tasks = Task.objects.filter(
            Q(title__icontains=query) | 
            Q(category__name__icontains=query) |
            Q(priority__name__icontains=query)
        ).order_by(priority_order, 'deadline').distinct()
    else:
        tasks = Task.objects.all().order_by(priority_order, 'deadline')
        
    return render(request, 'tasks/task_list.html', {'tasks': tasks})