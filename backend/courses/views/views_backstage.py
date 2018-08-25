from decimal import Decimal
import datetime

from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

from core.utils import get_backstage_page
from core.constants import ERROR, INFO, ACTION_TYPE
from courses.models import Course, Comment, Image, Hero
from admins.models import AdminLog


@permission_required('courses.view_course')
def get_course_list(request):
    codename = request.GET.get('codename', '')
    title = request.GET.get('title', '')

    courses = Course.objects.filter(
        codename__contains=codename,
        title__contains=title
    ).order_by('-updated_at')
    page = get_backstage_page(request, courses)
    page['title'] = title
    page['codename'] = codename
    return JsonResponse(page, safe=False)


@permission_required('courses.view_course')
def get_course_detail(request):
    course_id = request.GET.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    return JsonResponse(
        {
            'course_id': course.id,
            'codename': course.codename,
            'title': course.title,
            'up_votes': course.up_votes.count(),
            'expire_duration': course.expire_duration,
            'price': course.price,
            'reward_percent': course.reward_percent,
            'created_at': course.created_at,
            'updated_at': course.updated_at,
            'description': course.description
        }
    )


@permission_required('courses.delete_course')
def delete_course(request):
    course_id = request.POST.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['delete_course'],
        object_id=course_id
    )

    course.delete()
    return JsonResponse({'message': INFO['object_deleted']})


@permission_required('courses.add_course')
def add_course(request):
    title = request.POST.get('title')
    codename = request.POST.get('codename')
    expire_duration = datetime.timedelta(
        days=int(request.POST.get('days')),
        hours=int(request.POST.get('hours'))
    )
    price = float(request.POST.get('price'))
    can_comment = request.POST.get('can_comment') == '1'
    reward_percent = float(request.POST.get('reward_percent'))
    description = request.POST.get('description')
    images = request.FILES.getlist('images', [])
    audio = request.FILES.get('audio')
    load_times = request.POST.getlist('load_times', [])

    course = Course.objects.create(
        title=title,
        codename=codename,
        expire_duration=expire_duration,
        price=Decimal(price),
        can_comment=can_comment,
        reward_percent=Decimal(reward_percent),
        description=description,
        audio=audio,
    )

    for image in images:
        Image.objects.create(
            course=course,
            image_path=image,
            load_time=int(float(load_times[images.index(image)]))
        )

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['add_course'],
        object_id=course.id
    )
    return JsonResponse({'message': INFO['success']})


@permission_required('courses.delete_image')
def delete_course_images(request):
    delete_list = request.POST.getlist('delete_list', [])

    deleted = []
    for image_id in delete_list:
        try:
            image = Image.objects.get(id=int(image_id))
            image.delete()
            deleted.append(int(image_id))
        except Image.DoesNotExist:
            pass
    return JsonResponse(
        {
            'deleted': deleted
        }
    )


@permission_required('courses.change_course')
def edit_course(request):
    course_id = request.POST.get('course_id')

    try:
        course = Course.objects.get(id=str(course_id))
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    course.title = request.POST.get('title')
    course.codename = request.POST.get('codename')
    course.expire_duration = datetime.timedelta(
        days=int(request.POST.get('days')),
        hours=int(request.POST.get('hours'))
    )
    course.price = Decimal(float(request.POST.get('price')))
    course.can_comment = request.POST.get('can_comment') == '1'
    course.reward_percent = Decimal(float(request.POST.get('reward_percent')))
    course.description = request.POST.get('description')
    audio = request.FILES.get('audio')
    if audio is not None:
        course.audio = audio
    course.save()
    image_files = request.FILES.getlist('image_files', [])
    image_ids = request.POST.getlist('image_ids', [])
    load_times_files = request.POST.getlist('load_times_files', [])
    load_times_ids = request.POST.getlist('load_times_ids', [])

    for image in image_files:
        Image.objects.create(
            course=course,
            image_path=image,
            load_time=int(float(load_times_files[image_files.index(image)]))
        )

    for image_id in image_ids:
        image = Image.objects.get(id=str(image_id))
        image.load_time = int(float(load_times_ids[image_ids.index(image_id)]))
        image.save()

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['update_course'],
        object_id=course.id
    )
    return JsonResponse({'message': INFO['success']})


@permission_required('courses.change_course')
def get_course_assets(request):
    course_id = request.GET.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    images = Image.objects.filter(course=course).all().order_by('load_time')
    json_data = {
        'course_id': course.id,
        'title': course.title,
        'codename': course.codename,
        'expire_duration': course.expire_duration.total_seconds(),
        'price': course.price,
        'can_comment': course.can_comment,
        'reward_percent': course.reward_percent,
        'description': course.description,
        'audio': str(course.audio),
        'images': []
    }
    for image in images:
        json_data['images'].append(image.as_dict())

    return JsonResponse(json_data)


@permission_required('courses.view_comment')
def get_comment_list(request):
    username = request.GET.get('username', '')
    course_codename = request.GET.get('course_codename', '')
    course_title = request.GET.get('course_title', '')
    is_deleted = request.GET.get('is_deleted', '0')

    comments = Comment.all_objects.filter(
        user__username__contains=username,
        course__codename__contains=course_codename,
        course__title__contains=course_title,
    ).order_by('-created_at')
    if is_deleted == '1':
        comments = comments.filter(deleted_at=None)
    elif is_deleted == '2':
        comments = comments.exclude(deleted_at=None)

    page = get_backstage_page(request, comments)
    page['username'] = username
    page['course_codename'] = course_codename
    page['course_title'] = course_title
    page['is_deleted'] = is_deleted
    return JsonResponse(page, safe=False)


@permission_required('courses.view_comment')
def get_comment_detail(request):
    comment_id = request.GET.get('comment_id')

    try:
        comment = Comment.all_objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    return JsonResponse(
        {
            'comment_id': comment.id,
            'created_at': comment.created_at,
            'username': comment.user.username,
            'course_codename': comment.course.codename,
            'course_title': comment.course.title,
            'is_deleted': comment.deleted_at is not None,
            'deleted_at': comment.deleted_at,
            'up_votes': comment.up_votes.count(),
            'down_votes': comment.down_votes.count(),
            'content': comment.content
        }
    )


@permission_required('courses.add_comment')
def add_comment(request):
    reply_to_id = request.POST.get('reply_to_id', '-1')
    comment_content = request.POST.get('comment_content')

    try:
        reply_to = Comment.objects.get(id=int(reply_to_id))
    except Comment.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    course = reply_to.course
    if not course.can_comment:
        return JsonResponse({'message': ERROR['comment_not_allowed']}, status=403)

    reply = Comment.objects.create(
        user=request.user,
        course=course,
        content=comment_content,
        parent=reply_to
    )

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['reply_comment'],
        new_data=reply_to.id,
        object_id=reply.id
    )

    return JsonResponse({'message': INFO['success']})


@permission_required('courses.delete_comment')
def delete_comment(request):
    comment_id = request.POST.get('comment_id')

    try:
        comment = Comment.objects.get(id=comment_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['delete_comment'],
        object_id=comment_id
    )

    comment.delete()
    return JsonResponse({'message': INFO['object_deleted']})


@permission_required('courses.add_hero')
def add_hero(request):
    heroes = request.FILES.getlist('heroes', [])
    captions = request.POST.getlist('captions', [])

    for hero in heroes:
        Hero.objects.create(
            image=hero,
            caption=captions[heroes.index(hero)]
        )

    return JsonResponse({'message': INFO['success']})


@permission_required('courses.delete_hero')
def delete_hero(request):
    delete_list = request.POST.getlist('delete_list', [])

    deleted = []
    for hero_id in delete_list:
        try:
            Hero.objects.get(id=int(hero_id)).delete()
            deleted.append(int(hero_id))
        except Hero.DoesNotExist:
            pass

    return JsonResponse(
        {
            'deleted': deleted
        }
    )
