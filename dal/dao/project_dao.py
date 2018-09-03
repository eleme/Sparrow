from dal.models import Project
from django.contrib.auth.models import User
from dal.models import UserProfile
from django.forms.models import model_to_dict
from Sparrow.action.common_action import *
import logging

logger = logging.getLogger('django')


class ProjectDao:
    @staticmethod
    def get_projects(offset, limit):
        projects = Project.objects.all().order_by('-updateTime')[offset: offset + limit]
        return projects

    @staticmethod
    def get_project_list(offset, limit):
        projects = list(ProjectDao.get_projects(offset, limit).values('project_id',
                                                                      'name',
                                                                      'note',
                                                                      'status',
                                                                      'createTime',
                                                                      'updateTime'))
        return projects

    @staticmethod
    def get_project_list_with_user(user, offset, limit):
        userProfile = UserProfile.objects.get(user_id=user.id)
        result0 = Project.objects.filter(permissionType=Project.PermissionType.Public.value)
        result1 = userProfile.projects.filter()
        result = result0 | result1
        # 去重
        result = result.distinct()
        project_dics = list(result.values('project_id',
                                          'name',
                                          'note',
                                          'status')[offset: offset + limit])
        return project_dics

    @staticmethod
    def get_all_projects_count():
        result = Project.objects.all().values('project_id').count()
        return result

    @staticmethod
    def get_project_with_id(project_id):
        try:
            project = Project.objects.get(project_id=project_id)
            return project
        except:
            return None

    @staticmethod
    def get_project_with_api_id(api_id):
        try:
            project = Project.objects.filter(apis__api_id=api_id).values('project_id',
                                                                         'name',
                                                                         'note',
                                                                         'status',
                                                                         'createTime',
                                                                         'updateTime').first()
            return project
        except:
            return None

    @staticmethod
    def get_project_with_Name(name):
        try:
            project = Project.objects.get(name=name)
            return project
        except:
            return None

    @staticmethod
    def create(model):
        project = Project.objects.create(name=model.name,
                                         note=model.note,
                                         permissionType=model.permissionType,
                                         status=model.status)
        return project

    @staticmethod
    def update(model):
        result = Project.objects.filter(project_id=model.project_id).update(name=model.name,
                                                                            note=model.note,
                                                                            permissionType=model.permissionType,
                                                                            status=model.status,
                                                                            updateTime=datetime.datetime.now())
        if result > 0:
            return True
        else:
            return False

    @staticmethod
    def delete(project_id):
        q = Api.objects.filter(project__project_id=project_id)
        q.delete()

        deleted_count, _ = Project.objects.filter(project_id=project_id).delete()
        if deleted_count > 0:
            return True
        else:
            return False

    @staticmethod
    def get_all_users_with_project_id(project_id):
        userProfiles = UserProfile.objects.filter(projects__project_id=project_id).values('user_id')
        users = []
        for userProfile in userProfiles:
            user = list(User.objects.filter(id=userProfile['user_id']).values('id',
                                                                              'username',
                                                                              'email'))[0]
            users.append(user)

        return users

    @staticmethod
    def remove_user(project_id, user_id):
        project = ProjectDao.get_project_with_id(project_id)
        userProfile = UserProfile.objects.get(user__id=user_id)
        userProfile.projects.remove(project)
        userProfile.save()

    @staticmethod
    def add_users(project_id, user_ids):
        project = ProjectDao.get_project_with_id(project_id)
        userDics = []
        for id in user_ids:
            userProfile = UserProfile.objects.get(user__id__in=id)
            userDic = list(User.objects.filter(id=id).values('id',
                                                             'username',
                                                             'email'))[0]
            userDics.append(userDic)
            userProfile.projects.add(project)
        userProfile.save()

        return userDics
