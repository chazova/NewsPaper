from django_filters import FilterSet, CharFilter
import django_filters
from .models import Post


class NewsFilter(FilterSet):
    # title = CharFilter(lookup_expr='icontains')
    # author__author__username = CharFilter(lookup_expr='icontains')
    class Meta:
        model = Post

        fields = {
            'time_in': ['gt'],
            'title': ['iregex'],
            'author__author__username': ['iregex']
        }
        # labels = {
        #     'title': ('Поиск по заголовку'),
        # }
        # help_texts = {
        #     'title': ('Вспомогательный текст'),
        # }

