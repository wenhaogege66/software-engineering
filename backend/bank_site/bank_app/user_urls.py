# 自己建的
from django.urls import path

from . import user_views

urlpatterns = [
    path('sign_up/', user_views.user_add),
    path('sign_in/', user_views.user_log_in),
    path('change_password/', user_views.user_change_password),
    path('list_cards/', user_views.list_cards),
    path('bind_card', user_views.bind_card),
    path('card_lost/', user_views.card_lost),
    path('queryAccount/', user_views.online_bank_query_accounts),
]

