from django.urls import path
from . import manager_views

urlpatterns = [
    path('sign_in/', manager_views.online_manager_log_in),
    path('user_frozen/', manager_views.user_frozen),
    path('user_unfrozen/', manager_views.user_unfrozen),
    path('user_lost/', manager_views.user_lost),
    path('user_unlost/', manager_views.user_unlost),
    path('blacklist_add/', manager_views.blacklist_account_add),
    path('blacklist_query/', manager_views.blacklist_account_query),
    path('user_data_query/', manager_views.user_data_query),
    path('blacklist_delet/', manager_views.blacklist_account_delet),
]