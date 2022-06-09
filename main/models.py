from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class NewUser(AbstractUser):
    phone_number = models.CharField(max_length=10, null=False)
    email = models.EmailField()
    code = models.CharField(max_length=10, null=False, default="+91")

class Reference(models.Model):
    #maually define default value
    referance_id = models.AutoField(primary_key=True)
    ref_type = models.CharField(max_length=100, null=False)
    field1 = models.CharField(max_length=100, null=False)
    field2 = models.CharField(max_length=100, null=True)
    field3 = models.CharField(max_length=100, null=True)
    field4 = models.CharField(max_length=100, null=True)
    field5 = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.referance_id)
class DbInformation(models.Model):
    client_id = models.CharField(max_length=10, null=False)
    referance_id = models.ForeignKey(Reference, on_delete=models.CASCADE,default=1)

class ClientIdMapping(models.Model):
    client_id = models.CharField(max_length=10, null=False)
    ethan_token = models.CharField(max_length=100, null=True)


class Tableau(models.Model):
    sitename = models.CharField(max_length=150, null=True)
    password = models.CharField(max_length=150, null=True)
    user_id = models.CharField(max_length=150, null=True)

class TableauConnection(models.Model):
    client_id = models.CharField(max_length=150, null=True)
    tableau_id = models.CharField(max_length=150, null=True)
    