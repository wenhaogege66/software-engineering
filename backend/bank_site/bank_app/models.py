from django.db import models

# Create your models here.



class employee(models.Model):
    employee_id = models.AutoField(primary_key = True)
    employee_name = models.CharField(max_length = 20, null = False, default = "Unknown")
    identity_card = models.CharField(max_length = 18, null = False, default = "Unknown")
    employee_sex = models.IntegerField(null = False, default = 0)
    phone_number = models.CharField(max_length = 20, null = False, default = "Unknown")
    occupation_name = models.CharField(max_length = 50, null = False, default = "Unknown")
    is_employeed = models.BooleanField(null = False, default = "False")
    other_information = models.CharField(max_length = 1021, default = "Unknown")


class sys_manage(models.Model):
    sys_manager_id = models.AutoField(primary_key = True)
    employee = models.ForeignKey(employee, on_delete = models.CASCADE)
    account = models.CharField(max_length = 100, null = False)
    password = models.CharField(max_length = 20, null = False)


class cashier(models.Model):
    cashier_id = models.AutoField(primary_key = True)
    employee = models.ForeignKey(employee, on_delete = models.CASCADE)
    account = models.CharField(max_length = 100, null = False)
    password = models.CharField(max_length = 20, null = False)
    trade_authority = models.BooleanField(null = False)
    manage_authority = models.BooleanField(null = False)


class online_user(models.Model):
    user_id = models.AutoField(primary_key = True,default = 1)
    user_name = models.CharField(max_length = 20, null = False, default = "Unknown")
    password = models.CharField(max_length=20, null=False,default = "666666")
    identity_card = models.CharField(max_length = 18, null = False)
    phone_num = models.CharField(max_length=20, null=False,default = "10086")
    is_frozen = models.BooleanField(null=False, default=False)
    is_lost = models.BooleanField(null=False, default=False)
    is_blacklisted = models.BooleanField(default=False)


# 账户表
class account(models.Model):
    account_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=20, null=False)
    identity_card = models.ForeignKey(online_user, on_delete=models.PROTECT)
    card_type = models.IntegerField(null=False)
    balance = models.FloatField(null=False, default=0.0)
    current_deposit = models.FloatField(null=False, default=0.0)
    uncredited_deposit = models.FloatField(null=False, default=0.0)
    is_frozen = models.BooleanField(null=False, default=False)
    is_lost = models.BooleanField(null=False, default=True)


# 存款记录
class deposit_record(models.Model):
    deposit_record_id = models.AutoField(primary_key = True)
    account_id = models.IntegerField(null = False)
    deposit_type = models.CharField(max_length = 10, null = False)
    auto_renew_status = models.BooleanField()
    deposit_start_date = models.DateField(null = False)
    deposit_end_date = models.DateField()
    deposit_amount = models.FloatField(null = False)
    cashier_id = models.IntegerField(null = False)


# 取款记录
class withdrawal_record(models.Model):
    withdrawal_record_id = models.AutoField(primary_key = True)
    account_id = models.IntegerField(null = False)
    withdrawal_date = models.DateField(null = False)
    withdrawal_amount = models.FloatField(null = False)
    cashier_id = models.IntegerField(null = False)


# 转账记录
class transfer_record(models.Model):
    transfer_record_id = models.AutoField(primary_key = True)
    account_in_id = models.IntegerField(null = False)
    account_out_id = models.IntegerField(null = False)
    transfer_date = models.DateField(null = False)
    transfer_amount = models.FloatField(null = False)
    cashier_id = models.IntegerField(null = False)

class BlackList(models.Model):
    admin = models.ForeignKey(sys_manage, on_delete=models.CASCADE)
    user = models.ForeignKey(online_user, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)