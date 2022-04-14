"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Group3Capstone.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('dashboard/', Dashboard.as_view()),
    path('account/', Account.as_view()),
    path('createAccount/', CreateAccountsPage.as_view()),
    path('groups/', Groups.as_view()),
    path('joinedgroups/', JoinedGroups.as_view()),
    path('editaccount/', EditAccountPage.as_view()),
    path('createGroupPage/', CreateGroupPage.as_view()),
    path('notSignedIn/', NotSignedIn.as_view()),
]