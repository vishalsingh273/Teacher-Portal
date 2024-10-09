from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('teacher_home/', views.teacher_home, name='teacher_home'),
    path('update_student/',views.update_student, name='update_student'),
    path('add_student/', views.add_student, name='add_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),

]
