from django.db import models

# Create your models here.
from django.urls import reverse_lazy


class AccountType(models.TextChoices):
    Administrator = 'A'
    User = 'U'


class User(models.Model):
    User_ID = models.BigAutoField(primary_key=True)
    User_Password = models.CharField(max_length=20, blank=True)
    User_FName = models.CharField(max_length=40, null=True)
    User_LName = models.CharField(max_length=40, null=True)
    User_DOB = models.DateField(auto_now=False, auto_now_add=False, null=True)
    User_Address = models.CharField(max_length=100, null=True)
    User_Phone = models.CharField(max_length=12, null=True)
    UserName = models.CharField(max_length=40, null=True)
    User_Email = models.CharField(max_length=40, null=True)
    Account_type = models.CharField(max_length=1, choices=AccountType.choices, default=AccountType.Administrator)



class Group(models.Model):
    Group_Id = models.BigAutoField(primary_key=True)
    Group_Name = models.CharField(max_length=20, unique=True, blank=True)
    Sport = models.CharField(max_length=50, unique=True, blank=True)
    Group_Description = models.CharField(max_length=256, null=True)
    Creator = models.ForeignKey(User, related_name='Group_Creator', on_delete=models.CASCADE, null=True)
    SpotsAvailable = models.IntegerField(null=True)
    Joined_Users = models.ManyToManyField('User', related_name='Joining_User')

    def get_absolute_url(self):
        return reverse_lazy('GroupsEventsPage/', kwargs={'group_id': self.Group_Id})

class GroupReservation(models.Model):
    GroupReservation_Id = models.BigAutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)


class Location(models.Model):
    Location_Id = models.BigAutoField(primary_key=True)  # just a name
    Location_Name = models.CharField(max_length=40, null=True)
    Location_Address = models.CharField(max_length=40, null=True)


class Event(models.Model):
    Event_Id = models.BigAutoField(primary_key=True)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    Date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    Location = models.CharField(max_length=40, null = True)
    Event_Description = models.CharField(max_length=256, null=True)
    Event_Name = models.CharField(max_length=256, null=True)

class Reservation(models.Model):
    Reservation_Id = models.BigAutoField(primary_key=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

class GroupPost(models.Model):
    GroupPostID =models.BigAutoField(primary_key=True)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    Title = models.CharField(max_length=40, null = True)
    BodyText = models.CharField(max_length=256, null=True)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)


class Admin(User):
    pass
