from django.db import models
from datetime import timedelta
# from six import python_2_unicode_compatible
from multiselectfield import MultiSelectField
from django.urls import reverse

class OS_Windows(models.Model):
    computer_id = models.AutoField(primary_key=True)
    username = models.IntegerField()
    computer_name = models.CharField(max_length=100, blank=False, default='')
    product_key = models.CharField(max_length=30, blank=False, default='')
    hostname = models.CharField(max_length=100, blank=False, default='')
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=100, blank=False, default='')
    softwares_installed = models.CharField(max_length=10000, blank=False, default='')
    software_count = models.IntegerField()
    authentic_software_count = models.IntegerField()
    unauthentic_software_count = models.IntegerField()

    def get_absolute_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[str(self.id), 'unique_identifier'])

class Meta:
    ordering = ['computer_id']
