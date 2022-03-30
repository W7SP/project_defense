from django.contrib import admin
from final_project.accounts.models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_filter = ('email', 'groups', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
    )
