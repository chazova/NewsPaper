from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
    DeleteView  # импортируем необходимые дженерики
from django.utils import timezone
from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from django.views import View
from .models import *
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache # импортируем наш кэш
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from datetime import datetime

from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import CategorySubscriber



class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'rest/news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестисься наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    # queryset = Post.objects.order_by('-time_in')
    ordering = ['-time_in']  # сортировка по времени в порядке убывания
    paginate_by = 10  # поставим постраничный вывод в один элемент

    def get_queryset(self):
        queryset = NewsFilter(self.request.GET, super().get_queryset()).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_now'] = timezone.localtime(timezone.now())  # добавим переменную текущей даты time_now
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['choices'] = Post.TYPE_CHOICES
        context['form'] = NewsForm()
        return context

    # def get_queryset(self) -> QuerySet(any):
    #     post_filter = PostFilter(self.request.GET, queryset=Post.objects.all())
    #     return post_filter.qs.order_by('-time_in')
    # def get_queryset(self, *args, **kwargs):
    #     queryset = super().get_queryset(*args, **kwargs)
    #     queryset = NewsFilter(self.request.GET, queryset=queryset)
    #     return queryset

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


# class NewsDetail(DetailView):
#     model = Post
#     template_name = 'rest/new.html'
#     context_object_name = 'news'


# пример постраничного вывода на простых views:
class News(View):
    def get(self, request):
        news = Post.objects.order_by('-time_in')
        n = Paginator(news, 2)

        news = n.get_page(request.GET.get('page', 1))
        data = {
            'news': news,
        }

        return render(request, 'rest/news.html', data)


# дженерик для получения деталей о товаре
class NewsDetailView(DetailView):
    template_name = 'rest/news_detail.html'
    context_object_name = 'news'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует также.
        # Он забирает значение по ключу, если его нет, то забирает None.
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj
        # id = self.kwargs.get('pk')
        # return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        categories = context['object'].category.all()
        is_not_subscriber = False
        for category in categories:
            if not (user in category.subscribers.all()) and not is_not_subscriber:
                is_not_subscriber = True
        context['is_not_subscriber'] = is_not_subscriber
        return context


@login_required
def upgrade_me(request, pk):
    user = request.user
    categories = Post.objects.get(pk=pk).category.all()
    for category in categories:
        print(category)
        if not (user in category.subscribers.all()): category.subscribers.add(user)
    print(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect(f'/news/{pk}')


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'rest/news_create.html'
    form_class = NewsForm
    permission_required = ('rest.add_post',)


# дженерик для редактирования объекта
class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'rest/news_create.html'
    form_class = NewsForm
    permission_required = ('rest.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'rest/news_delete.html'
    context_object_name = 'news'
    queryset = Post.objects.all()
    success_url = reverse_lazy('rest:news')  # не забываем импортировать функцию reverse_lazy из пакета django.urls
    permission_required = ('rest.delete_post',)



