from urllib.parse import quote_plus
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

# Create your views here.


def posts_home(request):
    return HttpResponse("<h1>Hello</h1>")

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print (form.cleaned_data.get("title"))
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request,"Not Successfully Created - why this show up ?")

    # if request.method == "POST":
    #   print "title" + request.POST.get("content")
    #   print request.POST.get("title")
    #   #Post.objects.create(title=title)
    context = {
        "form": form,
        'formtype':"Create",
    }
    return render(request, "post_form.html", context)
    # return HttpResponse("<h1>Create</h1>")

def post_detail(request, slug=None): #retrieve
    # instance = Post.objects.get (id=10)
    today = timezone.now().date()
    instance = get_object_or_404(Post,slug = slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context ={
        "title":instance.title,
        "instance":instance,
        "instance.image.url":instance.image,
        "share_string": share_string,
        "today":today,

    }
    return render(request, 'post_detail.html',context)


def post_list(request): #list items
    today = timezone.now().date()
    qs_list = Post.objects.active().order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        qs_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        qs_list=qs_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct()

    paginator = Paginator(qs_list, 3) # Show 25 contacts per page
    page_request_var = "mooryn"
    page = request.GET.get(page_request_var)
    qs = paginator.get_page(page)

    # if request.user.is_authenticated:
    #     context ={
    #         "title":"My User List"
    #     }
    # else :
    #      context ={
    #          "title" : "List"
    #      }
    context ={
        "object_list" : qs,
        "title" : "List",
        "page_request_var":page_request_var,
        "today":today,
    }

    return render(request, 'post_list.html',context)



# def listing(request):
#     contact_list = Contacts.objects.all()

#     return render(request, 'list.html', {'contacts': contacts})


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Updated", extra_tags="some-extra-tags")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
        'formtype':"Update",
    }
    return render(request, "post_form.html", context)



def post_delete(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request,"Successfully Deleted", extra_tags="some-extra-tags")
    return redirect("postsurl:list")