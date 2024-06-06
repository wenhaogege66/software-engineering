from django.urls import path
from . import manager_views

urlpatterns = [
    path('all-cashier/', manager_views.all_cashiers, name = 'all-cashiers'),
    path('add/', manager_views.add_cashier, name = 'add_cashier'),
    path('delete/', manager_views.delete_cashier, name = 'delete_cashier'),
    path('modify-base/', manager_views.modify_cashier, name = 'modify_cashier'),
    path('modify-authority/', manager_views.modify_authority, name = 'modify_authority')
]