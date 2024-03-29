# Generated by Django 4.2 on 2023-06-26 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_content_four_repr_price_content_price"),
        ("preventa", "0004_usercontentpaymentplan_order_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercontentpaymentplan",
            name="content",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_content_plan",
                to="common.content",
                verbose_name="Content",
            ),
        ),
    ]
