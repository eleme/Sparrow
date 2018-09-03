from dal.models import *
import datetime
from dal.dao.account_dao import AccountDao
from django.db.models import *
from datetime import timedelta, datetime
import re


class ActionDao:
    @staticmethod
    def add_action(action):
        action.save()

    @staticmethod
    def get_daily_active_info(total):
        infos = []
        counter = total - 1
        while counter >= 0:
            info = {}
            start_date = datetime.today() + timedelta(-counter - 1)
            end_date = datetime.today() + timedelta(-counter)
            info['日期'] = end_date
            visits = Action.objects.filter(create_time__gte=start_date, create_time__lt=end_date).values('id').count()
            info['访问量'] = visits
            mock_visits = Action.objects.filter(create_time__gte=start_date, create_time__lt=end_date,
                                                type=ActionType.Mock.value).values(
                'id').count()
            info['Mock次数'] = mock_visits
            infos.append(info)
            counter -= 1
        # result = Action.objects.annotate(日期=TruncDay('create_time')).values('日期').annotate(访问量=Count('id')).values(
        #     '日期', '访问量').order_by('日期')[:7]
        return list(infos)

    @staticmethod
    def get_top_active_users_info(limit):
        week_ago = datetime.today() + timedelta(-7)
        infos = Action.objects.filter(create_time__gte=week_ago).exclude(user_id__isnull=True).values(
            'user_id').annotate(
            count=Count('id')).order_by('-count')[:limit]
        for info in infos:
            user = AccountDao.get_userProfile_with_id(info['user_id'])
            info['username'] = user.user.username
        return list(infos)

    @staticmethod
    def get_top_active_apis_info(limit):
        week_ago = datetime.today() + timedelta(-7)
        infos = Action.objects.filter(create_time__gte=week_ago, type=ActionType.Mock.value).values(
            'request_info').annotate(
            count=Count('id')).order_by('-count')[:limit]
        for info in infos:
            request_info = info['request_info']
            method = str.split(request_info, ' ')[1]
            result = re.search("/mock/[^\s]*/[^\s]*'", request_info)
            path = result.group(0).replace("'", "")
            project_id = int(str.split(path, '/')[2])
            info['project_id'] = project_id
            # path = path.replace("/mock/", "").replace(str(project_id)+ "/", "")
            info['path'] = path
        return list(infos)
