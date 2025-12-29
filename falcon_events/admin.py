from django.contrib import admin
from falcon_events.models import Category, Event, Registration

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'category',
                'start_datetime', 'end_datetime', 'location',
                'capacity', 'max_guests_per_user', 'created_by']
    list_filter = ['category', 'start_datetime', 'created_by', 'location']
    
    search_fields = ['title', 'description', 'location', 'category__name', 'created_by__username']
    
    ordering = ['-end_datetime']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'registered_at', 'guests']
    list_filter = ['event', 'registered_at']
    search_fields = ['user__username', 'event__title']