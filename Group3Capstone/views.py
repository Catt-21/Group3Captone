from datetime import datetime
from django.utils import timezone
from sqlite3 import IntegrityError

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import *  # create and add user models
from .classes.administrator import Admin


# Create your views here.

class Home(View):
    def get(self, request):
        request.session.pop("username", None)
        return render(request, "home.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False

        try:
            m = User.objects.get(UserName=request.POST['UserName'])
            badPassword = (m.User_Password != request.POST['User_Password'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "home.html", {"message": "user does not exist"})
        elif badPassword:
            return render(request, "home.html", {"message": "bad password"})
        else:
            request.session["username"] = m.UserName
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        uTest = request.session["username"]

        # using this variable from account view can now pass to a template via context and get whatever data needed
        u = User.objects.get(UserName=request.session['username'])

        return render(request, "dashboard.html", {"username": uTest, "user": u})


class CreateAccountsPage(View):
    def get(self, request):
        return render(request, "createAccountsPage.html", {"errors": {"Just returning GET"}})

    def post(self, request):
        first_name = request.POST['First_Name']
        last_name = request.POST['Last_Name']
        DOB = request.POST['DOB']
        phoneNumber = request.POST['PhoneNumber']
        userName = request.POST['UserName']
        role = "A"
        address = request.POST['Address']
        email = request.POST['Email']
        password = request.POST['Password']
        password2 = request.POST['Password2']

        error_dict = []

        if password != password2:
            error_dict.append("Passwords don't match, try again")
            return render(request, "home.html", {"errors": error_dict})

        newUser = User(User_FName=first_name, UserName=userName, User_LName=last_name, User_Password=password,
                       User_Phone=phoneNumber, Account_type=role, User_DOB=DOB, User_Address=address,
                       User_Email=email, )
        message_dict = []
        # error_dict = validate_user(user)
        valid = ["User successfully created"]

        try:
            newUser.save()
        except IntegrityError:
            error_dict.append("user_name / user_id already exists")
            return render(request, "createAccountsPage.html", {"errors": error_dict})
        else:
            return render(request, "home.html", {"errors": valid})
        # else:
        # return render(request, "create_user.html", {"errors": error_dict})


class Account(View):
    def get(self, request):
        if not request.session.get("username"):
            return redirect("/")
        u = User.objects.get(UserName=request.session['username'])
        return render(request, "account.html",
                      {"User_ID": u.User_ID, "User_Password": u.User_Password, "User_FName": u.User_FName,
                       "User_LName": u.User_LName,
                       "User_DOB": u.User_DOB, "User_Address": u.User_Address, "User_Phone": u.User_Phone,
                       "UserName": u.UserName, "User_Email": u.User_Email, "Account_type": u.Account_type})

    def post(self, request):
        uTest = request.session["username"]
        u = User.objects.get(UserName=uTest)
        return render(request, "account.html",
                      {"User_ID": u.User_ID, "User_Password": u.User_Password, "User_FName": u.User_FName,
                       "User_LName": u.User_LName,
                       "User_DOB": u.User_DOB, "User_Address": u.User_Address, "User_Phone": u.User_Phone,
                       "UserName": u.UserName, "User_Email": u.User_Email, "Account_type": u.Account_type, "user": u})


class EditAccountPage(View):
    def get(self, request):
        if not request.session.get("username"):
            return redirect("/")
        u = User.objects.get(UserName=request.session['username'])
        return render(request, "editaccount.html",
                      {"User_ID": u.User_ID, "User_Password": u.User_Password, "User_FName": u.User_FName,
                       "User_LName": u.User_LName,
                       "User_DOB": u.User_DOB, "User_Address": u.User_Address, "User_Phone": u.User_Phone,
                       "UserName": u.UserName, "User_Email": u.User_Email})

    def post(self, request):
        first_name = request.POST['First_Name']
        last_name = request.POST['Last_Name']
        DOB = request.POST['DOB']
        phoneNumber = request.POST['PhoneNumber']
        address = request.POST['Address']
        email = request.POST['Email']
        password = request.POST['Password']
        password2 = request.POST['Password2']

        error_dict = []

        if password != password2:
            error_dict.append("Passwords don't match, try again")
            return render(request, "editaccount.html", {"message": error_dict})
        request.session.get("username")
        u = User.objects.get(UserName=request.session["username"])
        u.User_FName = first_name
        u.User_LName = last_name
        u.User_DOB = DOB
        u.User_Phone = phoneNumber
        u.User_Address = address
        u.User_Email = email
        u.User_Password = password
        u.save()
        return render(request, "dashboard.html", {"user": u})


class Groups(View):
    def get(self, request):

        u = User.objects.get(UserName=request.session["username"])
        group = list(Group.objects.all())

        return render(request, "groups.html", {"user": u, "groups": group})

    def post(self, request):
        u = request.session["username"]
        currentUser = User.objects.get(UserName=request.session["username"])  # setting up user objects

        groupJoined = request.POST["name"]  # group ID

        g = Group.objects.get(Group_Id=groupJoined)
        joinedUsers = list(g.Joined_Users.all())  # returns a list of all user objects

        for i in joinedUsers:
            if (i.UserName == request.session["username"]):
                message = "You have already joined this group, here is who else is in your group"
                message2 = "To join another group, please click the group tab on the navigation bar up top to go back to the list of groups"
                return render(request, "groups.html",
                              {"message": message, "message2": message2, "joinedUsers": joinedUsers})
        # if it finds a matching username in the list of user objects, then don't add them to list, redirect to same page and show list of users

        if (g.SpotsAvailable <= 0):
            message = "This group is full please choose another one"
            group = list(Group.objects.all())
            return render(request, "groups.html", {"message": message, "groups": group})
        else:
            val = g.SpotsAvailable - 1  # if user hasn't joined group, decrease this

            g.SpotsAvailable = val
            g.save()
            g.Joined_Users.add(currentUser)
            g.save()
            groupReservation = GroupReservation(User=currentUser, Group=g)
            groupReservation.save()

            message = "You have successfully joined a group"
            message2 = "If you'd like join another group, please click the group tab on the navigation bar up top"
            message3 = "Here are other users in your group"
            return render(request, "groups.html",
                          {"message": message, "message2": message2, "message3": message3, "joinedUsers": joinedUsers})


class JoinedGroups(View):
    def get(self, request):
        currentUser = User.objects.get(UserName=request.session["username"])

        allGroups = Group.objects.all()  # every group
        currentUserGroups = []
        groupsToTemplate = []

        for i in allGroups:  # for each group in list of groups
            joinedUsers = i.Joined_Users.all()  # get list of users in that group
            for u in joinedUsers:
                if (u.UserName == currentUser.UserName):  # if our current user is in the group
                    currentUserGroups.append(i.Group_Id)  # add that group id to list of users groups


        if (len(currentUserGroups) == 0):  # if there are no joined groups, go join dummy
            message = "You have not joined a group yet please join one by clicking on the groups tab and selecting a group"
            return render(request, "joinedgroups.html", {"message": message})
        else:
            for i in currentUserGroups:
                g = Group.objects.get(
                    Group_Id=i)  # getting group object to put in new list so we can get details in template
                groupsToTemplate.append(g)

            message = "Here are the groups you are in: "
            return render(request, "joinedgroups.html", {"message": message, "joined_groups": groupsToTemplate})


class CreateGroupPage(View):
    def get(self, request):
        return render(request, "createGroupPage.html", {"errors": {"Just returning GET"}})

    def post(self, request):
        groupName = request.POST['Group_Name']
        sport = request.POST['Sport']
        maxCount = request.POST['Max_Players']
        groupDescription = request.POST['Group_Description']

        newGroup = Group(Sport=sport, Group_Description=groupDescription, Group_Name=groupName,
                         SpotsAvailable=maxCount)
        message_dict = []
        # error_dict = validate_user(user)
        valid = ["User successfully created"]

        try:
            newGroup.save()
        except IntegrityError:
            return render(request, "createGroupPage.html", "")
        else:
            return render(request, "groups.html", {"errors": valid})
        # else:
        # return render(request, "create_user.html", {"errors": error_dict})


class NotSignedIn(View):
    def get(self, request):
        return render(request, "notSignedIn.html", {})


@method_decorator(csrf_exempt, name='dispatch')
class GroupEventsPage(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['group_id']
        currGroup = Group.objects.get(Group_Id=id)
        users = currGroup.Joined_Users.all()
        groupPostArray = []
        allEvents = Event.objects.all()
        result = list(filter(lambda x: (x.Group == currGroup), allEvents))
        result = filter(lambda x: (x.Date > timezone.now()), result)

        try:
            groupPostArray = GroupPost.objects.filter(Group=currGroup)
        except GroupPost.DoesNotExist:
            return render(request, "groupEventsPage.html",
                          {"group": currGroup, "events": result, "users": users, "posts": groupPostArray})

        return render(request, "groupEventsPage.html",
                      {"group": currGroup, "events": result, "users": users, "posts": groupPostArray})

    def post(self, request, *args, **kwargs):
        id = kwargs['group_id']
        currentUser = User.objects.get(UserName=request.session["username"])
        currGroup = Group.objects.get(Group_Id=id)
        groupPostArray = []
        users = currGroup.Joined_Users.all()

        if 'createEvent' in request.POST:
            eventName = request.POST['Event_Name']
            location = request.POST['Location']
            dateTime = request.POST['dateTime']
            groupDescription = request.POST['Description']
            event = Event(Event_Name=eventName, Event_Description=groupDescription, Group=currGroup, Location=location,
                          Date=dateTime)
            event.save()

        allEvents = Event.objects.all()

        result = list(filter(lambda x: (x.Group == currGroup), allEvents))
        result = filter(lambda x: (x.Date > timezone.now()), result)


        if 'joinEvent' in request.POST:
            eventID = request.POST.get('joinEvent')
            currentUser = User.objects.get(UserName=request.session["username"])
            currentEvent = Event.objects.get(Event_Id=eventID)

            try:
                Reservation.objects.get(User=currentUser, Event=currentEvent)
            except Reservation.DoesNotExist:
                reservation = Reservation(User=currentUser, Event=currentEvent)
                reservation.save()

        if 'createGroupPost' in request.POST:
            title = request.POST['Title']
            groupBodyText = request.POST['GroupPostText']
            date = timezone.now()
            newPost = GroupPost(Creator=currentUser, Group=currGroup, Title=title, BodyText=groupBodyText, Date=date)

            newPost.save()

        return render(request, "groupEventsPage.html",
                      {"group": currGroup, "events": result, "users": users, "posts": groupPostArray})


class Events(View):
    def get(self, request, *args, **kwargs):
        currentUser = User.objects.get(UserName=request.session["username"])
        userReservationArr = Reservation.objects.filter(User=currentUser)
        eventArray = []

        groupReservations = GroupReservation.objects.filter(User=currentUser)
        groupArray = []

        groupEventsArr = []
        # get reservations, and get all the users groups
        for i in groupReservations:
            group = Group.objects.get(Group_Id=i.Group.Group_Id)
            groupArray.append(group)
        # using groupArray, get all events which belong to user
        for i in groupArray:
            groupEvents = Event.objects.filter(Group=i)
            for i in groupEvents:
                groupEventsArr.append(Event.objects.get(Event_Id=i.Event_Id))

        # using the datetime model field only show the upcoming events not past ones
        for i in userReservationArr:
            event = Event.objects.get(Event_Id=i.Event.Event_Id)
            if event.Date > timezone.now():
                eventArray.append(event)
        return render(request, "eventsPage.html", {"UserEvents": eventArray, "GroupsEvents": groupEventsArr})

    def post(self, request, *args, **kwargs):

        return render(request, "eventsPage.html", {})
