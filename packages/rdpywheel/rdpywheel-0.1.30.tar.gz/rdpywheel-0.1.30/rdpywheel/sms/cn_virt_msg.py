import os
from urllib.parse import urljoin, urlencode
import requests
from rdpywheel.model.global_info import sys_logger


class CnVirtMsg:
    def get_sms_phone_number(token: str):
        try:
            params = {
                "code": "getPhone",
                "token": token,
                "cardType": "实卡"
            }
            sms_base_url = os.environ.get("CN_VIRTUAL_BASE_URL")
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.content
            string_data = data.decode('utf-8')
            return string_data
        except Exception as e:
            sys_logger.error("get sms phone facing error", e)

    def get_sms_msg(token: str, phone_no: str, key_word: str):
        try:
            params = {
                "code": "getMsg",
                "token": token,
                "phone": phone_no,
                "keyWord": key_word
            }
            sms_base_url = os.environ.get("CN_VIRTUAL_BASE_URL")
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.content
            string_data = data.decode('utf-8')
            return string_data
        except Exception as e:
            sys_logger.error("get sms message error", e)

    def block_phone(token: str, phone_no: str):
        try:
            params = {
                "code": "block",
                "token": token,
                "phone": phone_no,
            }
            sms_base_url = os.environ.get("CN_VIRTUAL_BASE_URL")
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.content
            string_data = data.decode('utf-8')
            return string_data
        except Exception as e:
            sys_logger.error("get block phone error", e)
