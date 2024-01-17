from django.contrib import admin

from .models import User, UserSubscribe


@admin.register(User)
class UserAdminPanel(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email', 'username', 'is_staff',
              'is_active']


@admin.register(UserSubscribe)
class UserSubscribeAdmin(admin.ModelAdmin):
    fields = ['user', 'author']
