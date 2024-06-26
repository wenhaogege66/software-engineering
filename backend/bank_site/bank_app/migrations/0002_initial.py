# Generated by Django 5.0.6 on 2024-06-10 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("bank_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="deposit_record",
            fields=[
                (
                    "deposit_record_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("account_id", models.IntegerField()),
                ("deposit_type", models.CharField(max_length=10)),
                ("auto_renew_status", models.BooleanField()),
                ("deposit_start_date", models.DateField()),
                ("deposit_end_date", models.DateField()),
                ("deposit_amount", models.FloatField()),
                ("cashier_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="employee",
            fields=[
                ("employee_id", models.AutoField(primary_key=True, serialize=False)),
                ("employee_name", models.CharField(default="Unknown", max_length=20)),
                ("identity_card", models.CharField(default="Unknown", max_length=18)),
                ("employee_sex", models.IntegerField(default=0)),
                ("phone_number", models.CharField(default="Unknown", max_length=20)),
                ("occupation_name", models.CharField(default="Unknown", max_length=50)),
                ("is_employeed", models.BooleanField(default="False")),
                (
                    "other_information",
                    models.CharField(default="Unknown", max_length=1021),
                ),
            ],
        ),
        migrations.CreateModel(
            name="online_user",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("user_name", models.CharField(default="Unknown", max_length=20)),
                ("password", models.CharField(default="666666", max_length=20)),
                ("identity_card", models.CharField(max_length=18, unique=True)),
                ("phone_num", models.CharField(default="10086", max_length=20)),
                ("is_frozen", models.BooleanField(default=False)),
                ("is_lost", models.BooleanField(default=False)),
                ("is_blacklisted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="transfer_record",
            fields=[
                (
                    "transfer_record_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("account_in_id", models.IntegerField()),
                ("account_out_id", models.IntegerField()),
                ("transfer_date", models.DateField()),
                ("transfer_amount", models.FloatField()),
                ("cashier_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="withdrawal_record",
            fields=[
                (
                    "withdrawal_record_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("account_id", models.IntegerField()),
                ("withdrawal_date", models.DateField()),
                ("withdrawal_amount", models.FloatField()),
                ("cashier_id", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="cashier",
            fields=[
                ("cashier_id", models.AutoField(primary_key=True, serialize=False)),
                ("account", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=20)),
                ("trade_authority", models.BooleanField()),
                ("manage_authority", models.BooleanField()),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_app.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="online_bank_manager",
            fields=[
                (
                    "online_bank_manager_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("account", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=20)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_app.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BlackList",
            fields=[
                ("list_id", models.AutoField(primary_key=True, serialize=False)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "manager_id",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_app.online_bank_manager",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_app.online_user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="account",
            fields=[
                ("account_id", models.AutoField(primary_key=True, serialize=False)),
                ("password", models.CharField(max_length=20)),
                ("card_type", models.IntegerField()),
                ("balance", models.FloatField(default=0.0)),
                ("current_deposit", models.FloatField(default=0.0)),
                ("uncredited_deposit", models.FloatField(default=0.0)),
                ("is_frozen", models.BooleanField(default=False)),
                ("is_lost", models.BooleanField(default=True)),
                (
                    "identity_card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="bank_app.online_user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="sys_manage",
            fields=[
                ("sys_manager_id", models.AutoField(primary_key=True, serialize=False)),
                ("account", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=20)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bank_app.employee",
                    ),
                ),
            ],
        ),
    ]
