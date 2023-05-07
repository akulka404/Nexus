from django.db import models
from datetime import timedelta
# from six import python_2_unicode_compatible
from multiselectfield import MultiSelectField
from django.urls import reverse


class CRED_VERIFY(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    email = models.EmailField(default='')
    username = models.IntegerField()
    password = models.CharField(max_length=100, blank=False, default='')
    REGISTER_CHOICES = (('A', 'Admin'), ('T', 'Teacher'), ('S', 'Student'),)
    type_login = models.CharField(max_length=1, choices=REGISTER_CHOICES)

# class Meta:
#     ordering = ['computer_id']
