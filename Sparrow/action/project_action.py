from django.forms.models import model_to_dict
from dal.dao.project_dao import ProjectDao
from dal.dao.account_dao import AccountDao
from django.views.decorators.csrf import csrf_exempt
from Sparrow.action.common_action import *
from Sparrow.forms import *
from dal.models import *
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import User
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import remove_perm
from django.http.request import HttpRequest
from Sparrow.action.response import *
from Sparrow.action.track import track


class ProjectAction:
    @track(ActionType.ProjectList)
    @login_required
    def list(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            response = Response(RequestMethodError, 'Method is invalid', {})
            return HttpResponse(response.toJson(), content_type='application/json')
        limit = 10
        page = 1
        if 'limit' in request.GET.keys():
            limit = int(request.GET['limit'])
        if 'current_page' in request.GET.keys():
            page = int(request.GET['current_page'])

        offset = (page - 1) * limit
        project_list = ProjectDao.get_project_list_with_user(request.user, offset, limit)
        count = ProjectDao.get_all_projects_count()

        response = Response(Success,
                            'Success',
                            {'projects': project_list,
                             'current_page': page,
                             'total': count,
                             'limit': limit})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ProjectDetail)
    @permission_required_or_403('view_project', (Project, 'project_id', 'project_id'))
    @login_required
    def detail(request: HttpRequest, project_id):
        project = ProjectDao.get_project_with_id(project_id)

        response = Response(Success,
                            'Success',
                            model_to_dict(project))
        return HttpResponse(response.toJson(), content_type='application/json')

    @csrf_exempt
    @track(ActionType.ProjectCreate)
    @login_required
    def create(request: HttpRequest):
        if request.method != CommonData.Method.POST.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        form = ProjectCreateForm(data=request.POST)
        if form.is_valid():
            model = Project()
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.permissionType = form.clean().get('permissionType')
            model.status = form.clean().get('status')
            project = ProjectDao.create(model)

            # setting user profile
            userProfile = AccountDao.get_userProfile_with_id(request.user.id)
            userProfile.projects.add(project)
            userProfile.save()
            # setting user permissions
            user = User.objects.get(id=request.user.id)
            assign_perm('view_project', user, project)
            # setting group permissions
            default_group = AccountDao.get_default_group()
            if model.permissionType == Project.PermissionType.Public.value:
                assign_perm('view_project', default_group, project)
            else:
                remove_perm('view_project', default_group, project)

            if project is None:
                response = Response(DaoOperationError,
                                    'API create failed',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
            else:
                response = Response(Success,
                                    'Sucsses',
                                    model_to_dict(project))
                return HttpResponse(response.toJson(), content_type='application/json')
        else:
            response = Response(FormParseError,
                                'Form parse failed',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')

    @csrf_exempt
    @track(ActionType.ProjectUpdate)
    @login_required
    def update(request: HttpRequest, project_id):
        if request.method != CommonData.Method.POST.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')
        form = ProjectUpateForm(data=request.POST)
        if form.is_valid():
            model = ProjectDao.get_project_with_id(project_id)
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.permissionType = form.clean().get('permissionType')
            model.status = form.clean().get('status')
            result = ProjectDao.update(model)

            # setting group permissions
            default_group = AccountDao.get_default_group()
            if model.permissionType == Project.PermissionType.Public.value:
                assign_perm('view_project', default_group, model)
            else:
                remove_perm('view_project', default_group, model)

            if result is False:
                response = Response(DaoOperationError,
                                    'Project update failed',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
            else:
                response = Response(Success,
                                    'Success',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
        else:
            response = Response(FormParseError,
                                'Form parse failed',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ProjectRepeatNameVerification)
    @login_required
    def repeat_name_verification(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        if ('name' not in request.GET.keys()):
            response = Response(MissingParametersError,
                                'Missing parameters',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')
        name = request.GET['name']
        project = ProjectDao.get_project_with_Name(name)

        response = Response(Success, 'Success', {})

        if project is None:
            response.data['repeatability'] = False
        else:
            response.data['api'] = project.as_dict()
            if 'project_id' in request.GET.keys():
                project_id = request.GET['project_id']
                if str(project.project_id) == str(project_id):
                    response.data['repeatability'] = False
                else:
                    response.data['repeatability'] = True
            else:
                response.data['repeatability'] = True
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ProjectDelete)
    @login_required
    def delete(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        project_id = request.GET['project_id']
        if project_id is None:
            response = Response(RequestParamsError,
                                'Project_id is None',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')
        success = ProjectDao.delete(project_id)

        if success:
            return HttpResponse(Response.successResponse().toJson(), content_type='application/json')
        else:
            return HttpResponse(Response.daoOperationErrorResponse().toJson(), content_type='application/json')

    @track(ActionType.ProjectGetMembers)
    @login_required
    def get_members(request: HttpRequest, project_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        if project_id is None:
            response = Response(RequestParamsError,
                                'project_id is None',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')

        aList = ProjectDao.get_all_users_with_project_id(project_id)
        response = Response(Success,
                            'Success',
                            aList)
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ProjectRemoveMember)
    @login_required
    def remove_member(request: HttpRequest, project_id, user_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        project = ProjectDao.get_project_with_id(project_id)
        user = User.objects.get(id=user_id)
        # setting user permissions
        remove_perm('view_project', user, project)

        ProjectDao.remove_user(project_id, user_id)

        response = Response(Success,
                            'Success',
                            {})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ProjectAddMember)
    @login_required
    def add_member(request: HttpRequest, project_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        user_ids = request.GET.getlist('id[]')
        users = ProjectDao.add_users(project_id, user_ids)

        project = ProjectDao.get_project_with_id(project_id)
        # setting user permissions
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            assign_perm('view_project', user, project)

        response = Response(Success,
                            'Success',
                            users)
        return HttpResponse(response.toJson(), content_type='application/json')
