from django.db import models

# Create your models here.


class LTIConfiguration(models.Model):
    consumer_key = models.CharField(max_length=255, primary_key=True)
    secret_key = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RequestHistory(models.Model):
    timestamp = models.PositiveIntegerField()
    nonce = models.CharField(max_length=255)
    consumer = models.ForeignKey(LTIConfiguration)
