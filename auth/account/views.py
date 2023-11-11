from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model

from custom_user.models import User
from .token import account_activation_token  
from .forms import SignUpForm, SignInForm


def home(request):
    return HttpResponse("Home page")

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # save form in memory not in db
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email"
            message = render_to_string("account/acc_active_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return HttpResponse("Please confirm your email account")
            # password1 = form.cleaned_data.get("password1")
            # password2 = form.cleaned_data.get("password2")

            # if password1 != password2:
            #     messages.error(request, "Passwords do not match")
            # else:
            #     user.save()
            #     return redirect("account:signin")
        
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


def signout(request):

    logout(request)

    return redirect("account:signin")

