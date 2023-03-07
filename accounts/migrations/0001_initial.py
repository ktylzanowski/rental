# Generated by Django 4.1.5 on 2023-03-07 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('street', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('building_number', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('apartment_number', models.CharField(blank=True, default=None, max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
