# Generated by Django 4.2 on 2023-06-22 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("common", "0002_initial"),
        ("payment", "0002_initial"),
        ("preventa", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usercontentpaymentplan",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_content_payment_plans",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AddField(
            model_name="usercontent",
            name="content",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="common.content",
                verbose_name="Content",
            ),
        ),
        migrations.AddField(
            model_name="usercontent",
            name="order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="payment.order",
                verbose_name="Order",
            ),
        ),
        migrations.AddField(
            model_name="usercontent",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_content",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
