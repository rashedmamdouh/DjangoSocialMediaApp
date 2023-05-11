from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User=get_user_model()  

#Create Profile Model linked to the user using FK
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)  #User (admin) FK
    fname=models.CharField(max_length=100,default="NAN")
    lname=models.CharField(max_length=100,default="NAN")
    email=models.CharField(max_length=100,default="NAN")
    id_user=models.IntegerField()
    bio=models.TextField(blank=True)
    profileimg=models.ImageField( upload_to="profile_images", default="blank-profile-picture.png")
    location=models.CharField(max_length=100,blank=True)
    followers=models.IntegerField(default=0)
    following=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user_name=models.CharField(max_length=50)
    caption=models.TextField()
    image=models.ImageField(upload_to="post_images")
    created_at=models.DateTimeField(default=datetime.now)
    num_of_likes=models.IntegerField(default=0)

    def __str__(self):
        return self.user_name

#Connect the post with the username (unique)
class LikePost(models.Model):
    username=models.CharField(max_length=100)
    post_id=models.CharField(max_length=500)
    def __str__(self):
        return self.username

class Followers(models.Model):
    username=models.CharField(max_length=100,default="NAN") #own profile
    follower=models.CharField(max_length=100,default="NAN") #follower
    def __str__(self):
        return self.username
    
    username=models.CharField(max_length=100,default="NAN")
    following=models.CharField(max_length=100,default="NAN")
    def __str__(self):
        return self.username