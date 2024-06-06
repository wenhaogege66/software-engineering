# 自己建的
from django.urls import path

from bank_app import user_views

urlpatterns = [
    path('sign_in/', user_views.user_add),
    # path('sign_up/', user_views.QueryStudent.as_view()),
    path('queryAccount/', user_views.online_bank_query_accounts),
]

