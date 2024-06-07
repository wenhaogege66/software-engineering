from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import sys_manage, online_user, BlackList



def query_blacklist(request, sys_manager_id):
    admin = get_object_or_404(sys_manage, sys_manager_id=sys_manager_id)
    blacklisted_users = BlackList.objects.filter(admin=admin).values('user_id', 'user__user_name')
    return JsonResponse(list(blacklisted_users), safe=False)


def blacklist_account(request, sys_manager_id, user_id):
    admin = get_object_or_404(sys_manage, sys_manager_id=sys_manager_id)
    user = get_object_or_404(online_user, user_id=user_id)

    if not BlackList.objects.filter(admin=admin, user=user).exists():
        BlackList.objects.create(admin=admin, user=user)
        user.is_blacklisted = True
        user.save()
    return JsonResponse({'status': 'success'})


def cancel_black_account(request, sys_manager_id, user_id):
    admin = get_object_or_404(sys_manage, sys_manager_id=sys_manager_id)
    user = get_object_or_404(online_user, user_id=user_id)

    blacklist_entry = BlackList.objects.filter(admin=admin, user=user)
    if blacklist_entry.exists():
        blacklist_entry.delete()
        user.is_blacklisted = False
        user.save()
    return JsonResponse({'status': 'success'})