from dal.models import Api
import datetime


class ApiDao:
    @staticmethod
    def create(model):
        api = Api.objects.create(path=model.path,
                                 method=model.method,
                                 name=model.name,
                                 note=model.note,
                                 status=model.status,
                                 resTemplate=model.resTemplate)
        return api

    @staticmethod
    def get_all_apis():
        apis = Api.objects.all()
        return apis

    @staticmethod
    def get_all_api_list():
        apis = list(ApiDao.get_all_apis().values('api_id',
                                                 'path',
                                                 'method',
                                                 'name',
                                                 'note',
                                                 'status',
                                                 'project'))
        return apis

    @staticmethod
    def get_all_stared_apis(offset, limit):
        apis = Api.objects.filter(star__exact=True).order_by('-createTime')[offset: offset + limit]
        return apis

    @staticmethod
    def get_stared_apis_count():
        result = Api.objects.filter(star__exact=True).order_by('-createTime').count()
        return result

    @staticmethod
    def get_api_with_id(api_id):
        try:
            api = Api.objects.get(api_id=api_id)
            return api
        except:
            return None

    @staticmethod
    def get_apis_with_project_id(project_id, offset, limit):
        apis = Api.objects.filter(project__project_id=project_id).order_by('-createTime')[offset: offset + limit]
        return apis

    @staticmethod
    def get_all_apis_with_project_id(project_id):
        apis = Api.objects.filter(project__project_id=project_id).order_by('-createTime').values('api_id',
                                                                                                 'path',
                                                                                                 'method',
                                                                                                 'name',
                                                                                                 'note',
                                                                                                 'status')
        return apis

    @staticmethod
    def get_apis_count_with_project_id(project_id):
        result = Api.objects.all().filter(project__project_id=project_id).count()
        return result

    @staticmethod
    def get_apis_with_project_id_and_path(project_id, path):
        apis = Api.objects.filter(project__project_id=project_id, path=path)
        return apis

    @staticmethod
    def get_api(project_id, path, method):
        try:
            api = Api.objects.get(project__project_id=project_id, path=path, method=method)
            return api
        except:
            return None

    @staticmethod
    def delete(api_id):
        deleted_count, _ = Api.objects.filter(api_id=api_id).delete()
        if deleted_count > 0:
            return True
        else:
            return False

    @staticmethod
    def delete_all(self):
        result = Api.objects.all().delete()

    @staticmethod
    def update(model):
        result = Api.objects.filter(api_id=model.api_id).update(path=model.path,
                                                                method=model.method,
                                                                name=model.name,
                                                                note=model.note,
                                                                status=model.status,
                                                                star=model.star,
                                                                resTemplate=model.resTemplate,
                                                                updateTime=datetime.datetime.now())
        if result > 0:
            return True
        else:
            return False
