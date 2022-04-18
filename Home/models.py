from django.db import models
from Company import models as company_models


# Create your models here.

class Subscription(models.Model):
    email = models.EmailField(unique=True, null=False, blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Comment(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=100, null=True, blank=False)
    discussion = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=False, blank=False, help_text="1000 words maximum")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Email(models.Model):
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    client = models.CharField(max_length=100, null=True, blank=True)
    send_to = models.EmailField(null=True, blank=True)
    message_type = models.CharField(max_length=200, null=True, blank=True)
    sender = models.CharField(max_length=100, null=True, blank=True)
    reservation = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, null=True, blank=True, on_delete=models.CASCADE)


class HelpCategory(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
