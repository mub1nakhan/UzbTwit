from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Post



def logout_view(request):
    logout(request)
    return redirect("home")

def home(request):
    
    if request.method == "POST":
        body = request.POST.get("body")
        user= request.user
        post = Post.objects.create(
            author=user,
            body=body
        )
        return redirect("home")
    
    posts = Post.objects.all().select_related("author", "author__profile")
    users = User.objects.exclude(id=request.user.id)[:5]

    return render(request, "home.html", {
        "posts": posts,
        "users": users
    })
    

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "username yoki password xato")
        return redirect("login")
        
    return render(request, "auth/login.html")

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bunday username mavjud!")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Bunday email mavjud!")
            return redirect("register")
        
        if password1 != password2:
            messages.error(request, "Parollar mos emas!")
            return redirect("register")
        
        
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1  
        )
        
        login(request, user)
        return redirect("home")
        
        
        
    return render(request,"auth/register.html")
