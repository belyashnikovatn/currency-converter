from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',
                    'email', 'date_joined')
    list_filter = ('username', 'email',)
    search_fields = ('email', 'username')
    empty_value_display = '-пусто-'
