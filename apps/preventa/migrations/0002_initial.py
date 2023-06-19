# Generated by Django 4.2 on 2023-06-18 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("payment", "0002_initial"),
        ("preventa", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name="order",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="payment.order",
                verbose_name="Order",
            ),
        ),
        migrations.AddField(
            model_name="usercontent",
            name="preventa_audio",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="preventa.audio",
                verbose_name="Bought Audio",
            ),
        ),
        migrations.AddField(
            model_name="usercontent",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_preventa_audios",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
