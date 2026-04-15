from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ApplicationForm
from .models import StudentApplication

def home(request):
    return render(request, 'students/home.html')

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'students/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'students/login.html')

@login_required
def application(request):
    form = ApplicationForm(request.POST or None)
    if form.is_valid():
        app = form.save(commit=False)
        app.user = request.user
        app.save()
        return redirect('dashboard')
    return render(request, 'students/application.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        students = StudentApplication.objects.all()
        return render(request, 'students/admin_dashboard.html', {'students': students})

    data = StudentApplication.objects.filter(user=request.user).first()
    return render(request, 'students/student_dashboard.html', {'data': data})

def logout_view(request):
    logout(request)
    return redirect('login')
