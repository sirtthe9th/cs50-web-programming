from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Specify a unique related name for the groups field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    # Specify a unique related name for the user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
