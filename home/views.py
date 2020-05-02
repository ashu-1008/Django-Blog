from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from blog.models import Post


# Create your views here.

# Html PAges
def home(request):
    allUsers = User.objects.all()
    for userName in allUsers:
        if userName == 'ashu':
            print('old user')

    latestPost = Post.objects.all().order_by('-timeStamp')
    if len(latestPost) >= 2:
        latestPost = latestPost[0:2]
    data_for_frontend = {
        'superUser': 'ashu',
        'latestPost': latestPost,
    }
    return render(request, 'home/home.html', data_for_frontend)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone')
        query = request.POST.get('query')
        if len(name) < 2 or len(email) < 4 or len(phone_no) < 10 or len(query) < 20:
            messages.error(request, 'Please Fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone_no, query=query)
            contact.save()
            messages.success(request, 'Your Query has been sent successfully, We will Contact you soon.')
    return render(request, 'home/contact.html')

#
# def about(request):
#     return render(request, 'home/about.html')


def search(request):
    query = request.GET.get('query')
    if len(query) > 70:
        post = Post.objects.none()
    else:
        postTitle = Post.objects.filter(title__icontains=query)
        postContent = Post.objects.filter(content__icontains=query)
        postAuthor = Post.objects.filter(author__icontains=query)
        post = postTitle.union(postContent, postAuthor)

    if post.count() == 0:
        messages.warning(request, "No search result found. Please refine your query")

    data_for_frontend = {
        'post': post,
        'query': query,
    }
    return render(request, 'home/search.html', data_for_frontend)


# Authenticate APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        allUsers = User.objects.all()

        # check for errorneous inputs
        for userName in allUsers:
            if str(username) == str(userName):
                messages.error(request, "Username not available")
                return redirect('home')

        if len(username) > 15 or len(username) < 4:
            messages.error(request, "Username must be between 4 and 15 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username should contain only letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
    return redirect('home')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')


def adminPanel(request):
    if str(request.user) == 'ashu':
        allPosts = Post.objects.all()
        data = {
            'allPosts': allPosts,
        }
        if request.method == 'POST':
            if str(request.POST.get('data')) == 'addPost':
                title = request.POST.get('pTitle')
                content = request.POST.get('content')
                author = request.POST.get('author')
                slug = request.POST.get('slug')
                print(title, content, author, slug)
                post = Post(title=title, content=content, author=author, slug=slug, timeStamp=timezone.now())
                post.save()
            elif str(request.POST.get('data')) == 'deletePost':
                sno = request.POST.get('sno')
                post = Post.objects.get(sno=sno)
                post.delete()
        return render(request, 'home/adminPanel.html', data)
    else:
        return redirect('home')

