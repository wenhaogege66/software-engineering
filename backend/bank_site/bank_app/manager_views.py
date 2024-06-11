from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import sys_manage, online_user, BlackList

from rest_framework.views import APIView
from rest_framework.response import Response

import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


@csrf_exempt
def online_manager_log_in(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        # print("文豪说看看这个密码")
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        print('看看account:{}'.format(data.get('account')))
        filter_online_user = online_bank_manager.objects.filter(account=data.get('account'))
        # print('看看filter_online_user:{}'.format(filter_online_user.account))
        if filter_online_user.exists():
            # 用户存在开始对照密码
            cur_manager =  online_bank_manager.objects.get(account=data.get('account'))
            print(f"文豪说看看这个密码: {cur_manager.password}")
            if data.get('password') == cur_manager.password:
                return_data = {'id': cur_manager.online_bank_manager_id, 'state': True}
                return JsonResponse(return_data, status=200)
            else:
                # print("看看这里")
                # print(new_user)
                return JsonResponse({"error": "password is wrong",'state': False}, status=400)
        else:
            return JsonResponse({"error": "Manager don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)

@csrf_exempt
def blacklist_account_add(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        # print("文豪说看看这个密码")
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_manager = online_bank_manager.objects.filter(account=data.get('manager_name'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_manager.exists():
            # 用户存在开始对照密码
            cur_manager =  online_bank_manager.objects.get(account=data.get('manager_name'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))
            print('看看filter_online_manager:{}'.format(cur_manager.account))
            
            if filter_online_user.exists():
                cur_user =  online_user.objects.get(user_name=data.get('user_name'))
                print('看看filter_online_user:{}'.format(cur_user.user_name))
                if cur_user.is_blacklisted == False:
                    if not BlackList.objects.filter(user_id=cur_user.user_id).exists():
                        print("我日了个蛋")
                        cur_black = BlackList(user_id=cur_user, online_bank_manager_id=cur_manager)
                        cur_black.save()
                        cur_user.is_blacklisted=True
                        cur_user.save()
                    return_data = {'state': True}
                    return JsonResponse(return_data, status=200)
                else:
                    # print("看看这里")
                    # print(new_user)
                    return JsonResponse({"error": "already in black",'state': False}, status=400)
            else:
                return JsonResponse({"error": "User don't exist",'state': False}, status=403)
        else:
            return JsonResponse({"error": "Manager don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def user_frozen(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_id=data.get('user_id'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_user.exists():
            cur_user =  online_user.objects.get(user_id=data.get('user_id'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))            
            print('看看filter_online_user:{}'.format(cur_user.user_name))
            if cur_user.is_frozen == False:
                cur_user.is_frozen=True
                cur_user.save()
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "已经冻结了，宝贝",'state': False}, status=403)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def user_unfrozen(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_id=data.get('user_id'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_user.exists():
            cur_user =  online_user.objects.get(user_id=data.get('user_id'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))            
            print('看看filter_online_user:{}'.format(cur_user.user_name))
            if cur_user.is_frozen == True:
                cur_user.is_frozen=False
                cur_user.save()
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "你逗我呢，宝贝",'state': False}, status=403)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def user_lost(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_id=data.get('user_id'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_user.exists():
            cur_user =  online_user.objects.get(user_id=data.get('user_id'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))            
            print('看看filter_online_user:{}'.format(cur_user.user_name))
            if cur_user.is_lost == False:
                cur_user.is_lost=True
                cur_user.save()
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "已经挂失了，宝贝",'state': False}, status=403)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def user_unlost(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_id=data.get('user_id'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_user.exists():
            cur_user =  online_user.objects.get(user_id=data.get('user_id'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))            
            print('看看filter_online_user:{}'.format(cur_user.user_name))
            if cur_user.is_lost == True:
                cur_user.is_lost=False
                cur_user.save()
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "别闹，宝贝",'state': False}, status=403)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def user_lost(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_id=data.get('user_id'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_user.exists():
            cur_user =  online_user.objects.get(user_id=data.get('user_id'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))            
            print('看看filter_online_user:{}'.format(cur_user.user_name))
            if cur_user.is_lost == False:
                cur_user.is_lost=True
                cur_user.save()
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "已经挂失了，宝贝",'state': False}, status=403)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def user_unlost(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_id=data.get('user_id'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_user.exists():
            cur_user =  online_user.objects.get(user_id=data.get('user_id'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))            
            print('看看filter_online_user:{}'.format(cur_user.user_name))
            if cur_user.is_lost == True:
                cur_user.is_lost=False
                cur_user.save()
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "别闹，宝贝",'state': False}, status=403)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def blacklist_account_delet(request):
    # print("文豪说看看这个密码")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_id=data.get('user_id'))
        # print('看看filter_online_manager:{}'.format(filter_online_manager.account))
        if filter_online_user.exists():
            # 用户存在开始对照密码
            cur_user =  online_user.objects.get(user_id=data.get('user_id'))
            filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))            
            print('看看filter_online_user:{}'.format(cur_user.user_name))
            if cur_user.is_blacklisted == True:
                if  BlackList.objects.filter(user_id=cur_user.user_id).exists():
                    cur_black = BlackList.objects.get(user_id=cur_user)
                    cur_black.delete()
                    cur_user.is_blacklisted=False
                    cur_user.save()
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "Blacklist don't exist",'state': False}, status=403)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
    
def blacklist_account_query(request):
    if request.method == 'GET':
        filter_blacks = online_user.objects.filter(is_blacklisted = True)
        # if filter_users.exists():
        #     filter_user = filter_users[0]
        # else:
        #     return JsonResponse({"error": "User not found"}, status=404)
        # filter_cards = filter_user.accounts.all()
        results = [{
            "user_name": black.user_name,
            "phone_num": black.phone_num,
            "id_card": black.identity_card,
            "user_id": black.user_id,
        } for black in filter_blacks]
        # for res in results:
        #     print(res)
        return JsonResponse(results, status=200,safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
def user_data_query(request):
    if request.method == 'GET':
        filter_blacks = online_user.objects.all()
        results = [{
            "user_name": black.user_name,
            "phone_num": black.phone_num,
            "id_card": black.identity_card,
            "user_id": black.user_id,
            "is_frozen": black.is_frozen,
            "is_lost": black.is_lost,
        } for black in filter_blacks]
        # for res in results:
        #     print(res)
        return JsonResponse(results, status=200,safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)



def cancel_black_account(request, sys_manager_id, user_id):
    admin = get_object_or_404(online_bank_manager, online_bank_manager_id=sys_manager_id)
    user = get_object_or_404(online_user, user_id=user_id)

    blacklist_entry = BlackList.objects.filter(admin=admin, user=user)
    if blacklist_entry.exists():
        blacklist_entry.delete()
        user.is_blacklisted = False
        user.save()
    return JsonResponse({'status': 'success'})