# Generated by Django 4.1.2 on 2022-11-15 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablebooking',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
