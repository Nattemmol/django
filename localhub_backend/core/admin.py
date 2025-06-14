from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Location, Profile, Verification

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'phone', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'role', 'location', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2')
        }),
    )
    ordering = ('email',)
    search_fields = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(Location)
admin.site.register(Verification)