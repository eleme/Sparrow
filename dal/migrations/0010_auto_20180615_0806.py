# Generated by Django 2.0 on 2018-06-15 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dal', '0009_auto_20180615_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restemplate',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dal.Project'),
        ),
    ]
