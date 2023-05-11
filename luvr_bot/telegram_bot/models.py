from django.db import models


class Employee(models.Model):
    phone_number = models.CharField(max_length=250)


class EmployeeGeoPosition(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='geo_positions')
    latitude = models.CharField(max_length=300)
    longitude = models.CharField(max_length=300)


class BranchGeoPosition(models.Model):
    branch_name = models.CharField(max_length=250)
    latitude = models.CharField(max_length=300)
    longitude = models.CharField(max_length=300)
