from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from multiselectfield import MultiSelectField
from employees.models import Employee
import os


def get_upload_path(instance, filename):
    """
    Helper function to create a dynamic path for each sites documentation
    """
    return os.path.join(
        "uploads/",
        instance.name + "/",
        filename
    )


PRODUCT_CATEGORY = (
    (1, 'Personal Protective Equipment'),
    (2, 'Cleaning Chemicals'),
    (3, 'Janitorial Products')
)

DAYS_IN_WEEK = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday')
)


class Site(models.Model):
    """
    Site model stores site information needed to identify each site.
    Is referenced by Job model and Product order model in a one (Site) to many (Job/ProductOrder)
    """
    name = models.CharField(_('Name of the site'), max_length=255)
    address = models.CharField(_('First Line of Address'), max_length=255)
    post_code = models.CharField(_('Post Code'), max_length=8)
    manager = models.ForeignKey(Employee, limit_choices_to={
                                'groups__name': 'Managers'}, on_delete=models.SET_NULL, null=True, blank=True, related_name='managers')
    client_name = models.CharField(_('Client Name'), max_length=100)
    client_contact_number = models.CharField(
        _('Clients Phone Number'), max_length=11)
    site_documentation = models.FileField(
        upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    """
    Job model stores a corresponding to a site. One site may have one or more Jobs
    For example Birkbeck Mallet Street is one site with various jobs such as general areas, toilets and classrooms
    Each job can be independent and can be assigned to the same or separate cleaner or in the case of large jobs 
    (e.g a spring clean) many cleaners. Job also specifies the rate and number of hours.
    """
    name = models.CharField(_('Job Name'), max_length=100)
    description = models.TextField()
    cleaner = models.ForeignKey(Employee, limit_choices_to={
                                'groups__name': 'Cleaners'}, on_delete=models.SET_NULL, blank=True, null=True)
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, blank=True, null=True, related_name='job_sites')
    rate = MoneyField(
        decimal_places=2,
        default=9.18,
        default_currency='GBP',
        max_digits=11
    )
    hours = models.DurationField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.site.name}: {self.name}"

    def __unicode__(self):
        return f"{self.site.name}: {self.name}"


class Schedule(models.Model):
    """
    Schedule models the ongoing schedule for jobs, including startime, endtime and frequency.
    It has a one to one relation with job as one job has exactly one schedule and one schedule belong to one job. 
    """
    shift_start_time = models.TimeField()
    shift_end_time = models.TimeField()
    frequency = MultiSelectField(choices=DAYS_IN_WEEK, max_choices=7)
    job = models.OneToOneField(
        Job, on_delete=models.CASCADE, related_name='job_schedule')

    def __str__(self):
        return self.job.__str__()


class ProductOrder(models.Model):
    """
    ProductOrder models supplies orders such as mops, chemicals and other supplies required for a job.
    Each site can have many Product Orders.
    """
    date = models.DateField(auto_now_add=True)
    name = models.CharField(_('Product Name'),
                            max_length=100, blank=False, null=False)
    category = MultiSelectField(choices=PRODUCT_CATEGORY, max_choices=1)
    quantity = models.IntegerField()
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, blank=True, null=True, related_name='product_site')
    fullfilled = models.BooleanField(default=False)

    def __unicode__(self):
        return "{site}: {jobname}".format(site=self.site.name, jobname=self.name)

    def __str__(self):
        return "{site}: {jobname}".format(site=self.site.name, jobname=self.name)
