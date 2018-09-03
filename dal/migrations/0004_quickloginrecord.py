# Generated by Django 2.0 on 2018-05-17 08:07

import dal.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dal', '0003_auto_20180516_0736'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickLoginRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, dal.models.Dictable),
        ),
    ]
