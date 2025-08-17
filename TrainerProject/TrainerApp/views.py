from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Course, Department, Document, Unit, CustomUser

# Create your views here.

def home(request):
    return render(request, "front-end/index.html")

def department(request):
    title = "Departments"
    departments = Department.objects.all()
    return render(request, 'front-end/departments.html', {'departments': departments, 'title': title})

def course(request, id):
    department = Department.objects.get(id=id)
    courses = Course.objects.filter(department=id)
    return render(request, 'front-end/courses.html', {'courses': courses, 'department': department})

def unit(request, id):
    course = Course.objects.get(id=id)
    units = Unit.objects.filter(course=course)
    return render(request, 'front-end/units.html', {'units': units, 'course': course})

def document(request, id):
    unit = Unit.objects.get(id=id)
    documents = Document.objects.filter(unit=unit)
    return render(request, 'front-end/documents.html', {'documents': documents, 'unit': unit})

def contact(request):
    return render(request, 'front-end/contact.html')

def user_login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # Here you would typically authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or Password')
        else:
            login_form = LoginForm()
    return render(request, 'back-end/login.html', {'login_form': login_form})

def user_register(request):
    register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration Successful")
            return redirect('user-login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        register_form = RegisterForm()
    return render(request, 'back-end/register.html', {'register_form': register_form})


def dashboard(request):
    user = request.user
    return render(request, 'back-end/dashboard.html', {'user': user})

def user_courses(request, id):
    user_department = request.user.department_id
    courses = Course.objects.filter(department_id=user_department)
    return render(request, 'back-end/user-courses.html', {'courses': courses})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('user-login')

