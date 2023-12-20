from django.contrib import admin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdminPanel(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'username', 'is_staff']
