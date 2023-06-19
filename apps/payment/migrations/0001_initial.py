# Generated by Django 4.2 on 2023-06-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "type",
                    models.CharField(choices=[("audio", "Audio")], max_length=63, verbose_name="Type"),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("one_time", "One Time"),
                            ("four_time", "Four Time"),
                            ("one_month", "One Month"),
                            ("one_day", "One Day"),
                        ],
                        max_length=63,
                        verbose_name="Payment Type",
                    ),
                ),
                (
                    "provider",
                    models.CharField(
                        choices=[("flow", "FLOW")],
                        max_length=63,
                        verbose_name="Provider",
                    ),
                ),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Total Amount"),
                ),
                ("is_paid", models.BooleanField(default=False, verbose_name="Is Paid")),
                (
                    "is_canceled",
                    models.BooleanField(default=False, verbose_name="Is Canceled"),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
            },
        ),
        migrations.CreateModel(
            name="UserCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated at"),
                ),
                (
                    "card_number",
                    models.CharField(max_length=255, verbose_name="Card Number"),
                ),
                (
                    "expire_date",
                    models.CharField(max_length=255, verbose_name="Expire Date"),
                ),
                ("card_id", models.CharField(max_length=255, verbose_name="Card ID")),
                (
                    "token",
                    models.CharField(max_length=255, null=True, verbose_name="Token"),
                ),
                (
                    "confirmed",
                    models.BooleanField(default=False, verbose_name="Confirmed"),
                ),
            ],
            options={
                "verbose_name": "User Card",
                "verbose_name_plural": "User Cards",
            },
        ),
    ]
