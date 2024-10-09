from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Student
import json
from django.views.decorators.csrf import csrf_exempt

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('teacher_home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def teacher_home(request):
    students = Student.objects.all()
    return render(request, 'teacher_home.html', {'students': students})


@csrf_exempt  # Only use this for development/testing; better to handle CSRF tokens properly in production
def update_student(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            student_id = data.get('id')
            field = data.get('field')
            value = data.get('value')

            # Find the student
            student = Student.objects.get(id=student_id)

            # Update the field based on the field name
            if field == 'name':
                student.name = value
            elif field == 'subject':
                student.subject = value
            elif field == 'marks':
                student.marks = value
            
            student.save()  # Save the updated student
            return JsonResponse({'success': True})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            student = get_object_or_404(Student, id=student_id)
            student.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            subject = data.get('subject')
            marks = data.get('marks')

            # Ensure name, subject, and marks are present
            if not name or not subject or marks is None:
                return JsonResponse({'error': 'Name, Subject, and Marks are required'}, status=400)

            # Try to find the existing student
            student, created = Student.objects.get_or_create(name=name, subject=subject)

            if not created:
                # If student exists, update their marks
                student.marks += int(marks)
            else:
                # If it's a new student, set the marks
                student.marks = int(marks)
            
            student.save()
            return JsonResponse({'success': True})

        except ValueError:
            return JsonResponse({'error': 'Invalid input'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)