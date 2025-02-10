from django.contrib import admin

from .models import Profile, CustomUser


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
