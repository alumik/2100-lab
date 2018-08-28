"""用户模块工具函数"""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


def tencent_cloud_message(phone_number, verification_code):
    """腾讯云发送短信接口"""

    appid = 1400131309
    appkey = "7901df2b3113f98f1a9ad266ca07c9db"
    phone_numbers = phone_number
    template_id = 178579
    sms_sign = "南开软小依"
    ssender = SmsSingleSender(appid, appkey)
    params = [verification_code, '5']
    try:
        ssender.send_with_param(
            86,
            phone_numbers,
            template_id,
            params,
            sign=sms_sign,
            extend="",
            ext=""
        )
    except HTTPError as error:
        raise HTTPError from error
    except Exception as error:
        raise Exception from error


def get_customer_page(request, items):
    """用户分页工具函数"""

    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.GET.get('page_limit', 10))
    try:
        item_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        item_page = paginator.page(1)
    item_list = list(
        map(lambda item: item.as_customer_dict(), list(item_page))
    )
    return {
        'count': count,
        'page': item_page.number,
        'num_pages': paginator.num_pages,
        'content': item_list
    }
