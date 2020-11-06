"""chipscoco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from shrimp import views as shrimp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shrimp.Home.as_view(),name="home"),
    path('register/', shrimp.Register.as_view(),name="register"),
    path('api/sms/', shrimp.Sms.as_view(),name="sms"),
    path('login/', shrimp.Login.as_view(),name="login"),
    path('question/', shrimp.Question.as_view(),name="problem"),
    re_path('question/(\d+)/', shrimp.QuestionPage.as_view(),name="question"),
    re_path('question/(\d+)/answer/(\d+)/', shrimp.AnswerPage.as_view(),name="answerpage"),
    re_path('people/(\w+)/', shrimp.Profile.as_view(),name="people"),
    path('answer/', shrimp.Answer.as_view(),name="answer"),
    path('comment/', shrimp.Comment.as_view(),name="comment"),
    path('search/', shrimp.Search.as_view(),name="search"),


]
