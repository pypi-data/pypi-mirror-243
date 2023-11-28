from datetime import datetime


class RdTimeUtils:

    @staticmethod
    def get_current_time_seconds():
        return int(datetime.now().timestamp())