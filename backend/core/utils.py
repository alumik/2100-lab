"""核心功能工具函数"""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse


def get_page(request, items):
    """分页工具函数"""

    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.GET.get('page_limit', 10))
    try:
        item_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        item_page = paginator.page(1)
    item_list = list(
        map(lambda item: item.as_dict(), list(item_page))
    )
    return JsonResponse(
        {
            'count': count,
            'page': item_page.number,
            'num_pages': paginator.num_pages,
            'content': item_list
        },
        safe=False
    )


def get_backstage_page(request, items):
    """后台分页工具函数"""

    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.GET.get('page_limit', 10))
    try:
        item_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        item_page = paginator.page(1)
    item_list = list(
        map(lambda item: item.as_backstage_dict(), list(item_page))
    )
    return {
        'count': count,
        'page': item_page.number,
        'num_pages': paginator.num_pages,
        'content': item_list
    }


def get_brief_page(request, items):
    """简短信息分页工具函数"""

    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.GET.get('page_limit', 10))
    try:
        item_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        item_page = paginator.page(1)
    item_list = list(
        map(lambda item: item.as_brief_dict(), list(item_page))
    )
    return JsonResponse(
        {
            'count': count,
            'page': item_page.number,
            'num_pages': paginator.num_pages,
            'content': item_list
        },
        safe=False
    )
