from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import sys_manage, online_user, BlackList
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers



@csrf_exempt
def manager_log_in(request):
    if request.method == 'POST':
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))
        # print('看看filter_online_user:{}'.format(filter_online_user))
        if (filter_online_user.exists()):
            # 用户存在开始对照密码
            cur_user =  online_user.objects.get(user_name = data.get('user_name'))
            if(data.get('password') == cur_user.password):
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                # print(new_user)
                return JsonResponse({"error": "password is wrong",'state': False}, status=200)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)

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