# Generated by Django 4.2.3 on 2024-03-27 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
