from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.core.mail import send_mail, EmailMultiAlternatives, mail_managers, mail_admins
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class CustomSignupForm(SignupForm):
    # def save(self, request):
    #     user = super().save(request)
    #
    #     subject = 'Добро пожаловать в наш интернет-магазин!'
    #     text = f'{user.username}, вы успешно зарегистрировались на сайте!'
    #     html = (
    #         f'<b>{user.username}</b>, вы успешно зарегистрировались на '
    #         f'<a href="http://127.0.0.1:8000/posts">сайте</a>!'
    #     )
    #     msg = EmailMultiAlternatives(
    #         subject=subject, body=text, from_email=None, to=[user.email]
    #     )
    #     msg.attach_alternative(html, "text/html")
    #     msg.send()
    #
    #     return user

    # отправка рассылки зарегестрировавшемуся пользователю
    # def save(self, request):
    #     user = super().save(request)
    #
    #     mail_managers(
    #         subject='Новый пользователь!',
    #         message=f'Пользователь {user.username} зарегистрировался на сайте.'
    #     )
    #
    #     return user
    # отправка рассылки менеджерам

    def save(self, request):
        user = super().save(request)

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user
    # отправка рассылки админам



