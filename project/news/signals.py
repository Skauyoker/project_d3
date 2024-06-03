from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post


# @receiver(post_save, sender=Post)
# def product_created(instance, **kwargs):
#     print('Создан товар', instance)

@receiver(m2m_changed, sender=Post)
def product_created(instance, **kwargs):

    if not kwargs["action"] == 'post_add':
        emails = User.objects.filter(
            subscriptions__category__in=instance.post_category.all()
        ).values_list('email', flat=True)

        subject = f'Новый пост в категории {instance.post_category}'

        text_content = (
            f'Пост: {instance.titl}\n'
            f'Автор: {instance.author}\n\n'
            f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Пост: {instance.titl}\n'
            f'Автор: {instance.author}\n\n'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
