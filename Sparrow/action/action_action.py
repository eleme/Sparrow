from django.forms.models import model_to_dict
from Sparrow.action.common_action import *
from dal.dao.action_dao import ActionDao
from django.contrib.auth.decorators import login_required
from Sparrow.action.response import *
from django.http.request import *
from Sparrow.action.track import track
from dal.models import *


class ActionAction:
    @track(ActionType.ActionDailyActiveInfo)
    def daily_active_info(request: HttpRequest):
        daily_active_info = ActionDao.get_daily_active_info(14)
        response = Response(Success, 'Success', daily_active_info)
        return HttpResponse(response.to_json_with_mm_dd(), content_type='application/json')

    @track(ActionType.ActionTopActiveUserInfo)
    def top_active_users_info(request: HttpRequest):
        top_active_users_info = ActionDao.get_top_active_users_info(10)
        response = Response(Success, 'Success', top_active_users_info)
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.ActionTopActiveApisInfo)
    def top_active_apis_info(request: HttpRequest):
        top_active_apis_info = ActionDao.get_top_active_apis_info(10)
        response = Response(Success, 'Success', top_active_apis_info)
        return HttpResponse(response.toJson(), content_type='application/json')