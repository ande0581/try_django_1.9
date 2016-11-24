from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
from .models import Post
from .forms import PostForm


def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # print(form.cleaned_data)
        # print(form.cleaned_data.get('title'))
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, 'post_form.html', context)


def post_detail(request, pk):
    instance = get_object_or_404(Post, id=pk)
    context = {'title': instance.title,
               'instance': instance}
    return render(request, 'post_detail.html', context)


def post_list(request):
    queryset_list = Post.objects.all().order_by('-timestamp')  # sorts by timestamp, newest first
    paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {'title': 'list',
               'object_list': queryset}
    return render(request, 'post_list.html', context)


def post_update(request, pk=None):
    instance = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Saved")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {'title': instance.title,
               'instance': instance,
               'form': form}
    return render(request, 'post_form.html', context)


def post_delete(request, pk):
    instance = get_object_or_404(Post, id=pk)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:list")