from django.urls import path

from . import views


app_name = "account"

urlpatterns = [
    path("home", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),

]