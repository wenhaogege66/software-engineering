from rest_framework.views import APIView
from rest_framework.response import Response

import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


def get_user_info(request):
    if request.method == 'GET':
        filter_users = online_user.objects.filter(user_id=request.GET.get('user_id'))
        if filter_users.exists():
            filter_user = filter_users[0]
        else:
            return JsonResponse({"error": "User not found"}, status=404)
        result = {
            "user_name": filter_user.user_name,
            "phone_num": filter_user.phone_num
        }
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def list_cards(request):
    # user_id -> List[Card]
    if request.method == 'GET':
        filter_users = online_user.objects.filter(user_id=request.GET.get('user_id'))
        if filter_users.exists():
            filter_user = filter_users[0]
        else:
            return JsonResponse({"error": "User not found"}, status=404)
        filter_cards = filter_user.accounts.all()
        results = [{
            "account_id": card.account_id,
            "card_type": card.card_type,
            "balance": card.balance,
            "is_frozen": card.is_frozen,
            "is_lost": card.is_lost
        } for card in filter_cards]
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# @csrf_exempt
# def bind_cards(request):
#     if request.method == 'POST':
#         data = json.loads(request.body.decode('utf-8'))
#         print(f'获取到的post数据为：{data}')
#         filter_accounts = account.objects.filter(identity_card=data.get('identity_card'), phone_num=data.get('phone_num'))
#         filter_users = online_user.objects.filter(identity_card=data.get('identity_card'), phone_num=data.get('phone_num'))
#         if filter_accounts.exists() and filter_users.exists():
#             filter_accounts.update(user_id=filter_users[0].user_id)
#             return_data = {"success": "The auto-binding is successful", 'state': True}
#             return JsonResponse(return_data, status=200)
#         else:
#             return JsonResponse({"success": "No accounts now for this user", 'state': False}, status=200)
#     elif request.method == 'OPTION':
#         return JsonResponse({"success": "OPTION operation"}, status=200)
#     else:
#         return JsonResponse({"error": "Method not allowed", 'state': True}, status=405)


@csrf_exempt
def card_lost(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        lost_accounts = account.objects.filter(account_id=data.get('account_id'))
        if not lost_accounts.exists():
            return JsonResponse({"error": "Account not found", 'state': False}, status=400)
        lost_account = lost_accounts[0]
        if lost_account.password == data.get('password'):
            if lost_account.is_lost == data.get('to_lost'):
                return JsonResponse({"error": "The card has been lost", 'state': False}, status=400)
            lost_accounts.update(is_lost=data.get('to_lost'))
            return_data = {'state': True}
            return JsonResponse(return_data, status=200)
        else:
            return JsonResponse({"error": "Password is Wrong", 'state': False}, status=400)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed", 'state': True}, status=405)

#
# def online_bank_query_accounts(request):
#     if request.method == 'GET':
#         filter_accounts = account.objects.filter(account_id=request.GET.get('accountID'))[0]
#         account_data = {}
#         account_data['id'] = filter_accounts.account_id
#         account_data['password'] = filter_accounts.password
#         account_data['identity_card'] = filter_accounts.identity_card.identity_card
#         account_data['balance'] = filter_accounts.balance
#         account_data['currentDeposit'] = filter_accounts.current_deposit
#         account_data['uncreditedDeposit'] = filter_accounts.uncredited_deposit
#         account_data['isFrozen'] = filter_accounts.is_frozen
#         account_data['isLost'] = filter_accounts.is_lost
#         return JsonResponse(account_data, safe=False)
#     else:
#         return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def user_add(request):
    if request.method == 'POST':
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(identity_card=data.get('identity_card'))
        # print('看看filter_online_user:{}'.format(filter_online_user))
        if not filter_online_user.exists():
            if online_user.objects.count == 0:
                cur_id = 1
                new_user = online_user(
                    user_id = cur_id,
                    user_name = data.get('user_name'),
                    password = data.get('password'),
                    identity_card = data.get('identity_card'),
                    phone_num = data.get('phone_num'),
                    is_frozen=False,
                    is_lost=False
                )
                new_user.save()
            else:
                new_user = online_user(
                    user_name = data.get('user_name'),
                    password = data.get('password'),
                    identity_card = data.get('identity_card'),
                    phone_num = data.get('phone_num'),
                    is_frozen=False,
                    is_lost=False
                )
                new_user.save()
            # 注册成功后自动开始相关联的卡片（账户绑定）
            filter_accounts = account.objects.filter(identity_card=data.get('identity_card'), phone_num=data.get('phone_num'))
            print(f"看看这个{filter_accounts}")
            if filter_accounts.exists():
                filter_accounts.update(user_id=new_user.user_id)
                return_data = {"success": "The auto-binding is successful", 'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"success": "No accounts now for this user", 'state': True}, status=200)
        # # print(new_user)
            # return_data = {'state': True}
            # return JsonResponse(return_data, status=200)
        else:
            return JsonResponse({"error": "User with this identity_card has been exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)


@csrf_exempt
def user_log_in(request):
    if request.method == 'POST':
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))
        # print('看看filter_online_user:{}'.format(filter_online_user))
        if filter_online_user.exists():
            if filter_online_user[0].is_blacklisted:
                return JsonResponse({"error": "this user is blacklisted", 'state': False}, status=400)
            if filter_online_user[0].is_frozen:
                return JsonResponse({"error": "this user is frozen", 'state': False}, status=400)
            # 用户存在开始对照密码
            cur_user = online_user.objects.get(user_name = data.get('user_name'))
            print(f"文豪说看看这个密码: {cur_user.password}")
            if data.get('password') == cur_user.password:
                return_data = {'user_id': cur_user.user_id, 'state': True}
                return JsonResponse(return_data, status=200)
            else:
                print("看看这里")
                # print(new_user)
                return JsonResponse({"error": "password is wrong",'state': False}, status=400)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)
    
@csrf_exempt
def user_change_password(request):
    if request.method == 'POST':
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        print('看看data:{}'.format(data))
        filter_online_user = online_user.objects.filter(user_name=data.get('user_name'))
        # print('看看filter_online_user:{}'.format(filter_online_user))
        if (filter_online_user.exists()):
            # 用户存在开始对照密码
            cur_user =  online_user.objects.get(user_name = data.get('user_name'))
            if(data.get('identity_card') == cur_user.identity_card and data.get('phone_num') == cur_user.phone_num):
                online_user.objects.filter(user_name = data.get('user_name')).update(password = data.get('new_password'))
                return_data = {'state': True}
                return JsonResponse(return_data, status=200)
            else:
                return JsonResponse({"error": "information is wrong",'state': False}, status=400)
        else:
            return JsonResponse({"error": "User don't exist",'state': False}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed",'state': True}, status=405)


def user_account_all_records(request):
    # 一个疑问，在网页中请求某个账户的所有记录时，需不需要提供账户所属互联网用户的id？如果不需要的话会不会有安全问题？
    if request.method == 'GET':
        if (request.GET.get('account_id') != ''
                and not account.objects.filter(account_id=request.GET.get('account_id')).exists()):
            # print("Invalid account_id")
            return JsonResponse({"error": "查询的账户不存在"}, status=403)
        else:
            records = []
            record_type = int(request.GET.get('record_type'))
            if record_type == 1:
                filter_deposit_records = deposit_record.objects.filter(account_id=int(request.GET.get('account_id')))
                if filter_deposit_records.exists():
                    records =[{
                        "deposit_record_id": record.deposit_record_id,
                        "account_id": record.account_id,
                        "deposit_type": record.deposit_type,
                        "auto_renew_status": record.auto_renew_status,
                        "deposit_start_date": record.deposit_start_date,
                        "deposit_end_date": record.deposit_end_date,
                        "deposit_amount": record.deposit_amount,
                        "cashier_id": record.cashier_id,
                    } for record in filter_deposit_records]
            elif record_type == 2:
                filter_withdrawal_records = withdrawal_record.objects.filter(account_id=int(request.GET.get('account_id')))
                if filter_withdrawal_records.exists():
                    records = [{
                        "withdrawal_record_id": record.withdrawal_record_id,
                        "account_id": record.account_id,
                        "withdrawal_date": record.withdrawal_date,
                        "withdrawal_amount": record.withdrawal_amount,
                        "cashier_id": record.cashier_id,
                    } for record in filter_withdrawal_records]
            elif record_type == 3:
                filter_transfer_records = transfer_record.objects.filter(account_out_id=int(request.GET.get('account_id')))
                if filter_transfer_records.exists():
                    records = [{
                        "transfer_record_id": record.transfer_record_id,
                        "account_in_id": record.account_in_id,
                        "account_out_id": record.account_out_id,
                        "transfer_date": record.transfer_date,
                        "transfer_amount": record.transfer_amount,
                        "cashier_id": record.cashier_id,
                    } for record in filter_transfer_records]
            else:
                return JsonResponse({"error":"Wrong record type"},status=400)
            print(f"look records: {records}")
            return JsonResponse(records, safe=False, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 转账
@csrf_exempt
def user_account_transfer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if data.get('transfer_amount') <= 0:
            return JsonResponse({"error": "转账金额错误"}, status=403)
        filter_out_account = account.objects.filter(account_id=int(data.get('account_out_id')), password=data.get('password'))
        filter_in_account = account.objects.filter(account_id=int(data.get('account_in_id')))
        if not filter_in_account.exists():
            return JsonResponse({"error": "接收转账用户不存在"}, status=403)
        if not filter_out_account.exists():
            return JsonResponse({"error": "转出账户不存在或密码错误"}, status=403)
        filter_in_account = filter_in_account.first()
        filter_out_account = filter_out_account.first()
        if filter_out_account.is_frozen or filter_out_account.is_lost:
            return JsonResponse({"error": "转出账户被挂失/冻结"}, status=403)
        if filter_in_account.is_frozen or filter_in_account.is_lost:
            return JsonResponse({"error": "转入账户被挂失/冻结"}, status=403)
        # 判断用户存款是否满足取出条件
        if filter_out_account.uncredited_deposit >= float(data.get('transfer_amount')):
            # 更新用户存款情况
            filter_out_account.uncredited_deposit -= data.get('transfer_amount')
            filter_out_account.balance -= data.get('transfer_amount')
            filter_out_account.save()
            filter_in_account.uncredited_deposit += data.get('transfer_amount')
            filter_in_account.balance += data.get('transfer_amount')
            filter_in_account.save()
            # 更新取款记录
            new_transfer_record = transfer_record(
                account_in_id=data.get('account_in_id'),
                account_out_id=data.get('account_out_id'),
                # --此处存疑--
                transfer_date=datetime.datetime.now(),
                # -----
                transfer_amount=data.get('transfer_amount'),
                cashier_id=0 # 0 作为默认互联网转账的cashier_id
            )
            new_transfer_record.save()
            return JsonResponse({"success": "successful operation"}, status=200)
        else:
            return JsonResponse({"error": "转出账户余额不足"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

# 例子
# class QueryStudent(APIView):
#     @staticmethod
#     def get(request):
#         """
#         """
#         req = request.query_params.dict()#前端给的json包数据
#         student_name = req["student_name"]

#         student_id = Student.objects.filter(student_name=student_name).values("student_id")#提取数据表中数据
#         return Response(student_id)#返回数据，这里由于提取数据表中数据直接就是jason格式所以可以直接传，其他的需要转为json格式

#     @staticmethod
#     def post(request):
#         """
#         """
#         req = request.data#前端给的json包数据
#         student_id = req["student_id"]
#         student_name = req["student_name"]

#         Student(student_id=student_id,student_name=student_name).save()#保存数据
#         print('收到:id为{},name为{}'.format(student_id,student_name))

#         return Response()#不需要返回数据
