from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        # Add explicit 'data=' keyword argument
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = LoginForm(request)  # Keep request as only argument for GET
    
    return render(request, "accounts/login.html", {'form': form})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("accounts:login")
    else:
        form = RegisterForm()
    
    return render(request, "accounts/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/") 
