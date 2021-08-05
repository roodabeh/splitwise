from django.contrib import admin

from accounting.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone')


admin.site.register(User, UserAdmin)
