from django.contrib import admin
from .models import Destination, Banner

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_popular', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_popular', 'is_active')
    search_fields = ('name', 'description')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
