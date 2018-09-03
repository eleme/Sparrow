# Generated by Django 2.0 on 2018-04-05 07:02

import dal.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('api_id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=128)),
                ('method', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=128, null=True)),
                ('note', models.CharField(default='', max_length=512, null=True)),
                ('status', models.IntegerField(default=0)),
                ('responseJson', models.TextField(blank=True, default='{}', null=True)),
                ('star', models.BooleanField(default=False)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
            ],
            bases=(models.Model, dal.models.Dictable),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('note', models.CharField(default='', max_length=512, null=True)),
                ('status', models.IntegerField(default=1)),
                ('permissionType', models.IntegerField(default=0)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
                ('apis', models.ManyToManyField(to='dal.Api')),
            ],
            options={
                'permissions': (('view_project', 'Can see detail of project '),),
            },
            bases=(models.Model, dal.models.Dictable),
        ),
        migrations.CreateModel(
            name='ResTemplate',
            fields=[
                ('res_template_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('note', models.CharField(default='', max_length=512, null=True)),
                ('mimeType', models.IntegerField(default=0)),
                ('responseJson', models.TextField(blank=True, default='{}', null=True)),
                ('createTime', models.DateTimeField(auto_now_add=True)),
                ('updateTime', models.DateTimeField(auto_now=True)),
            ],
            bases=(models.Model, dal.models.Dictable),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('projects', models.ManyToManyField(related_name='dal_userprofile_related', to='dal.Project')),
            ],
            bases=(models.Model, dal.models.Dictable),
        ),
        migrations.AddField(
            model_name='project',
            name='responseTemplates',
            field=models.ManyToManyField(to='dal.ResTemplate'),
        ),
    ]
