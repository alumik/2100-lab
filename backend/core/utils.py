from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse


def get_page(request, items):
    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.POST.get('page_limit'))
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
            'content': item_list
        },
        safe=False
    )
