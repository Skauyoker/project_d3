from datetime import datetime
from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Subscription, Category
from .filters import NewsFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'titl'
    # queryset = Post.author.order_by('text')
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'Posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'Posts'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostsSearch(ListView):
    model = Post
    ordering = 'titl'
    template_name = 'search.html'
    context_object_name = 'Posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

        # Переопределяем функцию получения списка товаров


class ThePost(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'Posts'


class PostCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ("news.add_post")

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/posts/articles/create/':
            post.category_type = 'AR'
        elif self.request.path == '/posts/news/create/':
            post.category_type = 'NW'
        post.save()

        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ("news.change_post")


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ("news.delete_post")


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Post.category_type.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
