# Generated by Django 4.1.1 on 2022-09-29 07:51

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('iban', models.CharField(max_length=34, primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('amount', models.FloatField(default=0)),
                ('interest', models.FloatField(default=0)),
                ('negative_interest', models.FloatField(default=7.3)),
                ('status', models.IntegerField(default=0)),
                ('overdraft', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('balance', models.FloatField()),
                ('profit', models.FloatField()),
                ('bic', models.CharField(max_length=11, primary_key=1, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='BankStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('eid', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standing_order', models.BooleanField(default=0)),
                ('standing_order_days', models.IntegerField(blank=True, default=None, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.FloatField()),
                ('iban_receiver', models.CharField(max_length=34)),
                ('name_receiver', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('reference', models.CharField(blank=True, default=None, max_length=140, null=True)),
                ('approved', models.BooleanField(default=0)),
                ('approved_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='home.employee')),
                ('iban_sender', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='iban_sender', to='home.account')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalTransaction',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.transaction')),
            ],
            bases=('home.transaction',),
        ),
        migrations.CreateModel(
            name='TagesgeldAccount',
            fields=[
                ('account_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.account')),
                ('time_period', models.IntegerField(default=0)),
            ],
            bases=('home.account',),
        ),
        migrations.CreateModel(
            name='Tan',
            fields=[
                ('tan', models.IntegerField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=1)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.account')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('address', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('birthday', models.DateField()),
                ('confirmed', models.BooleanField(default=False)),
                ('contacts', models.ManyToManyField(blank=True, to='home.person')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.person'),
        ),
        migrations.CreateModel(
            name='DebitCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.IntegerField()),
                ('state', models.BooleanField(default=1)),
                ('expiration_date', models.DateField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.account')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvv', models.IntegerField()),
                ('pin', models.IntegerField()),
                ('state', models.BooleanField(default=1)),
                ('expiration_date', models.DateField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.account')),
            ],
        ),
        migrations.CreateModel(
            name='Accountkopie',
            fields=[
                ('iban', models.CharField(max_length=34, primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('amount', models.FloatField(default=0)),
                ('interest', models.FloatField(default=0)),
                ('negative_interest', models.FloatField(default=0.073)),
                ('status', models.IntegerField(default=0)),
                ('overdraft', models.FloatField(default=0)),
                ('employee', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.employee')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='employee',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.employee'),
        ),
        migrations.AddField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='transaction',
            constraint=models.CheckConstraint(check=models.Q(('amount__gt', 0)), name='check_amount'),
        ),
        migrations.AddField(
            model_name='externaltransaction',
            name='sending_bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='home.bank'),
        ),
    ]
