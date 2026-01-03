# users/signals.py
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

@receiver(post_save, sender=User)
def activate_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        instance.is_active = True
        instance.save()
