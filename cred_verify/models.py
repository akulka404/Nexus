from django.db import models
from datetime import timedelta
# from six import python_2_unicode_compatible
from multiselectfield import MultiSelectField
from django.urls import reverse


class CRED_VERIFY(models.Model):
    username = models.IntegerField()
    password = models.IntegerField()
    REGISTER_CHOICES = (('A', 'Admin'), ('T', 'Teacher'), ('S', 'Student'),)
    type_login = models.CharField(max_length=1, choices=REGISTER_CHOICES)

# class Meta:
#     ordering = ['computer_id']
