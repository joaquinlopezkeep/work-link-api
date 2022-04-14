from django.contrib import admin
from .models import Job, Site, Schedule, ProductOrder


class JobInline(admin.TabularInline):
    """
    Displays Jobs inline in the site admin form. 
    This enables the IT admin to perform CRUD actions on a 
    sites jobs without the need to change to the jobs form.
    """
    model = Job
    extra = 2


class ProductInline(admin.TabularInline):
    """
    Displays ProductOrders inline in the site admin form. 
    This enables the IT admin to perform CRUD actions on the
    sites product orders without the need to change to the product order form.
    """
    model = ProductOrder
    extra = 2


class ScheduleInline(admin.TabularInline):
    """
    Displays a jobs schedule inline in the Jobs form.
    Allows IT Admin to perform CRUD operations on the jobs schedule from the Jobs form.
    """
    model = Schedule
    extra = 2


class SiteAdmin(admin.ModelAdmin):
    """
    Site admin with inline Jobs and Product Orders
    """
    list_display = ('name', )
    search_fields = ['name']
    inlines = (JobInline, ProductInline,)
    ordering = ('name',)


class JobAdmin(admin.ModelAdmin):
    """
    Jobs Admin with inline Schedule 
    """
    list_display = ('name',)
    search_fields = ['name']
    inlines = (ScheduleInline, )
    ordering = ('name',)


admin.site.register(Site, SiteAdmin)
admin.site.register(Job, JobAdmin)
