from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
from random import randint
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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


def profile(request):
    return render(request, "lacrosse_quiz/profile.html", {
        "articles": util.list_articles()
    })


def register(request):
    if request.method == "POST":
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
        login(request, user)
        profile = Profile()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("allposts"))
    else:
        return render(request, "lacrosse_quiz/register.html")


def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("allposts"))
        else:
            return render(request, "lacrosse_quiz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lacrosse_quiz/login.html")


def question_view(request, question_id):
    question = Question.objects.get(id=question_id)
    choices = question.choices.split(",")
    if request.method == 'POST':
        answer = int(request.POST['answer'])
        user_answer = UserAnswer(
            user=request.user, question=question, answer=answer)
        user_answer.save()
        next_question_id = question_id + 1
        if next_question_id <= Question.objects.count():
            return redirect('question', question_id=next_question_id)
        else:
            return redirect('answer')
    context = {
        'question': question,
        'choices': choices,
    }
    return render(request, 'question.html', context)


def answer_view(request):
    user_answers = UserAnswer.objects.filter(user=request.user)
    questions = Question.objects.all()
    results = []
    for question in questions:
        user_answer = user_answers.filter(question=question).first()
        if user_answer is None:
            results.append(('Unanswered', question))
        elif user_answer.answer == question.correct_answer:
            results.append(('Correct', question))
        else:
            results.append(('Incorrect', question))
    context = {
        'results': results,
    }
    return render(request, 'answer.html', context)
