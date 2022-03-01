from Group3Capstone.models import User, AccountType
from Group3Capstone.classes.accounts import Accounts

class Admin(Accounts):
    def __createAccount__(self, username, email, password, type):
        if not username or not email or not password or not type:
            raise TypeError("Invalid input")
        accountExists = False
        try:
            a = User.objects.get(email=email)
            accountExists = True
        except:
            newAcc = None
            if type=='A':
                newAcc = Admin.objects.create(username=username, email=email, password=password, type=AccountType.Administrator)
            else:
                raise TypeError("Invalid input")

            newAcc.save()
            return newAcc

        if accountExists:
            raise ValueError("Account exists already")