from django.views.generic import ListView, DetailView
from datetime import datetime
from django.utils import timezone
from .models import *

class NewsList(ListView):
    model = Post # указываем модель, объекты которой мы будем выводить
    template_name = 'rest/news.html' # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестисься наши объекты
    context_object_name = 'news' # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-time_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.localtime(timezone.now())  # добавим переменную текущей даты time_now
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'rest/new.html'
    context_object_name = 'new'