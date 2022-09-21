# Generated by Django 4.1.1 on 2022-09-21 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='home.employee'),
        ),
    ]