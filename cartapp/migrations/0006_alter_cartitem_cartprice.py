# Generated by Django 3.2.13 on 2022-07-30 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0005_cartitem_cartprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cartprice',
            field=models.FloatField(null=True),
        ),
    ]