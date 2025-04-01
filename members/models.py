from django.contrib.auth.models import AbstractUser
from django.db import models

class Member(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True) 
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married'), ('Separated', 'Separated'), ('Widowed', 'Widowed')])
    license_expiration = models.DateField(null=True, blank=True)  # Allow null values 

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="member_groups",  # Avoids conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="member_permissions",  # Avoids conflict
        blank=True
    )

    def __str__(self):
        return self.username
