from django.contrib import admin
from django.apps import apps
# Register your models here.
from .models import Post


for model in apps.get_app_config("app").models.values():
    admin.site.register(model)

for model in apps.get_app_config("allauth").models.values():
    admin.site.register(model)

for model in apps.get_app_config("dj_rest_auth").models.values():
    admin.site.register(model)

for model in apps.get_app_config("rest_framework_simplejwt").models.values():
    admin.site.register(model)
