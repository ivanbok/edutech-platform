from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
import datetime
import json
import requests

from .models import *

########################################################################################################
## Account Management ##################################################################################
########################################################################################################

def index(request):
    return render(request, "eduplatform/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "eduplatform/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "eduplatform/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    return render(request, "eduplatform/register.html")
    
def registerstudent(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        level = request.POST["level"]
        levelObject = Levels.objects.get(level=level)

        # Ensure password matches confirmation 
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "eduplatform/registerstudent.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password,\
                first_name=first_name, last_name=last_name, is_active = True, is_student = True, is_tutor = False)
            user.save()
            student = Students.objects.create(user=user, level=levelObject)
            student.save()
        except IntegrityError:
            return render(request, "eduplatform/registerstudent.html", {
                "message": "Username already taken."
            })
        standardUser = StandardUser.objects.create(user=user)
        standardUser.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        levelsQuery = Levels.objects.all()
        levelsList = []
        for levelsObject in levelsQuery:
            levelsList.append(levelsObject.level)
        return render(request, "eduplatform/registerstudent.html", {
            "levelsList": levelsList
        })
    
def registertutor(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "eduplatform/registertutor.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password,\
                first_name=first_name, last_name=last_name, is_active = True, is_student = False, is_tutor = True)
            user.save()
        except IntegrityError:
            return render(request, "eduplatform/registertutor.html", {
                "message": "Username already taken."
            })
        standardUser = StandardUser.objects.create(user=user)
        standardUser.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "eduplatform/registertutor.html")

########################################################################################################
## Questions Creation ##################################################################################
########################################################################################################

def addmcqquestion(request):
    if request.method == "POST":
        pass
    else:
        # Get List of Subjects
        subjectsQuery = Subjects.objects.all()
        subjectsList = []
        for subjectsObject in subjectsQuery:
            subjectsList.append(subjectsObject.subject)
        # Get List of Levels
        levelsQuery = Levels.objects.all()
        levelsList = []
        for levelsObject in levelsQuery:
            levelsList.append(levelsObject.level)
        return render(request, "eduplatform/addmcqquestion.html", {
            "subjectsList": subjectsList,
            "levelsList": levelsList
        })