# Generated by Django 4.1.5 on 2023-03-07 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(default=None, upload_to='product')),
                ('quantity', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('price', models.IntegerField(default=15)),
                ('popularity', models.IntegerField(default=0)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
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
                ('genre', models.CharField(choices=[('Fantasy', 'Fantasy'), ('Sci-Fi', 'Sci-Fi'), ('Romance', 'Romance'), ('Historical Novel', 'Historical Novel'), ('Horror', 'Horror'), ('Criminal', 'Criminal'), ('Biography', 'Biography')], max_length=100)),
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
                ('band', models.CharField(max_length=100)),
                ('tracklist', models.TextField(max_length=500)),
                ('genre', models.CharField(choices=[('Rock', 'Rock'), ('Pop', 'Pop'), ('Reggae', 'Reggae'), ('Disco', 'Disco'), ('Rap', 'Rap'), ('Electronic music', 'Electronic music')], max_length=100)),
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
                ('genre', models.CharField(choices=[('Comedy', 'Comedy'), ('Adventure', 'Adventure'), ('Romance', 'Romance'), ('Horror', 'Horror'), ('Thriller', 'Thriller'), ('Animated', 'Animated')], max_length=100)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('products.product',),
        ),
    ]
