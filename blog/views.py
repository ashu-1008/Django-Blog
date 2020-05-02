from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.


def blogHome(request):
    allPosts = Post.objects.all()
    context = {
        'allPosts': allPosts,
    }
    return render(request, 'blog/blog.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comment = BlogComment.objects.filter(post=post, parent=None).order_by('-timeStamp')
    replies = BlogComment.objects.filter(post=post).exclude(parent=None).order_by('-timeStamp')
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    return render(request, 'blog/blogPost.html', {'post': post, 'comments': comment, 'replyDict': replyDict})


def postComment(request):
    if request.method == "POST":
        user = request.user
        comment = request.POST.get("comment")
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")

        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "your comment has been posted successfully...")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "your reply has been posted successfully...")

        red = '/blog/' + str(post.slug)
    return redirect(red)
