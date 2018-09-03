from dal.models import ResTemplate
from dal.models import Api
from dal.dao.api_dao import ApiDao
import datetime


class ResTemplateDao:
    @staticmethod
    def create(model):
        res_template = ResTemplate.objects.create(name=model.name,
                                                  note=model.note,
                                                  type=model.type,
                                                  mimeType=model.mimeType,
                                                  responseJson=model.responseJson,
                                                  project=model.project)
        return res_template

    @staticmethod
    def get_all_public_res_templates(offset, limit):
        res_templates = ResTemplate.objects.filter(type=ResTemplate.Type.Public.value).order_by('-updateTime')[offset: offset + limit].values(
            'res_template_id',
            'name',
            'note',
            'mimeType',
            'responseJson',
            'updateTime')
        return res_templates

    @staticmethod
    def get_all_public_res_template_count():
        result = ResTemplate.objects.filter(type=ResTemplate.Type.Public.value).values('res_template_id').count()
        return result

    @staticmethod
    def get_all_public_res_template_list(offset, limit):
        res_templates = list(ResTemplateDao.get_all_public_res_templates(offset, limit))
        return res_templates

    @staticmethod
    def get_res_template_with_id(id):
        res_templates = ResTemplate.objects.get(res_template_id=id)
        return res_templates

    @staticmethod
    def get_res_templates_with_project_id(project_id):
        res_templates = ResTemplate.objects.filter(project__project_id=project_id)
        return res_templates

    @staticmethod
    def get_public_res_template_with_name(name):
        try:
            res_templates = ResTemplate.objects.filter(name=name)
            return res_templates.first()
        except:
            return None

    @staticmethod
    def get_private_res_template_with_api_id(api_id):
        try:
            api = ApiDao.get_api_with_id(api_id)
            if api is None:
                return None
            res = api.resTemplate
            return res
        except:
            return None

    @staticmethod
    def delete(res_template_id):
        deleted_count, _ = ResTemplate.objects.filter(res_template_id=res_template_id).delete()
        if deleted_count > 0:
            return True
        else:
            return False

    @staticmethod
    def update(model):
        result = ResTemplate.objects.filter(res_template_id=model.res_template_id).update(
            name=model.name,
            note=model.note,
            type=model.type,
            mimeType=model.mimeType,
            responseJson=model.responseJson,
            updateTime=datetime.datetime.now())
        if result > 0:
            return True
        else:
            return False
