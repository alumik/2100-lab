# pylint: disable=E0401

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

def tencent_cloud_message(phone_number, verification_code):
    appid = 1400131309
    appkey = "7901df2b3113f98f1a9ad266ca07c9db"
    phone_numbers = phone_number
    template_id = 178579
    sms_sign = "南开软小依"
    ssender = SmsSingleSender(appid, appkey)
    params = [verification_code, '5']
    try:
        result = ssender.send_with_param(86, phone_numbers,
                                         template_id, params, sign=sms_sign, extend="",
                                         ext="")
    except HTTPError as error:
        print(error)
    except Exception as error:
        print(error)

    print(result)
