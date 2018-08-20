from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse


def get_page(request, items):
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


def get_back_stage_page(request, items):
    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.GET.get('page_limit', 10))
    try:
        item_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        item_page = paginator.page(1)
    item_list = list(
        map(lambda item: item.as_back_stage_dict(), list(item_page))
    )
    return {
        'count': count,
        'page': item_page.number,
        'num_pages': paginator.num_pages,
        'content': item_list
    }