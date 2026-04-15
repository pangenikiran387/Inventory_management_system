from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group, User

from products import models

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)


            if user.is_superuser or user.groups.filter(name='Admin').exists():
                return redirect('dashboard')

            elif user.groups.filter(name='Staff').exists():
                return redirect('products:product_list')

            else:
                return redirect('accounts:home')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

def home_view(request):
    return render(request, 'accounts/homepage.html')
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 🔒 Password match check
        if password1 != password2:
            return render(request, "accounts/register.html", {
                "error": "Passwords do not match"
            })

        # 🔒 Username exists check (FIX)
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Username already exists"
            })

        # 🔒 Email exists check
        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {
                "error": "Email already registered"
            })

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # ✅ Assign Staff role
        staff_group = Group.objects.get(name='Staff')
        user.groups.add(staff_group)

        return redirect('accounts:login')

    return render(request, "accounts/register.html")

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


