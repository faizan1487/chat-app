from django.contrib import admin
from .models import FriendList

class FriendListAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user']
    filter_horizontal = ['friends']


admin.site.register(FriendList, FriendListAdmin)
