from django.contrib import admin
from django.urls import path, include
from tasks import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home, name='home'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle-subtask/<int:subtask_id>/', views.toggle_subtask, name='toggle_subtask'),
    path('tables/', views.tables, name='tables'),
    path('notifications/', views.notifications, name='notifications'),
    path('', include('pwa.urls')),
]