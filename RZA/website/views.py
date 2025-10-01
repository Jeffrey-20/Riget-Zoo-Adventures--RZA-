from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, LoginForm
from .models import Record
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm


# Home page
def home(request):
    return render(request, 'pages/index.html')


# Register a user
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()   # ✅ hashes password properly
            return redirect('my-login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'pages/register.html', context)


# Login
def my_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()   # ✅ AuthenticationForm handles authenticate
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()

    context = {'login_form': form}
    return render(request, 'pages/my-login.html', context)


# Logout
def user_logout(request):
    logout(request)
    return redirect('my-login')


# Dashboard (protected page)
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records':my_records}

    return render(request, 'pages/dashboard.html')

# Creating a record
@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ This saves to the database
            return redirect('dashboard')
        else:
            form = CreateRecordForm()
    context = {'form': form}
    return render(request, 'pages/create_record.html', context)







