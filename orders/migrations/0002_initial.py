# Generated by Django 4.1.5 on 2023-04-05 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productindex'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.shipping'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
