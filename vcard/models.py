from django.db import models

# Create your models here.


class Address(models.Model):
    office_name = models.CharField(max_length=255)
    full_address = models.TextField(blank=True, null=True)
    coordinates = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.office_name


class VCard(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to='vcard_photos/')

    def __str__(self):
        return self.full_name
