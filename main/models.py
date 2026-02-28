from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to='avatars/',null=True,blank=True,default='avatars/default.png')
    bio = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return self.user.username
        

    
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="posts")
    # title = models.CharField(max_length=255)
    body = models.TextField()
    likes = models.ManyToManyField(User,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.author.username} - {self.body[:20]}"
    
    def likes_count(self):
        return self.likes.count()
    
    def comments_count(self):
        return self.comments.count()
    
    class Meta:
        ordering = ["-created_at"]
    

class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self",on_delete=models.SET_NULL,null=True, blank=True)
    body = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"comment by {self.author.username} on {self.post.body[:20]}"
    
    class Meta:
        ordering = ["-created_at"]
    
    
    