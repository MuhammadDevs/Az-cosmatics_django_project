# Generated by Django 5.0.4 on 2024-04-12 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=255)),
                ('image', models.ImageField(upload_to='product/')),
            ],
        ),
    ]
