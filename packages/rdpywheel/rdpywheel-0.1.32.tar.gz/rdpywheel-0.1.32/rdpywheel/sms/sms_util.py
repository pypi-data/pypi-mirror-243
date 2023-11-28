import distutils
import os
from urllib.parse import urljoin, urlencode
import requests
from time import sleep

from rdpywheel.model.global_info import sys_logger
from rdpywheel.sms.cn_virt_msg import CnVirtMsg
from rdpywheel.sms.visa_test import VisaTest


class SMSUtil:

    def get_platform_vfs_code(self, phone_no: str, token: str):
        is_test_str = os.environ.get("SMS_TEST_ENABLE")
        # https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
        is_test_str_bool = bool(distutils.util.strtobool(is_test_str))
        if is_test_str_bool:
            return SMSUtil.query_test_vfs_code(phone_no)
        else:
            return SMSUtil.query_vfs_code(phone_no, token)

    def query_test_vfs_code(phone_no):
        i = 0
        sleep(10)
        code = None
        while True:
            i += 1
            msg = VisaTest.get_test_sms_msg(phone_no=phone_no)
            if msg and len(msg) > 0:
                code = SMSUtil.get_vfs_code(msg)
            sleep(5)
            if code:
                break
            if i > 6:
                return None
        return code

    def query_vfs_code(phone_no, token):
        i = 0
        sleep(10)
        code = None
        while True:
            i += 1
            msg = CnVirtMsg.get_sms_msg(token=token, phone_no=phone_no, key_word="VFS")
            if msg and len(msg) > 0:
                code = SMSUtil.get_vfs_code(msg)
            sleep(5)
            if code:
                break
            if i > 6:
                return None
        return code

    def get_vfs_code(text):
        start_index = text.find('>')
        end_index = text.find(' is')
        if start_index != -1 and end_index != -1:
            otp = text[start_index + 1:end_index]
            print("验证码:", otp)
            return otp

        start_index = text.find('】')
        end_index = text.find(' is')

        if start_index != -1 and end_index != -1:
            otp = text[start_index + 1:end_index]
            print("验证码:", otp)
            return otp
        else:
            print("未找到验证码.")
            return None

    def get_test_sms_msg(activationId: str):
        try:
            params = {
                "activationId": activationId
            }
            sms_base_url = "https://sms.poemhub.top/post/sms/v1/sms-active"  # os.environ.get("SMS_TEST_BASE_URL")
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.json()
            if data["statusCode"] == "200" and data["resultCode"] == "200":
                result = data["result"]
                return result["text"]
            return None
        except Exception as e:
            sys_logger.error("get test sms message error", e)

    if __name__ == '__main__':
        get_test_sms_msg(str(15683761628))
