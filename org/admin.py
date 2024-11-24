from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, CustomUser, Role

# Customize CustomUserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('id','username', 'email', 'organization', 'is_staff', 'is_active', 'is_superuser','role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'organization')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Organization Info', {'fields': ('organization',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'organization'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

# Customize OrganizationAdmin
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_main', 'created_by')
    search_fields = ('name', 'address')
    list_filter = ('is_main',)
    
    # Custom logic to restrict organization creation
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            raise PermissionDenied("Only superusers can create or manage organizations.")
        super().save_model(request, obj, form, change)

    # Customize form fields based on the user
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Limit the "created_by" dropdown to only superusers
        form.base_fields['created_by'].queryset = CustomUser.objects.filter(is_superuser=True)
        return form


# Customize RoleAdmin
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Role, RoleAdmin)
