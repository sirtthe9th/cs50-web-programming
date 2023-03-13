from django.urls import path
# import the views from the lacrosse_quiz app
from .views import index, article, login_view, register, profile

# URL pattern for the lacrosse_quiz app, not the project.
urlpatterns = [
    # when the base path is visited, django will call the function in views called index
    path("", index, name="index"),
    path("article/<title>", article, name="article"),
    path("login", login_view, name="login"),
    path("register", register, name="register"),
    path("u/<username>", profile, name="profile"),
]
