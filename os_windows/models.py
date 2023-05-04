from django.db import models
from datetime import timedelta
# from six import python_2_unicode_compatible
from multiselectfield import MultiSelectField


class OS_Windows(models.Model):
    computer_id = models.IntegerField()
    computer_name = models.CharField(max_length=100, blank=False, default='')
    product_key = models.CharField(max_length=30, blank=False, default='')
    hostname = models.CharField(max_length=100, blank=False, default='')
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=100, blank=False, default='')
    softwares_installed = models.CharField(max_length=10000, blank=False, default='')
    software_count = models.IntegerField()
    authentic_software_count = models.IntegerField()
    unauthentic_software_count = models.IntegerField()

class Meta:
    ordering = ['computer_id']
