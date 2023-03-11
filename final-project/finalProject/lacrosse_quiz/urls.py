from django.urls import path
# import the views from the lacrosse_quiz app
from .views import index, question_view, answer_view

# URL pattern for the lacrosse_quiz app, not the project.
urlpatterns = [
    # when the base path is visited, django will call the function in views called index
    path("", index, name="index"),
    path('answer/', answer_view, name='answer'),
    path('question/', question_view, name='question'),
]
