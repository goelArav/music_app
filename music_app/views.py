from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Comment, Musician, Genre, Post
from django.db.models import Count
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


# Create your views here.
def music_home(request):
    most_followed_musicians = Musician.objects.annotate(nfollowers=Count('musician_followers')).order_by('-nfollowers')[:5]
    return home(request, most_followed_musicians)

@login_required(login_url='/music_app/sign_in')
def home(request, most_followed_musicians):
    # try:
    #     genre = Genre.objects.get(id=genre_id)
    # except Genre.DoesNotExist:
    #     raise Http404("No Genre Available")
   

    # output = ''
    # for m in most_followed_musicians:
    #     output += ((m.musician_name)  + ' No. of followers: ' +  str(m.nfollowers)) + '<br>'

    
    context = {
        'most_followed_musicians' : most_followed_musicians,
        'genres': Genre.objects.all()

    }
    # genres = Genre.objects.get()
    # output1 =''
    # for item in genres:
    #     output1 += item
    return render(request, 'music_app/music_home.html', context)
def musician_page(request, musician_id):
    try:
        musician = Musician.objects.get(id=musician_id)
    except Musician.DoesNotExist:
        raise Http404("musician does not exist")
    
    posts = musician.post_set.all()

    context = {
        'posts': posts, 'musician': musician
    }
    return render(request, 'music_app/musician_page.html', context)
def like(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.post_likers.all():
        post.post_likers.remove(request.user)
    else:
        post.post_likers.add(request.user)
    return(redirect(request.META['HTTP_REFERER']))
def post_comment(request, post_id):
    author = request.user
    text = request.POST['post_conversation']
    post_conversation = Comment(comment_text=text, comment_author=author, comment_post=Post.objects.get(id=post_id))
    post_conversation.save()

    return(redirect(request.META['HTTP_REFERER']))
def post_post(request, musician_id):
    try:
        image = request.FILES['post_image']
        print(image)
    except:
        image = None


    author = request.user

    try:
        text = request.POST['post_post']
    except KeyError:
        return redirect(request.META['HTTP_REFERER'])
    post_post = Post(post_text=text, post_author=author, post_image=image, post_musician=Musician.objects.get(id=musician_id) )

    post_post.save()
    

    
    return(redirect(request.META['HTTP_REFERER'])) 

def add_musician(request):
    
    try:
        image = request.FILES['add_image']

    except:
        image = None
    try:
        bio = request.POST['add_bio']
    except:
        bio = None
    text = request.POST['add_musician']
    genre_id = request.POST['genre']
    genre = Genre.objects.get(id=genre_id)
    

    add_musician = Musician(musician_name=text, musician_genre=genre, musician_bio=bio, musician_photo=image)
    add_musician.save()
    return redirect(reverse('music_app:musician_page', args=(add_musician.id,)))

def genrebased_home(request, genre_id):
    genre_musicians = Musician.objects.filter(musician_genre=Genre.objects.get(id=genre_id)).annotate(nfollowers=Count('musician_followers')).order_by('-nfollowers')[:5]
    return home(request, genre_musicians)
def follow_musician(request, musician_id):
    
    musician = Musician.objects.get(id=musician_id)

    if request.user in musician.musician_followers.all():
        musician.musician_followers.remove(request.user)
    else:
        musician.musician_followers.add(request.user)

    return(redirect(request.META['HTTP_REFERER']))
    

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['newusername']
        password = request.POST['newuserpassword']

        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            messages.error(request, 'User already exists')
            return redirect('music_app:sign_in')        
        
        if user is not None:
            login(request, user)
            return redirect('music_app:music_home')# Redirect to a success page.
                    
        else:
            messages.error(request, 'Sorry we failed to create user')
            return redirect('music_app:sign_in')


     
          
    else:
        return render(request, 'music_app/login.html')


def sign_in(request):

    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['userpassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('music_app:music_home')
            # Redirect to a success page.
            
        else:
            messages.error(request, 'Sorry, username or password was not recognised')
            return redirect('music_app:sign_in')
            # Return an 'invalid login' error message.
           
    else:
        return render(request, 'music_app/login.html', {})

def search(request):
    
    search_term = request.GET['search']
    print(search_term)
    musicians = Musician.objects.filter(musician_name__icontains=search_term)
    print(musicians)

    if len(musicians) == 1:
        return redirect('music_app:musician_page', musician_id=musicians[0].id)


    return home(request, musicians)


def logout_view(request):
    if request.user != 'admin':
        logout(request)
        return(redirect('music_app:sign_in'))

def send_to_signin(request):
    logout(request)
    return(redirect('music_app:sign_in'))







