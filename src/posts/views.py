from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.
from .models import Post


def post_create(request):
    return HttpResponse('<h1>create</h1>')


def post_detail(request, pk):
    instance = get_object_or_404(Post, id=pk)
    context = {'title': instance.title,
               'instance': instance}
    return render(request, 'post_detail.html', context)


def post_list(request):
    queryset = Post.objects.all()
    context = {'title': 'list',
               'object_list': queryset}
    return render(request, 'index.html', context)


def post_update(request):
    return HttpResponse('<h1>update</h1>')


def post_delete(request):
    return HttpResponse('<h1>delete</h1>')