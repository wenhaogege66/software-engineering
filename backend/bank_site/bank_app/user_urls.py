# 自己建的
from django.urls import path

from bank_app import user_views

urlpatterns = [
    path('sign_up/', user_views.user_add),
    path('sign_in/', user_views.user_log_in),
    path('change_password/', user_views.user_change_password),
    path('queryAccount/', user_views.online_bank_query_accounts),
]

