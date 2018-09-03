import json
import datetime


def datetime2string(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def datetime2string_mm_dd(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%m-%d')


Success = 200
LoginFailed = 900
NeedLogin = 901
QuickLoginFailed = 902

APINotExist = 1000
FormParseError = 1001
DaoOperationError = 1002
RequestMethodError = 1003
RequestParamsError = 1004
MissingParametersError = 1005
APINotOpenMock = 1006
APIAlreadyExist = 1007


class Response(object):
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def toJson(self):
        return json.dumps(self.__dict__, default=datetime2string, ensure_ascii=False)

    def to_json_with_mm_dd(self):
        return json.dumps(self.__dict__, default=datetime2string_mm_dd)

    @staticmethod
    def methodInvalidResponse():
        response = Response(RequestMethodError, 'Method is invalid', {})
        return response

    @staticmethod
    def successResponse():
        response = Response(Success, 'Success', {})
        return response

    @staticmethod
    def daoOperationErrorResponse():
        response = Response(DaoOperationError, 'DaoOperation error', {})
        return response

    @staticmethod
    def requestParamsErrorResponse():
        response = Response(RequestParamsError, 'RequestParams error', {})
        return response

    @staticmethod
    def formParseErrorResponse():
        response = Response(FormParseError, 'FormParse error', {})
        return response
