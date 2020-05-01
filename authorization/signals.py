from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

DEFAULT_GROUP = settings.DEFAULT_GROUP


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_to_group(sender, instance, created, **kwargs):
    """
        Add default group(users) to new user
    """
    if created and not instance.is_superuser:
        group = Group.objects.get(name=DEFAULT_GROUP)
        instance.groups.add(group)
    elif instance.is_superuser:
        group = Group.objects.get(name='admins')
        instance.groups.add(group)
