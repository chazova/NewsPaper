from django.core.mail import EmailMultiAlternatives  # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from rest.models import Post
from datetime import date, timedelta


def get_subscriber(category):
    subscriber_emails = []
    for subscriber in category.subscribers.all():
        subscriber_emails.append(subscriber.email)
    return subscriber_emails


def new_post_subscription(instance, **kwargs):
    template = 'news_created_email.html'

    for category in instance.category.all():
        subject = instance.title
        subscriber_emails = get_subscriber(category)

        html_content = render_to_string(
            template,
            {
                'category': category,
                'post': instance,
            }
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body='',  # это то же, что и message
            from_email='test-mail-dj@yandex.ru',
            to=subscriber_emails,  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем


def notify_subscribers_weekly():
    current_date = date.today()
    one_week_ago_date = current_date - timedelta(days=7)
    posts_for_week = Post.objects.filter(time_in__range=[one_week_ago_date, current_date])
    for post in posts_for_week:
        categories = post.category.all()
        for category in categories:
            subscriber_emails = get_subscriber(category)

            html_content = render_to_string(
                'news_for_week.html',
                {
                    'category': category,
                    'posts': category.post_set.filter(time_in__range=[one_week_ago_date, current_date]),
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Новые статьи в категории {category.category_name}',
                body='',  # это то же, что и message
                from_email='test-mail-dj@yandex.ru',
                to=subscriber_emails,  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()


