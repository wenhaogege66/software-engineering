# 自己建的
from django.urls import path
from . import views

urlpatterns = [
    path('/bind', views.QueryStudent.as_view()),
    path('/loss', views.QueryStudent.as_view()),
    path('/list_cards',views.QueryStudent)
]

