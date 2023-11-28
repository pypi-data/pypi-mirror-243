import os
from urllib.parse import urljoin, urlencode
import requests


class VisaTest:

    def get_test_sms_msg(phone_no: str):
        try:
            params = {
                "activationId": phone_no
            }
            sms_base_url = "https://sms.poemhub.top/post/sms/v1/sms-active" #os.environ.get("SMS_TEST_BASE_URL")
            url = urljoin(sms_base_url, "?" + urlencode(params))
            response = requests.get(url=url, timeout=10)
            data = response.json()
            if data["statusCode"] == "200" and data["resultCode"] == "200":
                result = data["result"]
                return result["text"]
            return None
        except Exception as e:
            print(e)

    if __name__ == '__main__':
        get_test_sms_msg(str(15683761628))
