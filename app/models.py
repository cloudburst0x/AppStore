from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class usersext(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nric= models.CharField(max_length=9, unique=True)
    dob = models.DateField()
    role = models.CharField(max_length=16)

class jobs(models.Model):
    jobid = models.CharField(max_length=10, unique=True)
    user = models.ForeignKey(usersext, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    rate = models.CharField(max_length = 4)
    experience_req = models.CharField(max_length = 2)
    job_requirement = models.TextField(_('describe the job requirement'), max_length=500, blank=True)

class babysitter(models.Model):
    user = models.ForeignKey(usersext, on_delete=models.CASCADE)
    bank_number = models.CharField(max_length=40)
    experience = models.CharField(max_length=2)
    rating_score = models.CharField(max_length=4)
    reviews = models.CharField(max_length=4)
    rate = models.CharField(max_length=4)
    available_startdate = models.DateField()
    available_enddate = models.DateField()



