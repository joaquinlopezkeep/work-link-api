from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import EmployeeCreationForm, EmployeeChangeForm
from .models import Employee


class EmployeeAdmin(UserAdmin):
    """
    Employee Admin taken from: https://testdriven.io/blog/django-custom-user-model/
    and adapted to show display user group eg is_cleaner, is_manager.
    """
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name',
         'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Group Permissions', {
            'classes': ('expand',),
            'fields': ('groups', 'user_permissions', )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'groups', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Employee, EmployeeAdmin)
