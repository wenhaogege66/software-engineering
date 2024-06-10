from django.urls import path
from . import manager_views

urlpatterns = [
    path('query_blacklist/<int:sys_manager_id>/', manager_views.query_blacklist, name='query_blacklist'),
    path('blacklist_account/<int:sys_manager_id>/<int:user_id>/', manager_views.blacklist_account, name='blacklist_account'),
    path('cancel_black_account/<int:sys_manager_id>/<int:user_id>/', manager_views.cancel_black_account, name='cancel_black_account'),
]