from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.MainModel)
admin.site.register(models.Boost)