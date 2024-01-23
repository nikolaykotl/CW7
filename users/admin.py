from django.contrib import admin

# Register your models here.

from users.models import User

admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'country', 'tg_id')
