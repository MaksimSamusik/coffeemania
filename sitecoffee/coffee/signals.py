from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    """Создание аккаунта при регистрации нового пользователя."""
    if created:
        Account.objects.create(user=instance, balance=0.00)

@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    """Сохранение аккаунта при изменении пользователя."""
    instance.account.save()
