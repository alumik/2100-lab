from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse

from courses.models import Course, Hero


def get_page(request, items):
    count = items.count()
    page = request.POST.get('page')
    paginator = Paginator(items, request.POST.get('page_limit'))
    try:
        item_page = paginator.page(page)
    except PageNotAnInteger:
        item_page = paginator.page(request.POST.get('page'))
    except EmptyPage:
        item_page = paginator.page(paginator.num_pages)
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


def create_test_customers(count):
    for index in range(1, count + 1):
        get_user_model().objects.create_user(phone_number=str(index).zfill(11))


def create_test_heroes(count):
    for index in range(1, count + 1):
        Hero.objects.create(
            image='fake/path/image' + str(index) + '.png',
            caption='c' + str(index)
        )


def create_test_courses(count):
    for index in range(1, count + 1):
        Course.objects.create(
            title='t' + str(index),
            description='d' + str(index),
            codename='c' + str(index)
        )