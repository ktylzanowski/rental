# Generated by Django 4.1.5 on 2023-03-15 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='if_extended',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='number_of_extensions',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]