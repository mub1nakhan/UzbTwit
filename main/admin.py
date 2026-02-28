from django.contrib import admin
from .models import Post, Comment, UserProfile
from django.contrib.auth.models import User

admin.site.unregister(User)


class UserProfileInlineAdmin(admin.StackedInline):
    model = UserProfile
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "get_full_name", "profile__bio", "date_joined", "last_login"]
    inlines = [UserProfileInlineAdmin]

class CommentInlineAdmin(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "body", "get_likes_count", "get_comments_count", "created_at", "updated_at"]
    list_filter = ["author", "created_at", "updated_at"]
    inlines = [CommentInlineAdmin]
    
    def get_likes_count(self, obj):
        return obj.likes_count()
    
    def get_comments_count(self, obj):
        return obj.comments_count()
    
    