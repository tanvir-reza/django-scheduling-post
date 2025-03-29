from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class UserManagement(AbstractUser):
    email = models.EmailField(unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 15 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='user_management_set',  # Add related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_management_set',  # Add related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email


class Post(models.Model):
    author = models.ForeignKey(UserManagement, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100,blank=False,null=True)
    description = models.TextField(blank=False,null=True)
    image = models.ImageField(upload_to='post_images', blank=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

    # def save(self, *args, **kwargs):
    #     # cheking if the post created or updated
    #     is_created = self._state.adding
    #     super().save(*args, **kwargs)
    #     if is_created:
    #         from .tasks import publish_post
    #         publish_post.apply_async((self.id,), eta=self.post_time)
        
