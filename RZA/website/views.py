from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate


# Create your views here.

def home(request):
    return render(request,'pages/index.html')

def navbar(request):
    return render(request,'components/navbar.html')

# register a user

from django.shortcuts import render, redirect
from .forms import CreateUserForm

#registering 
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')  

    context = {'form': form}
    return render(request, 'pages/register.html', context)

# logging in

def my_login(request):
    form= LoginForm

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
    context = {'login_form': form}
    return render(request,'pages/my-login.html', context=context)


# logout 
def user_logout(request):
    auth.logout(request)
    return redirect('my-login')

#





