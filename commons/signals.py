from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from commons.models import UserProfile  # ✅ commons에서 UserProfile 불러오기

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
