from django.views.decorators.csrf import csrf_exempt
from dal.dao.api_dao import ApiDao
import Sparrow._const
from django.shortcuts import render
from django.http import HttpResponse
from Sparrow.action.response import *
from Sparrow.action.track import track
from dal.models import *
import uuid
from dal.dao.res_template_dao import ResTemplateDao


def datetime2string(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class CommonData(object):
    def response_data(code, message):
        dic = {'code': code, 'message': message}
        return dic

    @unique
    class Method(Enum):
        GET = 'GET'
        POST = 'POST'


def index(request):
    context = {}
    return render(request, 'index.html', context)


@csrf_exempt
@track(ActionType.Mock)
def mock(request, project_id, path):
    method = str(request.method)
    api = ApiDao.get_api(project_id, path, method)

    if api is None:
        response = Response(APINotExist, '该 Method 的 API 不存在', {})
        return HttpResponse(response.toJson(), content_type='application/json')
    if api.status != Api.Status.Mock.value:
        response = Response(APINotOpenMock, '该 API 没有开启 Mock', {})
        return HttpResponse(response.toJson(), content_type='application/json')

    data = json.loads(api.resTemplate.responseJson)
    return HttpResponse(json.dumps(data), content_type='application/json')


def move(request):
    apis = ApiDao.get_all_api_list()
    response = Response(Success,
                        'Success',
                        list(apis))
    for api in apis:
        res = ResTemplate()
        res.name = uuid.uuid4()
        res.mimeType = 0
        res.responseJson = api['responseJson']
        res.type = ResTemplate.Type.BelongsToProject.value

        project = Project.objects.get(project_id=int(api['project']))

        project.save()
        res.project = project
        result = ResTemplateDao.create(res)
        a = ApiDao.get_api_with_id(api['api_id'])
        a.resTemplate = result
        a.save()
    return HttpResponse(response.toJson(), content_type='application/json')
