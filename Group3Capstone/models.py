from django.db import models


# Create your models here.
class AccountType(models.TextChoices):
    Administrator = 'A'
    User = 'U'


class User(models.Model):
    User_ID = models.BigAutoField(primary_key=True)
    User_Password = models.CharField(max_length=20, unique=True)
    User_FName = models.CharField(max_length=40)
    User_LName = models.CharField(max_length=40)
    User_DOB = models.DateField(auto_now=False, auto_now_add=False)
    User_Address = models.CharField(max_length=100)
    User_Phone = models.IntegerField()
    UserName = models.CharField(max_length=40)
    User_Email = models.CharField(max_length=40)
    Account_type = models.CharField(max_length=1, choices=AccountType.choices, default=AccountType.Administrator)


class Sport(models.Model):
    Sport_Id = models.BigAutoField(primary_key=True)
    Sport_Name = models.CharField(max_length=40)  # just the name....


class Group(models.Model):
    Group_Id = models.BigAutoField(primary_key=True)
    Sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Location(models.Model):
    Location_Id = models.BigAutoField(primary_key=True)  # just a name
    Location_Name = models.CharField(max_length=40)
    Location_Address = models.CharField(max_length=40)


class Event(models.Model):
    Event_Id = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    Date = models.DateTimeField(auto_now=False, auto_now_add=False)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Reservation(models.Model):
    Reservation_Id = models.BigAutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Admin(User):
    pass
