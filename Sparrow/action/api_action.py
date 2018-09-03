from dal.dao.api_dao import ApiDao
from dal.dao.project_dao import ProjectDao
from Sparrow.forms import *
from dal.models import *
from Sparrow.action.common_action import *
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from Sparrow.action.response import *
from Sparrow.action.track import track
from enum import IntEnum


class ApiAction:
    @track(ActionType.ApiList)
    @login_required
    def list(request, project_id):
        if request.method != CommonData.Method.GET.value:
            data = CommonData.response_data(RequestMethodError, 'Method is invalid')
            return HttpResponse(json.dumps(data), content_type='application/json')

        limit = 10
        page = 1
        if 'limit' in request.GET.keys():
            limit = int(request.GET['limit'])
        if 'current_page' in request.GET.keys():
            page = int(request.GET['current_page'])

        offset = (page - 1) * limit

        apis = ApiDao.get_apis_with_project_id(project_id, offset, limit)
        apis_dict = []
        for api in apis:
            api_dic = api.as_dict()
            project_dic = ProjectDao.get_project_with_api_id(api.api_id)
            if project_dic is not None:
                api_dic['project'] = project_dic
            apis_dict.append(api_dic)

        count = ApiDao.get_apis_count_with_project_id(project_id)
        data = CommonData.response_data(Success, 'Success')

        data['apis_data'] = {'apis': apis_dict,
                             'current_page': page,
                             'total': count,
                             'limit': limit}
        return HttpResponse(json.dumps(data, default=datetime2string), content_type='application/json')

    @track(ActionType.ApiFetch)
    @login_required
    def fetch(request):
        if request.method != CommonData.Method.GET.value:
            response = Response(RequestMethodError, 'Method is invalid', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        if 'project_id[]' not in request.GET.keys():
            response = Response(MissingParametersError, 'Missing Parameters', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        project_ids = request.GET.getlist('project_id[]')

        apis_dics = []
        for project_id in project_ids:
            aList = list(ApiDao.get_all_apis_with_project_id(project_id))
            for api in aList:
                api['project_id'] = int(project_id)
                apis_dics.append(api)

        response = Response(Success,
                            'Success',
                            apis_dics)
        return HttpResponse(response.toJson(), content_type='application/json')

    @csrf_exempt
    @track(ActionType.ApiCreate)
    @login_required
    def create(request, project_id):
        if request.method != CommonData.Method.POST.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        form = ApiCreateForm(data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            model = Api()
            model.path = form.clean().get('path')
            if model.path.startswith('/', ):
                model.path = model.path[1:]
            model.method = form.clean().get('method')
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.status = form.clean().get('status')

            project = ProjectDao.get_project_with_id(project_id)
            res = ResTemplate()
            res.type = ResTemplate.Type.BelongsToProject.value
            res.name = uuid.uuid4()
            res.mimeType = ResTemplate.MIMEType.ApplicationJson.value
            res.responseJson = form.clean().get('responseJson')
            res.project = project
            result = ResTemplateDao.create(res)
            model.resTemplate = result

            api = ApiDao.create(model)

            project.apis.add(api)
            project.save()
            if api is None:
                response = Response(DaoOperationError,
                                    'API create failed',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
            else:
                response = Response(Success,
                                    'Success',
                                    model_to_dict(api))
                return HttpResponse(response.toJson(), content_type='application/json')
        else:
            return HttpResponse(Response.formParseErrorResponse().toJson(), content_type='application/json')

    @track(ActionType.ApiRepeatNameVerification)
    @login_required
    def repeat_name_verification(request, project_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        if ('path' not in request.GET.keys()) or \
                ('method' not in request.GET.keys()):
            response = Response(MissingParametersError,
                                'Missing Parameters',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')
        path = request.GET['path']
        method = request.GET['method']
        if path is None:
            return
        api = ApiDao.get_api(project_id, path, method)
        response = Response(Success,
                            'Success',
                            {})
        if api is None:
            response.data['repeatability'] = False
        else:
            response.data['api'] = api.as_dict()
            if 'api_id' in request.GET.keys():
                api_id = request.GET['api_id']
                if (str(api.api_id) == str(api_id)):
                    response.data['repeatability'] = False
                else:
                    response.data['repeatability'] = True
            else:
                response.data['repeatability'] = True
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ApiDetail)
    @login_required
    def detail(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        isOriginal = True
        if 'isOriginal' in request.GET.keys():
            isOriginal = False
        api = ApiDao.get_api_with_id(api_id=api_id)
        response = Response(Success,
                            'Success',
                            {})

        dic = api.as_dict()
        if isOriginal == False:
            dic['responseJson'] = json.loads(api.resTemplate.responseJson)
        else:
            dic['responseJson'] = api.resTemplate.responseJson
        response.data = dic
        return HttpResponse(response.toJson(), content_type='application/json')

    @csrf_exempt
    @track(ActionType.ApiUpdate)
    @login_required
    def update(request, project_id, api_id):
        if request.method != CommonData.Method.POST.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        form = ApiUpdateForm(data=request.POST)
        if form.is_valid():
            model = ApiDao.get_api_with_id(api_id)
            model.path = form.clean().get('path')
            if model.path.startswith('/', ):
                model.path = model.path[1:]
            model.method = form.clean().get('method')
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.status = form.clean().get('status')

            res = ResTemplateDao.get_private_res_template_with_api_id(api_id)
            res.responseJson = form.clean().get('responseJson')

            ResTemplateDao.update(res)
            result = ApiDao.update(model)

            if result is False:
                response = Response(DaoOperationError,
                                    'API update failed',
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

    @track(ActionType.ApiDelete)
    @login_required
    def delete(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        res = ResTemplateDao.get_private_res_template_with_api_id(api_id)
        success = ResTemplateDao.delete(res.res_template_id)
        if success:
            response = Response(Success,
                                'Success',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')
        else:
            response = Response(DaoOperationError,
                                'Delete Failed',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ApiStar)
    @login_required
    def star(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        api = ApiDao.get_api_with_id(api_id)
        if api is not None:
            api.star = not api.star

            result = ApiDao.update(api)
            if result is False:
                response = Response(DaoOperationError,
                                    'Update API Failed',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
            else:
                response = Response(Success,
                                    'Success',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
        else:
            response = Response(DaoOperationError,
                                'API is not exist',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ApiStarList)
    @login_required
    def starList(request):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        limit = 10
        page = 1
        if 'limit' in request.GET.keys():
            limit = int(request.GET['limit'])
        if 'current_page' in request.GET.keys():
            page = int(request.GET['current_page'])

        offset = (page - 1) * limit

        apis = ApiDao.get_all_stared_apis(offset, limit)
        apis_dict = []
        for api in apis:
            api_dic = api.as_dict()
            project_dic = ProjectDao.get_project_with_api_id(api.api_id)
            if project_dic is not None:
                api_dic['project'] = project_dic
            apis_dict.append(api_dic)
        count = ApiDao.get_stared_apis_count()
        response = Response(Success,
                            'Success',
                            {'apis': apis_dict,
                             'current_page': page,
                             'total': count,
                             'limit': limit})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ApiBatchUpdateStatus)
    @login_required
    def batch_update_status(request):
        if request.method != CommonData.Method.GET.value:
            response = Response(RequestMethodError, 'Method is invalid', {})
            return HttpResponse(response.toJson(), content_type='application/json')
        if 'api_ids[]' not in request.GET.keys():
            response = Response(MissingParametersError, 'Missing Parameters', {})
            return HttpResponse(response.toJson(), content_type='application/json')
        if ('status' not in request.GET.keys()):
            response = Response(MissingParametersError, 'Has no param "status"', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        status = int(request.GET['status'])
        enum_list = [e.value for e in Api.Status]
        if status not in enum_list:
            response = Response(MissingParametersError, 'status 参数错误', {})
            return HttpResponse(response.toJson(), content_type='application/json')
        api_ids = request.GET.getlist('api_ids[]')
        for api_id in api_ids:
            api = ApiDao.get_api_with_id(api_id)
            if api is not None:
                api.status = status
                ApiDao.update(api)
        response = Response(Success,
                            'Success',
                            {})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ApiUpdateStatus)
    @login_required
    def update_status(request, project_id, api_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        if ('status' not in request.GET.keys()):
            response = Response(MissingParametersError, 'Has no param "status"', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        status = request.GET['status']
        api = ApiDao.get_api_with_id(api_id)
        if api is not None:
            api.status = status
            result = ApiDao.update(api)

            if result is False:
                response = Response(DaoOperationError,
                                    'Update API Failed',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
            else:
                response = Response(Success,
                                    'Success',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
        else:
            response = Response(DaoOperationError,
                                'API is not exist',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')

    def copy(request, api_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')
        if ('target_project_id' not in request.GET.keys()):
            response = Response(MissingParametersError, 'Has no param "status"', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        target_project_id = request.GET['target_project_id']

        api = ApiDao.get_api_with_id(api_id)
        result = ApiDao.get_api(target_project_id, api.path, api.method)
        if result is not None:
            response = Response(APIAlreadyExist,
                                '该项目下已存在相同 Method 和 Path 的 API',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')

        project = ProjectDao.get_project_with_id(target_project_id)

        new_api = Api()
        new_api.path = api.path
        new_api.method = api.method
        new_api.name = api.name
        new_api.note = api.note
        new_api.status = api.status


        original_res = ResTemplateDao.get_private_res_template_with_api_id(api_id)
        res = ResTemplate()
        res.type = original_res.type
        res.name = uuid.uuid4()
        res.mimeType = original_res.mimeType
        res.responseJson = original_res.responseJson
        res.project = project
        result = ResTemplateDao.create(res)

        new_api.resTemplate = result
        result_api = ApiDao.create(new_api)

        project.apis.add(result_api)
        project.save()
        if result_api is None:
            response = Response(DaoOperationError,
                                'API create failed',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')
        response = Response(Success,
                            'API copy success',
                            {})
        return HttpResponse(response.toJson(), content_type='application/json')
