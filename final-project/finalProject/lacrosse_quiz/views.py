from django.shortcuts import render
from markdown2 import markdown
from . import util
from random import randint
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User


def index(request):
    # when a pth is called that references thius view,
    # the function returns and renders the index.html file t
    # hat is in the lacrosse_quiz app path.
    return render(request, "lacrosse_quiz/index.html", {
        "articles": util.list_articles()
    })


def article(request, title):
    content = util.get_article(title.strip())
    if content == None:
        content = "## Page was not found"
    content = markdown(content)
    return render(request, "lacrosse_quiz/articles.html", {'content': content, 'title': title})


def profile(request, username):
    return render(request, "lacrosse_quiz/profile.html", {
        "username": username
    })


def register(request):
    if request.method == "POST":
        if not request.POST["username"] or request.POST["email"] is "":
            return render(request, "lacrosse_quiz/register.html", {
                "message": "Please complete all fields."
            })
        else:
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                return render(request, "lacrosse_quiz/register.html", {
                    "message": "Passwords must match."
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "lacrosse_quiz/register.html", {
                    "message": "Username already taken."
                })
            return HttpResponseRedirect(reverse("lacrosse_quiz/index.html", {
                "message": ""
            }))
    else:
        return render(request, "lacrosse_quiz/register.html", {
            "message": ""
        })


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
            return render(request, "lacrosse_quiz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lacrosse_quiz/login.html")
