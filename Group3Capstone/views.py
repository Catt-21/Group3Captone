from sqlite3 import IntegrityError

from django.shortcuts import render, redirect
from django.views import View
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

        print("\n" + uTest + "\n")
        print("\n" + u.User_FName)

        sports = list(Sport.objects.all().values())

        return render(request, "dashboard.html", {"username": uTest, "sport": sports, "user": u})


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
        print("\n", group)

        return render(request, "groups.html", {"user": u, "groups": group})

    def post(self, request):
        u = request.session["username"]
        currentUser = User.objects.get(UserName=request.session["username"])  # setting up user objects

        groupJoined = request.POST["name"]  # group ID
        print("\n", groupJoined)  # to confirm in console that group was sent to post properly

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
            print("\n", val)
            g.SpotsAvailable = val
            g.save()
            g.Joined_Users.add(currentUser)
            g.save()
            print(g.SpotsAvailable)
            print(list(g.Joined_Users.all()))

            for i in joinedUsers:
                print(
                    i.User_FName)  # using 'i' to iterate through the list, can call whatever value using i because i is the object that's in the list

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
            print(i.Sport)
            joinedUsers = i.Joined_Users.all()  # get list of users in that group
            for u in joinedUsers:
                if (u.UserName == currentUser.UserName):  # if our current user is in the group
                    print("This person is in a group")
                    currentUserGroups.append(i.Group_Id)  # add that group id to list of users groups

        print(currentUserGroups)
        print(len(currentUserGroups))

        if (len(currentUserGroups) == 0):  # if there are no joined groups, go join dummy
            message = "You have not joined a group yet please join one by clicking on the groups tab and selecting a group"
            return render(request, "joinedgroups.html", {"message": message})
        else:
            for i in currentUserGroups:
                g = Group.objects.get(
                    Group_Id=i)  # getting group object to put in new list so we can get details in template
                print(g.Sport.Sport_Name)
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
        sportObj = Sport(Sport_Name=sport)

        sportObj.save()

        newGroup = Group(Sport=sportObj,Group_Description=groupDescription, Group_Name=groupName, SpotsAvailable=maxCount)
        message_dict = []
        # error_dict = validate_user(user)
        valid = ["User successfully created"]

        try:
            newGroup.save()
        except IntegrityError:
            return render(request, "createGroupPage.html", "")
        else:
            return render(request, "home.html", {"errors": valid})
        # else:
        # return render(request, "create_user.html", {"errors": error_dict})
class NotSignedIn(View):
    def get(self, request):
        return render(request, "notSignedIn.html", {})
