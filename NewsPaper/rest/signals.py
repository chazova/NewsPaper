from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post, PostCategory, Category, CategorySubscriber
from django.core.mail import EmailMultiAlternatives # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string # импортируем функцию, которая срендерит наш html в текст
from rest.tasks import new_post_subscription


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)

