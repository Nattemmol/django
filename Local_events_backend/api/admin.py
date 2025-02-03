from django.contrib import admin
from .models import User, Category, Event, Guest  # Import your models

# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'display_name')  # Columns to display
    search_fields = ('name', 'email')  # Fields for search functionality
    list_filter = ('name',)  # Filters in the sidebar

# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon_name')
    search_fields = ('name',)
    list_filter = ('icon_name',)

# Register the Event model
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'date', 'duration')
    search_fields = ('title', 'description', 'location')
    list_filter = ('date',)
    filter_horizontal = ('categories', 'guests')  # For many-to-many fields
    readonly_fields = ('gallery_images',)  # If you want to prevent editing certain fields

# Register the Guest model
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'image_path')
    search_fields = ('name', 'email')
    list_filter = ('name',)
