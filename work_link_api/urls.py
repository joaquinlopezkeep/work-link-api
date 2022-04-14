from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sites.views import *
from employees.views import *


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'sites', SiteViewSet, basename='site')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'product-orders', ProductOrderViewSet,
                basename='product-order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('authentication/', include('employees.urls')),
    path('api/v1/', include(router.urls)),
]
