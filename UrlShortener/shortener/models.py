from django.db import models


class URL(models.Model):
    targetURL = models.CharField(max_length=1000)
    shortenedURL = models.CharField(max_length=20, primary_key=True)

class AdminConfig(models.Model):
    min_url_length = models.IntegerField(default = 5)
    max_url_length = models.IntegerField(default = 10)
    allow_uppercase = models.BooleanField(default = True)
    allow_lowercase = models.BooleanField(default = True)
    allow_digits = models.BooleanField(default = True)
    myDomain = models.CharField(max_length = 100, default = 'http://localhost:8000/')
    prefix = models.CharField(max_length = 100, default = '', blank = True)
    suffix = models.CharField(max_length = 100, default = '', blank = True)
