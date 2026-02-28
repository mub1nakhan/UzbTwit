from django.urls import path
from .views import (home, logout_view,login_view,register_view,about_developer,
                    post_detail_view, comment_create, like_post_view,profile_view
                    )

urlpatterns = [
    path("", home, name="home"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("register/", register_view,name="register"),
    path("about/", about_developer,name="about"),
    path("post/<int:pk>/", post_detail_view, name="post_detail"),
    path("like/", like_post_view, name="like_post"),
    path("comment/", comment_create, name="comment_create"),
    path("userProfile/<str:username>/", profile_view, name="profile_view"),
]
