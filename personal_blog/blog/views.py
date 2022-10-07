from ast import Pass
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

# Create your views here.
def index(request):

    return render(request, "blog/all_posts.html")

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            redirect('index')
        else:
            return render(request, "blog/all_posts.html", {"message": f" {user} Invalid username and/or password."})
    
    return render(request, 'blog/all_posts.html')


def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        # ensure password equals confirmation
        password = request.POST.get('password')
        confirmation = request.POST.get('passwordConf')

        if password != confirmation:
            return render(request, 'blog/register.html', {'message': 'Passwords must match.'})
        
        # create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # login user
            login(request, user)

            return redirect('index')
        except IntegrityError as e:
            print(e)
            return render(request, 'blog/register.html', {'message': 'Email already taken.'})
        
    return render(request, 'blog/register.html')

def recover_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)

        if form.is_valid():
            form.send_mail(
                subject_template_name= 'Reset Password',
                email_template_name= 'Body test',
                context= '',
                from_email='soraiaoliveira094@gmail.com',
                to_email=request.POST.get('email')
            )
            form.save()
    else:
        form = PasswordResetForm()
    
    return render(request, 'blog/reset_password.html', {'form': form})

@login_required
def new_post(request):

    form = PostForm(request.POST or None)

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)

            # to be replaced once i set up login system
            new_post.author = User.objects.get(username=request.user)
            new_post.save()

            return redirect('index')
    else:
        form = PostForm()
    
    context_dict = {
        'post_form': form,
    }

    return render(request, "blog/new_post.html", context=context_dict)