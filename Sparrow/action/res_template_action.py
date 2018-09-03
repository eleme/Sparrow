from django.forms.models import model_to_dict
from dal.dao.res_template_dao import ResTemplateDao
from Sparrow.action.common_action import *
from Sparrow.forms import *
from dal.models import ResTemplate
from django.http.request import *
from Sparrow.action.track import track
from dal.models import *


class ResTemplateAction:
    @track(ActionType.ResTemplateList)
    def list(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        limit = 10
        page = 1
        if 'limit' in request.GET.keys():
            limit = int(request.GET['limit'])
        if 'current_page' in request.GET.keys():
            page = int(request.GET['current_page'])

        offset = (page - 1) * limit
        resTemplates = ResTemplateDao.get_all_public_res_template_list(offset, limit)
        count = ResTemplateDao.get_all_public_res_template_count()

        response = Response(Success,
                            'Success',
                            {'res_templates': resTemplates,
                             'current_page': page,
                             'total': count,
                             'limit': limit})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ResTemplateDetail)
    def detail(request: HttpRequest, res_template_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        isOriginal = True
        if 'isOriginal' in request.GET.keys():
            isOriginal = False
        res_template = ResTemplateDao.get_res_template_with_id(res_template_id)

        if isOriginal == False:
            res_template.responseJson = json.loads(res_template.responseJson)
        dic = model_to_dict(res_template)

        response = Response(Success,
                            'Success',
                            dic)
        return HttpResponse(response.toJson(), content_type='application/json')

    @csrf_exempt
    @track(ActionType.ResTemplateCreate)
    def create(request: HttpRequest):
        if request.method != CommonData.Method.POST.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        form = ResTemplateCreateForm(data=request.POST)
        if form.is_valid():
            model = ResTemplate()
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.type = form.clean().get('type')
            model.responseJson = form.clean().get('responseJson')
            resTemplate = ResTemplateDao.create(model)
            if resTemplate is None:
                response = Response(DaoOperationError,
                                    'Response template create failed',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
            else:
                response = Response(Success,
                                    'Success',
                                    model_to_dict(resTemplate))
                return HttpResponse(response.toJson(), content_type='application/json')
        else:
            return HttpResponse(Response.formParseErrorResponse().toJson(), content_type='application/json')

    @csrf_exempt
    @track(ActionType.ResTemplateUpdate)
    def update(request: HttpRequest, res_template_id):
        if request.method != CommonData.Method.POST.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        form = ResTemplateUpdateForm(data=request.POST)
        if form.is_valid():
            model = ResTemplateDao.get_res_template_with_id(res_template_id)
            model.name = form.clean().get('name')
            model.note = form.clean().get('note')
            model.mimeType = form.clean().get('mimeType')
            model.responseJson = form.clean().get('responseJson')
            result = ResTemplateDao.update(model)

            if result is False:
                response = Response(DaoOperationError,
                                    'Response template update failed',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
            else:
                response = Response(Success,
                                    'Success',
                                    {})
                return HttpResponse(response.toJson(), content_type='application/json')
        else:
            return HttpResponse(Response.formParseErrorResponse().toJson(), content_type='application/json')

    @track(ActionType.ResTemplateRepeatNameVerification)
    def repeat_name_verification(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        if ('name' not in request.GET.keys()):
            data = CommonData.response_data(MissingParametersError, '缺少参数')
            return HttpResponse(json.dumps(data), content_type='application/json')
        name = request.GET['name']
        resTemplate = ResTemplateDao.get_public_res_template_with_name(name)

        response = Response(Success,
                            'Success',
                            {})
        if resTemplate is None:
            response.data['repeatability'] = False
        else:
            response.data['resTemplate'] = resTemplate.as_dict()
            if 'res_template_id' in request.GET.keys():
                res_template_id = request.GET['res_template_id']
                if str(resTemplate.res_template_id) == str(res_template_id):
                    response.data['repeatability'] = False
                else:
                    response.data['repeatability'] = True
            else:
                response.data['repeatability'] = True

        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ResTemplateDelete)
    def delete(request: HttpRequest, res_template_id):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')

        success = ResTemplateDao.delete(res_template_id)
        if success:
            response = Response(Success,
                                'Success',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')
        else:
            response = Response(DaoOperationError,
                                'Delete template Failed',
                                {})
            return HttpResponse(response.toJson(), content_type='application/json')
