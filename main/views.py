from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Post, Comment
from django.contrib.auth.decorators import login_required



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
    
    
    

def about_developer(request):
    context = {
        "name": "Mubinaxon Gafurovna",
        "profession": "Python & Dart",
        "experience": "3 oy+ tajriba",
        "description": "Men zamonaviy web ilovalar, REST API va to‘liq backend tizimlar yaratish bilan shug‘ullanaman. Django, PostgreSQL va API integratsiyalar bilan ishlayman. Maqsadim — xavfsiz, tezkor va foydalanuvchi uchun qulay platformalar yaratish.",
        
        "phone": "+998 91 234 56 78",
        "email": "mub1nakhano22@gmail.com",
        "telegram": "@programiistt",
        "instagram": "@mub1nakhan.o6",
        "github": "github.com/mub1nakhan",
        
        "location": "Toshkent, O'zbekiston"
    }

    return render(request, 'about.html', context)
   
    

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


def post_detail_view(request,pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all().order_by("-created_at")
    is_liked = False
    if request.user.is_authenticated:
        user = request.user
        
        is_liked = post.likes.filter(id=user.id).exists()
    
    context = {
        "post": post,
        "comments": comments,
        "is_liked": is_liked
    }
    
    return render(request,"post_detail.html",context)

@login_required(login_url="login/")
def comment_create(request):
    user = request.user
    
    if request.method == "POST":
        parent = request.POST.get("parent", None)
        body = request.POST.get("body")
        post_id = request.POST.get("post_id")
        
        post = get_object_or_404(Post, id=post_id)
        
        comment = Comment.objects.create(
            author=user,
            body=body,
            parent=parent,
            post=post
        )
        messages.success(request, "Comment succesfully created!")
        print("comment yaratildi:", comment)
        return redirect("post_detail", post_id)
    

@login_required
def like_post_view(request):
    user = request.user
    
    if request.method == "POST":
        
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            post.save()
        
        messages.success(request, "Liked post")
        return redirect("post_detail", post_id)
    
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        "user": user
    }
    return render(request,"user_profile.html", context)