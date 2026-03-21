from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Task, Category, Priority, SubTask, Note

def get_sidebar_context(title, content):
    return {
        'title': title, 
        'content': content,
        'tasks': Task.objects.all().order_by('-id'),
        'categories': Category.objects.all(),
        'priorities': Priority.objects.all(),
        'pending_count': Task.objects.filter(status='Pending').count(),
    }

def home(request):
    query = request.GET.get('q')
    # Pre-loading everything for the progress bars and notes
    tasks_query = Task.objects.prefetch_related('subtasks', 'notes').order_by('-id')
    
    if query:
        tasks = tasks_query.filter(
            Q(title__icontains(query)) | Q(category__name__icontains(query))
        ).distinct()
    else:
        tasks = tasks_query

    context = {
        'tasks': tasks,
        'categories': Category.objects.all(),
        'priorities': Priority.objects.all(),
        'pending_count': Task.objects.filter(status='Pending').count(),
        'query': query,
    }
    return render(request, 'home.html', context)

def toggle_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    subtask.status = "Pending" if subtask.status == "Completed" else "Completed"
    subtask.save()
    return redirect('home')

def add_task(request):
    if request.method == "POST":
        category_obj = Category.objects.get(id=request.POST.get('category'))
        priority_obj = Priority.objects.get(id=request.POST.get('priority'))
        Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=category_obj,
            priority=priority_obj,
            deadline=request.POST.get('deadline'),
            status='Pending'
        )
        return redirect('home')
    return render(request, 'page_template.html', get_sidebar_context('Add Task', 'Create new.'))

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.title = request.POST.get('title')
        task.status = request.POST.get('status')
        task.save()
        return redirect('home')
    context = get_sidebar_context('Edit Task', 'Update details.')
    context['task'] = task
    return render(request, 'page_template.html', context)

def delete_task(request, task_id):
    get_object_or_404(Task, id=task_id).delete()
    return redirect('home')

def tables(request):
    return render(request, 'page_template.html', get_sidebar_context('Tables', 'View records.'))

def notifications(request):
    context = get_sidebar_context('Notifications', 'Pending items.')
    context['tasks'] = Task.objects.filter(status='Pending')
    return render(request, 'page_template.html', context)