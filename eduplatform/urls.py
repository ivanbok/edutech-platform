from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("registerstudent", views.registerstudent, name="registerstudent"),
    path("registertutor", views.registertutor, name="registertutor"),
    path("addmcqquestion", views.addmcqquestion, name="addmcqquestion")
]
