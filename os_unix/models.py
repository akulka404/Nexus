from django.db import models
from datetime import timedelta
# from six import python_2_unicode_compatible
from multiselectfield import MultiSelectField
from django.urls import reverse


class OS_UNIX(models.Model):
    computer_id = models.AutoField(primary_key=True)
    username = models.IntegerField()
    computer_name = models.CharField(max_length=100, blank=False, default='')
    os_version = models.CharField(max_length=100, blank=False, default='')
    serial_number = models.CharField(max_length=30, blank=False, default='')
    build_version = models.CharField(max_length=100, blank=False, default='')
    hardware_uuid = models.CharField(max_length=100, blank=False, default='')
    provisioning_udid = models.CharField(max_length=100, blank=False, default='')
    hostname = models.CharField(max_length=100, blank=False, default='')
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=100, blank=False, default='')
    softwares_installed = models.TextField()
    software_count = models.IntegerField()
    authentic_software_count = models.IntegerField()
    unauthentic_software_count = models.IntegerField()
    
    def get_absolute_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[str(self.id), 'unique_identifier'])


class Meta:
    ordering = ['computer_id']
