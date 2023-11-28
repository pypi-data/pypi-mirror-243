import jwt
from rdpywheel.utils.rd_time_utils import RdTimeUtils


class JwtHandler:

    @staticmethod
    def token_is_expire(access_token):
        parsed_token = jwt.decode(access_token,
                                  verify=False,
                                  algorithms=['HS512'],
                                  options={
                                      'verify_signature': False
                                  })
        exp = parsed_token["exp"]
        now = RdTimeUtils.get_current_time_seconds()
        if now - 500 > exp:
            return True
        else:
            return False
