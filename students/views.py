from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentApplication

# Home
def home(request):
    return render(request, 'students/home.html')

# Register
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! You can login now.")
        return redirect('login')

    return render(request, 'students/register.html')

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'students/login.html')

    return render(request, 'students/login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Application Form
@login_required
def application_form(request):
    data = StudentApplication.objects.filter(user=request.user).first()

    courses = [
        'Python',
        'C',
        'C++',
        'Java',
        'Machine Learning',
        'Deep Learning'
    ]

    if request.method == 'POST':
        StudentApplication.objects.update_or_create(
            user=request.user,
            defaults={
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'phone': request.POST.get('phone'),
                'country': request.POST.get('country'),
                'gender': request.POST.get('gender'),
                'course': request.POST.get('course'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
            }
        )
        messages.success(request, "Application submitted successfully!")
        return redirect('dashboard')

    return render(
        request,
        'students/application.html',
        {
            'data': data,
            'courses': courses
        }
    )

# Dashboard
@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Admin sees all students
        students = StudentApplication.objects.select_related('user').all()
        return render(request, 'students/admin_dashboard.html', {'students': students})

    # Student sees own application
    try:
        data = StudentApplication.objects.get(user=request.user)
    except StudentApplication.DoesNotExist:
        data = None
    return render(request, 'students/student_dashboard.html', {'data': data})
