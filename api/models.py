from django.db import models

# Create your models here.

class EmployeeDetails(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email
    

class File(models.Model):
    file = models.FileField(upload_to="files")