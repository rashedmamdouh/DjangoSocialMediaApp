from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Profile,Post,LikePost,Followers
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages #dynmic messages
from itertools import chain


@login_required(login_url="signin")
def index(request):
    user_profile=Profile.objects.get(user=request.user)
    following_users_list=[]
    posts=[]

    following_users=Followers.objects.filter(follower=request.user.username)
    for users in following_users:
        following_users_list.append(users.username)
    for username in following_users_list:
        posts.append(Post.objects.filter(user_name=username))
    posts_list=list(chain(*posts))                  #[[1,2],3]===>[1,2,3]

    profiles=[]
    Users=User.objects.all()
    for user in Users:
        if user.username not in following_users_list:
            if  user.username != request.user.username :
                profiles.append(Profile.objects.get(user=user))
    return  render(request,"index.html",{"user_profile":user_profile,"posts":posts_list,"profiles":profiles})

def signup(request):
    if request.method=="POST":
        #check admin (user) account
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        username=request.POST["Username"]
        email=request.POST["Email"]
        pass1=request.POST["Password"]
        pass2=request.POST["Password2"]
        if pass1==pass2 :
            if(User.objects.filter(email=email).exists()):
                messages.info(request,"Email Already Exist")
                return redirect("signup")
            if(User.objects.filter(username=username).exists()):
                messages.info(request,"Username Already Exist")
                return redirect("signup")
            else:
                user=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=pass1)
                user.save()

                # Login the user Automaticlly
                user_login=auth.authenticate(username=username,password=pass1)
                auth.login(request,user_login)

                #Create new profile to this user
                user_model=User.objects.get(username=username) #Forgien Key
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id,fname=user_model.first_name,lname=user_model.last_name,email=user_model.email)
                new_profile.save()
                return redirect("index")

        else:
            messages.info(request,"Not Same Password")
            return redirect("signup")
    return  render(request,"signup.html")

def signin(request):
    if request.method=="POST":
        username=request.POST["Username"]
        password=request.POST["Password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("index")
        else:
            messages.info(request,"Invalid user")
            return redirect("signin")
    
    return render(request,"signin.html")

@login_required(login_url="signin")
def signout(request):
    auth.logout(request)
    return redirect("signin")

@login_required(login_url="signin")
def settings(request):
    profile_change=Profile.objects.get(user=request.user)
    user_change=User.objects.get(username=request.user)
    print(User.objects.get(username=request.user).first_name)
    if request.method=="POST":
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        bio=request.POST["bio"]
        location=request.POST["location"]


        user_change.first_name=fname
        user_change.last_name=lname
        profile_change.fname=fname
        profile_change.lname=lname
        profile_change.location=location
        profile_change.bio=bio
        profile_change.save()
        user_change.save()
        if request.FILES.get('image')!=None:
            image=request.FILES.get('image')
            profile_change.profileimg=image
            profile_change.save()

    return render(request,"setting.html",{"profile_change":profile_change})

@login_required(login_url="signin")
def upload(request):
    if request.method=="POST":
        caption=request.POST["caption"]
        user_name=request.user.username
        if request.FILES.get('image_uploaded')==None:
            return redirect(index)
        image=request.FILES.get('image_uploaded')
        new_post=Post.objects.create(user_name=user_name,caption=caption,image=image)
        new_post.save()
    else:
        return redirect(index)
    return redirect("index")

@login_required(login_url="signin")
def like(request):
    username=request.user.username
    post_id=request.GET.get("post_id")  # GET requests are intended to retrieve data from   a server and do not modify the server's state. On the other hand, POST requests are used to send data to the server for processing and may modify 
    post=Post.objects.get(id=post_id)
    is_liked=LikePost.objects.filter(post_id=post_id,username=username).first()
    if is_liked==None:
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.num_of_likes= post.num_of_likes+1
        post.save()
        return redirect("/")
    else:
        is_liked.delete()
        post.num_of_likes= post.num_of_likes-1
        post.save()
        return redirect("/")
 
@login_required(login_url="signin")   
def profile(request,pk):
    user=User.objects.get(username=pk)
    profile=Profile.objects.get(user=user)
    posts=Post.objects.filter(user_name=pk)
    post_count=Post.objects.filter(user_name=pk).count()
    username=pk
    follower=Followers.objects.filter(username=username,follower=request.user.username).first()
    print(follower)
    att={"profile":profile,"username":username,"posts":posts,"post_count":post_count,"follower":follower}
    return render(request,"profile.html",att)
    
@login_required(login_url="signin")
def follow(request):
    if request.method=="POST":
        username=request.POST["username"]
        follower=request.user.username
        user=User.objects.get(username=username)
        user_profile=Profile.objects.get(user=user)
        request_profile=Profile.objects.get(user=request.user)
        follow=Followers.objects.filter(username=username,follower=request.user.username).first()
        if follow ==None:
            newfollower=Followers.objects.create(username=username,follower=request.user.username)
            user_profile.followers=user_profile.followers+1
            request_profile.following=request_profile.followers+1
            user_profile.save()
            request_profile.save()
            return redirect("/profile/"+username)
        else:
            follow.delete()
            user_profile.followers=user_profile.followers-1
            request_profile.following=request_profile.followers-1
            user_profile.save()
            request_profile.save()
            return redirect("/profile/"+username)
            
def search(request):
    if request.method=="POST":
        name=request.POST["search"]
        fname_to_search=Profile.objects.filter(fname=name)
        lname_to_search=Profile.objects.filter(lname=name)
        user_to_search_profiles=[]
        profiles=[]
        if (fname_to_search).first() != None :
            for user in fname_to_search:
                user_to_search_profiles.append(Profile.objects.filter(fname=name))
        else :
            for user in lname_to_search:
                user_to_search_profiles.append(Profile.objects.filter(lname=name))  
        for i in range(len(user_to_search_profiles)):
            profiles.append(user_to_search_profiles[i][i])
    return render(request,"search.html",{"searchprofiles":profiles})
    

