# Generated by Django 2.0.2 on 2018-02-07 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20180207_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculation',
            name='customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='polls.Customer'),
        ),
    ]
