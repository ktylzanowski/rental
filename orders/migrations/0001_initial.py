# Generated by Django 4.1.7 on 2023-03-30 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField()),
                ('deadline', models.DateTimeField(null=True)),
                ('return_date', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('Ordered', 'Ordered'), ('Sent', 'Sent'), ('Delivered', 'Delivered'), ('Extended', 'Extended'), ('Returned', 'Returned')], default='Ordered', max_length=100)),
                ('total', models.IntegerField()),
                ('debt', models.IntegerField(default=0, null=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=12)),
                ('city', models.CharField(default=None, max_length=255)),
                ('zip_code', models.CharField(default=None, max_length=10)),
                ('street', models.CharField(default=None, max_length=255)),
                ('building_number', models.CharField(default=None, max_length=10)),
                ('apartment_number', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('if_extended', models.BooleanField(blank=True, default=False, null=True)),
                ('number_of_extensions', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_method', models.CharField(max_length=100)),
                ('if_paid', models.BooleanField(default=False)),
                ('postage', models.IntegerField()),
                ('quantity_of_items', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
                ('amount_paid', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=15)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
