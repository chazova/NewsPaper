from django.urls import path

from .views import NewsList, News, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView

app_name = 'rest'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('search/', NewsList.as_view(), name='news'),
    # path('<int:pk>', NewsDetail.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'), # Ссылка на детали товара
    path('add/', NewsCreateView.as_view(), name='news_create'), # Ссылка на создание товара
    # path('news/', News.as_view())
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_update'), # Ссылка на редактирование товара
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'), # Ссылка на удаление товара
]