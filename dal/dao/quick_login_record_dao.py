from dal.models import *
import datetime


class QuickLoginRecordDao:
    @staticmethod
    def add_record(record):
        record.save()

    @staticmethod
    def get_record_with_user_id(user_id):
        try:
            record = QuickLoginRecord.objects.get(user_id=user_id)
            return record
        except:
            return None

    @staticmethod
    def update_record(record):
        result = QuickLoginRecord.objects.filter(id=record.id).update(
            verification_code=record.verification_code,
            update_time=datetime.datetime.now())
        if result > 0:
            return True
        else:
            return False

    @staticmethod
    def get_record_with_verification_code(code):
        try:
            record = QuickLoginRecord.objects.get(verification_code=code)
            return record
        except:
            return None
