# Generated by Django 2.0 on 2018-06-15 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dal', '0010_auto_20180615_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='responseJson',
        ),
        migrations.AddField(
            model_name='api',
            name='resTemplate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dal.ResTemplate'),
        ),
    ]
