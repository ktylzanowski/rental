# Generated by Django 4.1.5 on 2023-03-19 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deadline',
            field=models.DateTimeField(null=True),
        ),
    ]