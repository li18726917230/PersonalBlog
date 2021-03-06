# Generated by Django 3.2.5 on 2021-08-16 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_other',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_name', models.CharField(max_length=128)),
                ('sex', models.CharField(max_length=4)),
                ('id_card', models.CharField(max_length=128, null=True)),
                ('home_add', models.CharField(max_length=128, null=True)),
                ('marital_status', models.CharField(max_length=128)),
                ('worku_nits', models.CharField(max_length=128, null=True)),
                ('monthly_income', models.CharField(max_length=128, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
