from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tasks import views 

urlpatterns = [
    path('', views.home, name='home'), 
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    
    # NEW: Toggle route for the Checklist
    path('toggle-subtask/<int:subtask_id>/', views.toggle_subtask, name='toggle_subtask'),
    
    path('tables/', views.tables, name='tables'),
    path('notifications/', views.notifications, name='notifications'),
    path('admin/', admin.site.urls),
]