import json
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers


@csrf_exempt
def cashier_add(request):
    if request.method == 'POST':
        # 将请求体中的数据转化为json格式
        data = json.loads(request.body.decode('utf-8'))
        filter_online_user = online_user.objects.filter(identity_card=data.get('identity_card'))
        if filter_online_user.exists():
            filter_account = account.objects.filter(identity_card=filter_online_user[0])
            if filter_account.count() >= 4:
                return JsonResponse({"error": "账户数量超过限制"}, status=403)
            new_account = account(
                password=data.get('password'),
                identity_card=filter_online_user[0],
                card_type=data.get('cashierID'),
                balance=0.0,
                current_deposit=0.0,
                uncredited_deposit=0.0,
                is_frozen=False,
                is_lost=False,
            )
            new_account.save()
            return JsonResponse({"success": "successful operation"}, status=200)
        else:
            return JsonResponse({"error": "User not exits"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def cashier_query_account(request):
    if request.method == 'GET':
        filter_accounts = account.objects.filter(account_id=request.GET.get('accountID'))[0]
        account_data = {}
        account_data['id'] = filter_accounts.account_id
        account_data['password'] = filter_accounts.password
        account_data['identity_card'] = filter_accounts.identity_card.identity_card
        account_data['balance'] = filter_accounts.balance
        account_data['currentDeposit'] = filter_accounts.current_deposit
        account_data['uncreditedDeposit'] = filter_accounts.uncredited_deposit
        account_data['isFrozen'] = filter_accounts.is_frozen
        account_data['isLost'] = filter_accounts.is_lost
        return JsonResponse(account_data, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_deposit_record_list(dic):
    deposits = deposit_record.objects.filter(**dic)
    deposit_record_list = list()
    for deposit in deposits:
        deposit_return = {}
        deposit_return['deposit_record_id'] = deposit.deposit_record_id
        deposit_return['account_id'] = deposit.account_id
        deposit_return['deposit_type'] = deposit.deposit_type
        deposit_return['auto_renew_status'] = deposit.auto_renew_status
        deposit_return['deposit_start_date'] = deposit.deposit_start_date
        deposit_return['deposit_end_date'] = deposit.deposit_end_date
        deposit_return['deposit_amount'] = deposit.deposit_ammount
        deposit_return['cashier_id'] = deposit.cashier_id
        deposit_record_list.append(deposit_return)
    return deposit_record_list


# 查询所有的存款记录
def cashier_all_deposits(request):
    if request.method == 'GET':
        dic = {}
        deposit_record_list = get_deposit_record_list(dic)
        return JsonResponse(deposit_record_list, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 活期存款
@csrf_exempt
def cashier_demand_deposit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        filter_account = account.objects.filter(account_id=data.get('account_id'), password=data.get('password'))
        if filter_account.exists():
            if filter_account[0].is_frozen or filter_account[0].is_lost:
                return JsonResponse({"error": "账户挂失/冻结"}, status=403)
            # 更新用户存款情况
            filter_account[0].uncredited_deposit += data.get('deposit_amount')
            filter_account[0].balance += data.get('deposit_amount')
            filter_account[0].save()
            # 更新存款记录
            new_deposit_record = deposit_record(
                account_id=data.get('account_id'),
                deposit_type='活期存款',
                # --此处存疑--
                deposit_start_date=datetime.datetime.now(),
                # -----
                deposit_amount=data.get('deposit_amount'),
                cashier_id=data.get('cashier_id'),
            )
            new_deposit_record.save()
            return JsonResponse({"success": "successful operation"}, status=200)
        else:
            return JsonResponse({"error": "User not exists"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 定期存款
@csrf_exempt
def cashier_time_deposit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        filter_account = account.objects.filter(account_id=data.get('account_id'), password=data.get('password'))
        if filter_account.exists():
            if filter_account[0].is_frozen or filter_account[0].is_lost:
                return JsonResponse({"error": "账户挂失/冻结"}, status=403)
            # 更新用户存款情况
            filter_account[0].current_deposit += data.get('deposit_amount')
            filter_account[0].balance += data.get('deposit_amount')
            filter_account[0].save()
            # 更新存款记录
            new_deposit_record = deposit_record(
                account_id=data.get('account_id'),
                deposit_type='定期存款',
                auto_renew_status=data.get('auto_renew_status'),
                # --此处存疑--
                deposit_start_date=datetime.datetime.now(),
                deposit_end_date=datetime.datetime.now() + data.get('deposit_term'),
                # -----
                deposit_amount=data.get('deposit_amount'),
                cashier_id=data.get('cashier_id'),
            )
            new_deposit_record.save()
            return JsonResponse({"success": "successful operation"}, status=200)
        else:
            return JsonResponse({"error": "User not exists"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 累计存款
def cashier_total_deposit(request):
    if request.method == 'GET':
        filter_account = account.objects.filter(account_id=request.GET.get('account_id'),
                                                password=request.GET.get('password'))
        if filter_account.exists():
            total_deposit = {}
            total_deposit['total_amount'] = filter_account[0].balance
            return JsonResponse(total_deposit, safe=False)
        else:
            return JsonResponse({"error": "User not exists"}, status=403)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_with_drawls_record_list(dic):
    with_drawls = withdrawal_record.objects.filter(**dic)
    with_drawls_record_list = list()
    for with_drawl in with_drawls:
        with_drawls_return = {}
        with_drawls_return['withdrawl_record_id'] = with_drawl.withdrawal_record_id
        with_drawls_return['account_id'] = with_drawl.account_id
        with_drawls_return['withdrawl_date'] = with_drawl.withdrawal_date
        with_drawls_return['withdrawl_amount'] = with_drawl.withdrawal_amount
        with_drawls_return['cashier_id'] = with_drawl.cashier_id
        with_drawls_record_list.append(with_drawls_return)
    return with_drawls_record_list


# 查询所有取款记录
def cashier_all_withdrawls(request):
    if request.method == 'GET':
        dic = {}
        with_drawls_record_list = get_with_drawls_record_list(dic)
        return JsonResponse(with_drawls_record_list, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 取款
@csrf_exempt
def cashier_withdrawl(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        filter_account = account.objects.filter(account_id=data.get('account_id'), password=data.get('password'))
        if filter_account.exists():
            if filter_account[0].is_frozen or filter_account[0].is_lost:
                return JsonResponse({"error": "账户挂失/冻结"}, status=403)
            # 判断用户存款是否满足取出条件
            if filter_account[0].uncredited_deposit >= data.get('withdrawl_amount'):
                # 更新用户存款情况
                filter_account[0].uncredited_deposit -= data.get('withdrawl_amount')
                filter_account[0].balance -= data.get('withdrawl_amount')
                filter_account[0].save()
                # 更新取款记录
                new_withdrawal_record = withdrawal_record(
                    account_id=data.get('account_id'),
                    # --此处存疑--
                    withdrawal_date=datetime.datetime.now(),
                    # -----
                    withdrawal_amount=data.get('withdrawl_amount'),
                    cashier_id=data.get('cashier_id'),
                )
                new_withdrawal_record.save()
                return JsonResponse({"success": "successful operation"}, status=200)
            else:
                return JsonResponse({"error": "存款不足"}, status=403)
        else:
            return JsonResponse({"error": "User not exists"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_transfer_record_list(dic):
    transfers = transfer_record.objects.filter(**dic)
    transfer_record_list = list()
    for transfer in transfers:
        transfers_return = {}
        transfers_return['transfer_record_id'] = transfer.transfer_record_id
        transfers_return['account_in_id'] = transfer.account_in_id
        transfers_return['account_out_id'] = transfer.account_out_id
        transfers_return['transfer_date'] = transfer.transfer_date
        transfers_return['transfer_amount'] = transfer.transfer_amount
        transfers_return['cashier_id'] = transfer.cashier_id
        transfer_record_list.append(transfers_return)
    return transfer_record_list


# 转账记录查询
def cashier_all_transfers(request):
    if request.method == 'GET':
        dic = {}
        transfer_record_list = get_transfer_record_list(dic)
        return JsonResponse(transfer_record_list, safe=False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 转账
@csrf_exempt
def cashier_transfer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        filter_out_account = account.objects.filter(account_id=data.get('account_out_id'), password=data.get('password'))
        filter_in_account = account.objects.filter(account_id=data.get('account_in_id'))
        if not filter_in_account.exists():
            return JsonResponse({"error": "接收转账用户不存在"}, status=403)
        if filter_out_account.exists():
            if filter_out_account[0].is_frozen or filter_out_account[0].is_lost:
                return JsonResponse({"error": "转出账户挂失/冻结"}, status=403)
            if filter_in_account[0].is_frozen or filter_in_account[0].is_lost:
                return JsonResponse({"error": "转入账户挂失/冻结"}, status=403)
            # 判断用户存款是否满足取出条件
            if filter_out_account[0].uncredited_deposit >= data.get('transfer_amount'):
                # 更新用户存款情况
                filter_out_account[0].uncredited_deposit -= data.get('transfer_amount')
                filter_out_account[0].balance -= data.get('transfer_amount')
                filter_out_account[0].save()
                # 更新取款记录
                new_transfer_record = transfer_record(
                    account_in_id=data.get('account_in_id'),
                    account_out_id=data.get('account_out_id'),
                    # --此处存疑--
                    transfer_date=datetime.datetime.now(),
                    # -----
                    transfer_amount=data.get('transfer_amount'),
                    cashier_id=data.get('cashier_id'),
                )
                new_transfer_record.save()
                return JsonResponse({"success": "successful operation"}, status=200)
            else:
                return JsonResponse({"error": "存款不足"}, status=403)
        else:
            return JsonResponse({"error": "转账用户不存在"}, status=403)
    elif request.method == 'OPTION':
        return JsonResponse({"success": "OPTION operation"}, status=200)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


# 查询所有交易记录
def cashier_all_records(request):
    if request.method == 'GET':
        dic = {}
        dic['account_id'] = int(request.GET.get('account_id'))
        if request.GET.get('type') == 1:
            deposit_record_list = get_deposit_record_list(dic)
            return JsonResponse(deposit_record_list, safe=False)
        elif request.GET.get('type') == 2:
            with_drawls_record_list = get_with_drawls_record_list(dic)
            return JsonResponse(with_drawls_record_list, safe=False)
        elif request.GET.get('type') == 3:
            transfer_record_list = get_transfer_record_list(dic)
            return JsonResponse(transfer_record_list, safe=False)
        return JsonResponse({"error": "传入参数错误"}, status=403)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def cashier_unfreeze(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        modify_account = account.objects.get(account_id = data.get("accountID"))
        modify_account.is_frozen = False
        modify_account.save()
        return JsonResponse({"success": "successful operation"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)


def cashier_freeze(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        modify_account = account.objects.get(account_id = data.get("accountID"))
        modify_account.is_frozen = True
        modify_account.save()
        return JsonResponse({"success": "successful operation"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)


def cashier_reportloss(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        modify_account = account.objects.get(account_id = data.get("accountID"))
        modify_account.is_lost = True
        modify_account.save()
        return JsonResponse({"success": "successful operation"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)


def cashier_reissue(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        delete_account = account.objects.get(account_id = data.get("accountID"))
        delete_account.delete()
        return JsonResponse({"success": "successful operation"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)