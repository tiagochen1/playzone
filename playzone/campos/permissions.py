from __future__ import annotations

from django.contrib.auth.models import Group
from django.http import HttpRequest


ADMIN_GROUP_NAME = "Admin"


def is_admin(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    return user.groups.filter(name=ADMIN_GROUP_NAME).exists()


def ensure_admin_group_exists():
    Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
