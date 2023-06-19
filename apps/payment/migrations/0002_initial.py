# Generated by Django 4.2 on 2023-06-18 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("preventa", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usercard",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="audio",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="preventa.audio",
                verbose_name="Audio",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user_card",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orders",
                to="payment.usercard",
                verbose_name="User card",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="usercard",
            unique_together={("user", "card_number")},
        ),
    ]
