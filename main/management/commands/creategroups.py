"""
Create all groups

Add publish permissions to redactors and admins
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from main import models

HAS_PERM_GROUPS = settings.HAS_PERM_GROUPS
NO_PERM_GROUPS = settings.NO_PERM_GROUPS


class Command(BaseCommand):
    help = 'Creates groups'

    def handle(self, *args, **options):
        # create permission for Pub model
        permission, created = Permission.objects.get_or_create(codename='can_publish')
        if created:
            permission.name = 'Can publish'
            content_type = ContentType.objects.get_for_model(models.Pub)
            permission.content_type = content_type
            permission.save()

        # create groups with perm and 'give' him permission
        for group in HAS_PERM_GROUPS:
            role, created = Group.objects.get_or_create(name=group)
            role.permissions.add(permission)

        # create groups without permissions
        for group in NO_PERM_GROUPS:
            role, created = Group.objects.get_or_create(name=group)

        print("Done")