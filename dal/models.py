from django.db import models
from enum import Enum, unique
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


class Dictable(object):
    def as_dict(self):
        dict = {}
        # exclude ManyToOneRel, which backwards to ForeignKey
        field_names = []
        for field in self._meta.get_fields():
            if 'ManyToOneRel' not in str(field) and 'ManyToManyRel' not in str(field):
                field_names.append(field.name)
        for name in field_names:
            field_instance = getattr(self, name)
            if field_instance.__class__.__name__ == 'ManyRelatedManager':
                model_dics = []
                for model in field_instance.all():
                    model_dics.append(model_to_dict(model))
                dict[name] = model_dics
                continue
            dict[name] = field_instance
        return dict


class ResTemplate(models.Model, Dictable):
    res_template_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    note = models.CharField(max_length=512, null=True, default='')
    mimeType = models.IntegerField(default=0)
    responseJson = models.TextField(default='{}', blank=True, null=True)
    type = models.IntegerField(default=0, null=False)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)

    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    @unique
    class MIMEType(Enum):
        ApplicationJson = 0
        TextPlain = 1
        ImageJpeg = 2

    @unique
    class Type(Enum):
        Public = 0
        BelongsToProject = 1


class Api(models.Model, Dictable):
    api_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=128)
    method = models.CharField(max_length=8)
    name = models.CharField(max_length=128, null=True)
    note = models.CharField(max_length=512, null=True, default='')
    status = models.IntegerField(default=0)
    star = models.BooleanField(default=False)
    resTemplate = models.ForeignKey(ResTemplate, on_delete=models.CASCADE, null=True)

    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    @unique
    class Status(Enum):
        Disabled = 0
        Mock = 1
        # 使用其他环境
        UseOther = 2


class Project(models.Model, Dictable):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    note = models.CharField(max_length=512, null=True, default='')
    status = models.IntegerField(default=1)
    permissionType = models.IntegerField(default=0)
    apis = models.ManyToManyField(Api)

    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)

    @unique
    class Status(Enum):
        Disabled = 0
        Abled = 1

    @unique
    class PermissionType(Enum):
        # 所有人可见
        Public = 0
        # 用户自行配置
        Custom = 1

    class Meta:
        permissions = (
            ("view_project", "Can see detail of project "),
        )


class UserProfile(models.Model, Dictable):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True, )
    projects = models.ManyToManyField(
        Project,
        related_name='%(app_label)s_%(class)s_related')

    def create(self, *args, **kwargs):
        if not self.pk:
            try:
                p = UserProfile.objects.get(user=self.user)
                self.pk = p.pk
            except UserProfile.DoesNotExist:
                pass
        super(UserProfile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    print(kwargs)
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


def add_user_to_default_group(sender, instance, created, **kwargs):
    print(kwargs)
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        try:
            default_group = Group.objects.get(name='default_group')
        except:
            default_group = Group.objects.create(name='default_group')
        default_group.user_set.add(instance)


post_save.connect(create_user_profile, sender=User)
post_save.connect(add_user_to_default_group, sender=User)


# 数据统计部分
@unique
class ActionType(Enum):
    Mock = 0

    ProjectList = 1
    ProjectDetail = 2
    ProjectCreate = 3
    ProjectUpdate = 4
    ProjectRepeatNameVerification = 5
    ProjectDelete = 6
    ProjectGetMembers = 7
    ProjectRemoveMember = 8
    ProjectAddMember = 9

    ApiFetch = 10
    ApiCreate = 11
    ApiList = 12
    ApiRepeatNameVerification = 13
    ApiDelete = 14
    ApiDetail = 15
    ApiUpdate = 16
    ApiStar = 17
    ApiUpdateStatus = 18
    ApiStarList = 19
    ApiBatchUpdateStatus = 33

    ResTemplateList = 20
    ResTemplateDetail = 21
    ResTemplateCreate = 22
    ResTemplateRepeatNameVerification = 23
    ResTemplateDelete = 24
    ResTemplateUpdate = 25

    AccountLogin = 26
    AccountLogout = 27
    AccountRedirectLogin = 28
    AccountCheckStatus = 29
    AccountSearch = 30
    AccountQuickLogin = 31
    AccountRequestQuickLogin = 32

    ActionDailyActiveInfo = 34
    ActionTopActiveUserInfo = 35
    ActionTopActiveApisInfo = 36


class Action(models.Model, Dictable):
    # 操作类型
    type = models.IntegerField(default=0)
    function_info = models.CharField(max_length=512, null=True, default='')
    request_info = models.CharField(max_length=512, null=True, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_time = models.DateTimeField(auto_now_add=True)


class QuickLoginRecord(models.Model, Dictable):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    verification_code = models.CharField(max_length=32, null=True, default='')
