import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import cashier, employee
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def all_cashiers(request):
    if request.method == 'GET':
        # 获取所有的cashier
        cashiers = cashier.objects.all()
        # 转化为list形式
        cashier_list = list(cashiers.values())
        rs = []
        cashier_dict = {}
        for one_cashier in cashier_list:
            cashier_dict = {}
            employee_list = employee.objects.get(employee_id = one_cashier["employee_id"])
            cashier_dict["id"] = one_cashier["cashier_id"]
            cashier_dict["account"] = one_cashier["account"]
            cashier_dict["password"] = one_cashier["password"]
            cashier_dict["name"] = employee_list.employee_name
            cashier_dict["identity_card"] = employee_list.identity_card
            if employee_list.employee_sex == 0:
                cashier_dict["sex"] = "男"
            else: cashier_dict["sex"] = "女"
            cashier_dict["phone"] = employee_list.phone_number
            if one_cashier["trade_authority"]:
                cashier_dict["ifTrade"] = True
            else: cashier_dict["ifTrade"] = False
            if one_cashier["manage_authority"]:
                cashier_dict["ifManage"] = True
            else: cashier_dict["ifManage"] = False
            rs.append(cashier_dict)
        return JsonResponse(rs, safe = False)
    else:
        return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def add_cashier(request):
    if request.method == 'POST':
        # data是一个字典，可以用.get()访问键值对
        data = json.loads(request.body.decode('utf-8'))
        check_account = data.get("account")
        if cashier.objects.filter(account = check_account).exists():
            return JsonResponse({"error": "出纳员账户已存在"}, status = 403)
        sex = 0
        if data.get("sex") == "男":
            sex = 0
        else: sex = 1
        new_employee = employee(employee_name = data.get("name"), 
                             identity_card = data.get("identity_card"),
                             employee_sex = sex,
                             phone_number = data.get("phone"),
                             occupation_name = "bank",
                             is_employeed = True)
        new_employee.save()
        new_cashier = cashier(employee = new_employee,
                              account = data.get("account"),
                              password = data.get("password"),
                              trade_authority = data.get("trade_authority"),
                              manage_authority = data.get("manage_authority"))
        new_cashier.save()
        return JsonResponse({"success": "出纳员添加成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def delete_cashier(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        delete_cashier = cashier.objects.get(cashier_id = data.get("id"))
        modify_employee = delete_cashier.employee
        delete_cashier.delete()
        modify_employee.is_employeed = False
        modify_employee.save()
        return JsonResponse({"success": "出纳员删除成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def modify_cashier(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        modify_cashier = cashier.objects.get(cashier_id = data.get("id"))
        if modify_cashier.account != data.get("account"):
            if cashier.objects.filter(account = data.get("account")).exists():
                return JsonResponse({"error": "出纳员账户已存在"}, status = 403)
        modify_employee = modify_cashier.employee
        modify_employee.employee_name = data.get("name")
        modify_employee.identity_card = data.get("identity_card")
        modify_employee.phone_number = data.get("phone")
        if data.get("sex") == "男":
            modify_employee.employee_sex = 0
        else: modify_employee.employee_sex = 1
        modify_cashier.password = data.get("password")
        modify_cashier.account = data.get("account")
        modify_employee.save()
        modify_cashier.save()
        return JsonResponse({"success": "修改出纳员成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)

@csrf_exempt
def modify_authority(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        modify_cashier = cashier.objects.get(cashier_id = data.get("id"))
        modify_cashier.trade_authority = data.get("ifTrade")
        modify_cashier.manage_authority = data.get("ifManage")
        modify_cashier.save()
        return JsonResponse({"success": "修改出纳员权限成功"}, status = 200)
    elif request.method == 'OPTIONS':
        return JsonResponse({"success": "OPTION operation"}, status = 200)
    else: return JsonResponse({"error": "Method not allowed"}, status = 405)