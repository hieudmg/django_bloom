from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class SchoolClass(models.Model):
    name = models.TextField(max_length=30, default='')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
