from django.urls import path, re_path

from . import views


app_name = "account"

urlpatterns = [
    path("home", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),

    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate,
        name='activate'
    ),

]