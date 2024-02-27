from django.db import models
from contacts.models import *
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class UploadFile(models.Model):
    file = models.FileField(upload_to='media/')
    file_name = models.CharField(max_length=255)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved

    def __str__(self):
        return self.file_name


class WastePaperBin(models.Model):
    file = models.FileField(upload_to='media/', null=True, blank=True)
    file_name = models.CharField(max_length=255)
    deleted_on = models.DateField()
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    
    def __str__(self):
        return self.file_name

@receiver(pre_delete, sender=UploadFile)
def create_waste_paper_bin(sender, instance, **kwargs):
    WastePaperBin.objects.create(
        file=instance.file,
        file_name=instance.file_name,
        deleted_on=timezone.now(),
        MyInfo=instance.MyInfo
    )


class Folder(models.Model):
    folder_name = models.CharField(max_length=255)
    upload_file = models.OneToOneField(UploadFile, on_delete=models.SET_NULL, null=True)
    MyInfo = models.ForeignKey(MyInfo, on_delete=models.CASCADE)

    created = models.DateTimeField(default=timezone.now)  # Auto-populated when created
    updated = models.DateTimeField(auto_now=True)  # Auto-updated every time the model is saved
    
    def __str__(self):
        return self.folder_name
