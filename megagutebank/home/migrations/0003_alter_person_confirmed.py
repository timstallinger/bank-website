# Generated by Django 4.1.1 on 2022-09-29 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_bank_balance_alter_bank_bic_alter_bank_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='confirmed',
            field=models.IntegerField(default=0),
        ),
    ]
