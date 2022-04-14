from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee


class EmployeeCreationForm(UserCreationForm):
    """
    EmployeeCreationForm code taken from: https://testdriven.io/blog/django-custom-user-model/
    """
    class Meta:
        model = Employee
        fields = ('email',)


class EmployeeChangeForm(UserChangeForm):
    """
    EmployeeChangeForm code taken from: https://testdriven.io/blog/django-custom-user-model/
    """
    class Meta:
        model = Employee
        fields = ('email',)
