# Generated by Django 4.1.5 on 2023-01-10 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(default=None, upload_to='product')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
                ('author', models.CharField(max_length=100)),
                ('isbn', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='CD',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
                ('author', models.CharField(max_length=100)),
                ('tracklist', models.TextField(max_length=500)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.product')),
                ('director', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('products.product',),
        ),
    ]
