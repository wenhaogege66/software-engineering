from django.urls import path
from . import cashier_views

urlpatterns = [
    path('add/', cashier_views.cashier_add),
    path('queryAccount/', cashier_views.cashier_query_account),
    path('all-deposits/', cashier_views.cashier_all_deposits),
    path('demand-deposit/', cashier_views.cashier_demand_deposit),
    path('time-deposit/', cashier_views.cashier_time_deposit),
    path('total-deposit/', cashier_views.cashier_total_deposit),
    path('all-withdrawls/', cashier_views.cashier_all_withdrawls),
    path('withdrawl/', cashier_views.cashier_withdrawl),
    path('all-transfers/', cashier_views.cashier_all_transfers),
    path('transfer/', cashier_views.cashier_transfer),
    path('all-records/', cashier_views.cashier_all_records),

    path('unfreeze/', cashier_views.cashier_unfreeze, name = 'all-cashier_unfreeze'),
    path('freeze/', cashier_views.cashier_freeze, name = 'cashier_freeze'),
    path('reportloss/', cashier_views.cashier_reportloss, name = 'cashier_reportloss'),
    path('reissue/', cashier_views.cashier_reissue, name = 'cashier_reissue'),
]