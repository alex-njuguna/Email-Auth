from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from custom_user.models import User
from .forms import SignUpForm, SignInForm


def home(request):
    return HttpResponse("Home page")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")

            if password1 != password2:
                messages.error(request, "Passwords do not match")
            else:
                user.save()
                return redirect("account:signin")
        
    form = SignUpForm()

    return render(request, "account/signup.html", {
        "form": form,
        "title": "sign up"
    })


def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)

        print(form)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, email=email, password=password)

            print(user)

            if user is not None:
                login(request, user)
                messages.success(request, "Signed in")
                return redirect("account:home")
            else:
                messages.error(request, "Incorrect email or password!")
        
    form = SignInForm()

    return render(request, "account/signin.html", {
        "title": "sign in",
        "form": form
    })

