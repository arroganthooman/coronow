from django.contrib import admin
from .models import Admin, Blog, Comment

# Register your models here.

admin.site.register(Admin)
admin.site.register(Blog)
admin.site.register(Comment)