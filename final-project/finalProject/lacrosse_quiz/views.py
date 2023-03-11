from django.shortcuts import render, redirect
from .models import Question, UserAnswer
from markdown2 import markdown
from . import util
from random import randint


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


def index(request):
    # when a pth is called that references thius view,
    # the function returns and renders the index.html file t
    # hat is in the lacrosse_quiz app path.
    return render(request, "lacrosse_quiz/index.html",
                  {
                      "article": util.list_articles()
                  })


def article(request, title):
    content = util.get_article(title.strip())
    if content == None:
        content = "## Page was not found"
    content = markdown(content)
    return render(request, "lacrosse_quiz/articles.html", {'content': content, 'title': title})
