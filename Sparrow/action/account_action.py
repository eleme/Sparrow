from django.forms.models import model_to_dict
from Sparrow.action.common_action import *
from django.contrib import auth
from dal.dao.account_dao import AccountDao
from dal.dao.quick_login_record_dao import QuickLoginRecordDao
from django.contrib.auth.decorators import login_required
from Sparrow.action.response import *
from django.http.request import *
from Sparrow.action.track import track
from dal.models import *
import uuid
from datetime import datetime, timezone


class AccountAction:
    @csrf_exempt
    @track(ActionType.AccountLogin)
    def login(request: HttpRequest):
        # if request.user.is_authenticated():ss
        #     data = CommonData.response_data(Success, 'Success')

        # body = bytes.decode(request.body)
        # loginData = json.loads(body)

        username = request.POST['username']
        password = request.POST['password']

        print('用户 ' + username + ' 尝试登录')

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            accountInfo = User.objects.get(id=user.id)
            response = Response(Success, 'Success', {'id': accountInfo.id,
                                                     'username': accountInfo.username,
                                                     'email': accountInfo.email})
            return HttpResponse(response.toJson(), content_type='application/json')
        else:
            response = Response(LoginFailed, 'Login failed', {})
            return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.AccountQuickLogin)
    def quick_login(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')
        user_id = request.GET.get('user_id')
        verification_code = request.GET.get('verification_code')

        record = QuickLoginRecordDao.get_record_with_verification_code(verification_code)
        if record is None:
            response = Response(QuickLoginFailed, '验证码不存在或已过期', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        now = datetime.now(timezone.utc)
        offset = (now - record.update_time).seconds

        if offset > 60:
            response = Response(QuickLoginFailed, '验证码已过期', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        user = AccountDao.get_user_with_id(user_id)
        if user is None:
            response = Response(QuickLoginFailed, '用户不存在', {})
            return HttpResponse(response.toJson(), content_type='application/json')
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        print('用户 ' + user.username + ' 尝试登录')
        auth.login(request, user)
        accountInfo = User.objects.get(id=user.id)
        response = Response(Success, 'Success', {'id': accountInfo.id,
                                                 'username': accountInfo.username,
                                                 'email': accountInfo.email})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.AccountRequestQuickLogin)
    def request_quick_login(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            return HttpResponse(Response.methodInvalidResponse().toJson(), content_type='application/json')
        user = request.user
        r = QuickLoginRecordDao.get_record_with_user_id(user.id)
        if r is not None:
            r.verification_code = str(uuid.uuid4())
            QuickLoginRecordDao.update_record(r)
            response = Response(Success, 'Success', {'verification_code': r.verification_code})
            return HttpResponse(response.toJson(), content_type='application/json')
        else:
            record = QuickLoginRecord()
            record.user = user
            record.verification_code = str(uuid.uuid4())
            QuickLoginRecordDao.add_record(record)
            response = Response(Success, 'Success', {'verification_code': record.verification_code})
            return HttpResponse(response.toJson(), content_type='application/json')


    @login_required
    @csrf_exempt
    @track(ActionType.AccountLogout)
    def logout(request: HttpRequest):
        auth.logout(request)
        response = Response(Success, 'Success', {})
        return HttpResponse(response.toJson(), content_type='application/json')

    def redirect_login(request: HttpRequest):
        response = Response(NeedLogin, 'Need Login', {})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.AccountCheckStatus)
    @login_required
    def check_status(request: HttpRequest):
        response = Response(Success, 'Has logged', {})
        return HttpResponse(response.toJson(), content_type='application/json')

    @track(ActionType.AccountSearch)
    def search(request: HttpRequest):
        if request.method != CommonData.Method.GET.value:
            response = Response(RequestMethodError, 'Method is invalid', {})
            return HttpResponse(response.toJson(), content_type='application/json')

        users = AccountDao.get_users_with_username(request.GET['username'])
        response = Response(Success, 'Success', users)
        return HttpResponse(response.toJson(), content_type='application/json')
