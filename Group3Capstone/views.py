from sqlite3 import IntegrityError

from django.shortcuts import render, redirect
from django.views import View
from .models import User  # create and add user models
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
            return render(request, "home.html", {"message": "Incorrect UserName/Password"})
        elif badPassword:
            return render(request, "home.html", {"message": "Incorrect UserName/Password"})
        else:
            request.session["username"] = m.UserName
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        # if not request.session.get("UserName"):
        #     return redirect("/")
        # u = User.objects.get(UserName=request.session['UserName'])

        # u = User.objects.get(UserName=request.get['UserName'])
        uTest = request.session["username"]

        print("\n", uTest, "\n")

        return render(request, "dashboard.html", {"username": uTest})


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
        u = User.objects.get(username=request.session["username"])
        return render(request, "account.html",
                      {"User_ID": u.User_ID, "User_Password": u.User_Password, "User_FName": u.User_FName,
                       "User_LName": u.User_LName,
                       "User_DOB": u.User_DOB, "User_Address": u.User_Address, "User_Phone": u.User_Phone,
                       "UserName": u.UserName, "User_Email": u.User_Email, "Account_type": u.Account_type})
