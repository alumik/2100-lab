"""课程模块后台操作"""

from decimal import Decimal
import datetime

from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError
from django.http import JsonResponse

from admins.models import AdminLog
from core.constants import ERROR, INFO, ACTION_TYPE
from core.utils import get_backstage_page
from courses.models import Course, Comment, Image, Hero


@permission_required('courses.view_course')
def get_course_list(request):
    """获取课程列表

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/get-course-list/

    **传入参数**

    ========== ==== ==================
    参数       方法 说明
    ========== ==== ==================
    page       GET  当前页码
    page_limit GET  每页最大显示数量
    codename   GET  筛选参数：课程代码
    title      GET  筛选参数：课程名
    ========== ==== ==================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            codename: '',                                          // 筛选参数：课程代码
            title: '',                                             // 筛选参数：课程名
            count: 2,                                              // 总条数
            page: 2,                                               // 当前页码
            num_pages: 1,                                          // 总页数
            content: [
                {
                    course_id: 1,                                  // 课程ID
                    codename: 'SOFT001',                           // 课程代码
                    title: 'Data Structure',                       // 课程名
                    price: '100.00',                               // 价格
                    updated_at: '2018-08-31 16:46:44.794596+00:00' // 修改时间
                },
                ...
            ]
        }

    """

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
    """获取课程详情

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/get-course-detail/

    **传入参数**

    ========= ==== ======
    参数      方法 说明
    ========= ==== ======
    course_id GET  课程ID
    ========= ==== ======

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            course_id: 1,                                   // 课程ID
            codename: 'SOFT001',                            // 课程代码
            title: 'Data Structure',                        // 课程名
            up_votes: 1,                                    // 点赞数
            expire_duration: 86400,                         // 课程时效
            price: '100.00',                                // 价格
            reward_percent: '0.50',                         // 奖励金比例
            created_at: '2018-08-31 16:46:44.794596+00:00', // 创建日期
            updated_at: '2018-08-31 16:46:44.794596+00:00', // 修改日期
            description: '...'                              // 简介
        }

    """

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
    """删除课程

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/delete-course/

    **传入参数**

    ========= ==== ======
    参数      方法 说明
    ========= ==== ======
    course_id POST 课程ID
    ========= ==== ======

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Object deleted.'
        }

    """

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
    """添加课程

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/add-course/

    **传入参数**

    ================ ==== ==============
    参数             方法 说明
    ================ ==== ==============
    title            POST 课程名
    codename         POST 课程代码
    days             POST 课程时效天数
    hours            POST 课程时效小时数
    price            POST 价格
    can_comment      POST 能否评论
    reward_percent   POST 奖励金比例
    description      POST 简介
    images           POST 图片文件
    audio            POST 音频文件
    load_times       POST 加载时间
    thumbnail        POST 缩略图
    ================ ==== ==============

    **返回值**

    HTTP400：数据库错误

    .. code-block:: javascript

        {
            message: 'Database integrity error.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

    title = request.POST.get('title')
    codename = request.POST.get('codename')
    expire_duration = datetime.timedelta(
        days=int(request.POST.get('days', '0')),
        hours=int(request.POST.get('hours', '0'))
    )
    price = float(request.POST.get('price', '0.00'))
    can_comment = request.POST.get('can_comment') == '1'
    reward_percent = float(request.POST.get('reward_percent', '0.00'))
    description = request.POST.get('description')
    images = request.FILES.getlist('images', [])
    audio = request.FILES.get('audio', '')
    load_times = request.POST.getlist('load_times', [])
    thumbnail = request.FILES.get('thumbnail', '')

    try:
        course = Course.objects.create(
            title=title,
            codename=codename,
            expire_duration=expire_duration,
            price=Decimal(price),
            can_comment=can_comment,
            reward_percent=Decimal(reward_percent),
            description=description,
            audio=audio,
            thumbnail=thumbnail
        )
    except IntegrityError:
        return JsonResponse({'message': ERROR['integrity_error']}, status=400)

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


@permission_required('courses.change_course')
def edit_course(request):
    """编辑课程

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/edit-course/

    **传入参数**

    ================ ==== ==============
    参数             方法 说明
    ================ ==== ==============
    course_id        POST 课程ID
    title            POST 课程名
    codename         POST 课程代码
    days             POST 课程时效天数
    hours            POST 课程时效小时数
    price            POST 价格
    can_comment      POST 能否评论
    reward_percent   POST 奖励金比例
    description      POST 简介
    audio            POST 音频文件
    thumbnail        POST 缩略图
    image_files      POST 图片文件
    image_ids        POST 图片ID
    load_times_files POST 加载时间文件
    load_times_ids   POST 加载时间ID
    ================ ==== ==============

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

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
    thumbnail = request.FILES.get('thumbnail')
    if thumbnail is not None:
        course.thumbnail.delete()
        course.thumbnail = thumbnail
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


@permission_required('courses.delete_image')
def delete_course_images(request):
    """删除课程图片

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/delete-course-images/

    **传入参数**

    =========== ==== ==================
    参数        方法 说明
    =========== ==== ==================
    delete_list POST 要删除的图片ID列表
    =========== ==== ==================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            deleted: [ // 已删除的图片ID列表
                1,
                ...
            ]
        }

    """

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
def get_course_assets(request):
    """获取课程播放资源

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/get-course-assets/

    **传入参数**

    ========= ==== ======
    参数      方法 说明
    ========= ==== ======
    course_id GET  课程ID
    ========= ==== ======

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            course_id: 1,                        // 课程ID
            title: 'Data Structure',             // 课程名
            codename: 'SOFT001',                 // 课程代码
            expire_duration: 86400,              // 课程时效
            price: '100.00',                     // 价格
            can_comment: true,                   // 能否评论
            reward_percent: '0.50',              // 奖励金比例
            description: '...',                  // 简介
            audio: 'uploads/1.mp3',              // 课程音频
            thumbnail: 'uploads/1.png',          // 缩略图
            'images': [                          // 课程图片
                {
                    image_id: 1,                 // 图片ID
                    image_path: 'uploads/1.png', // 图片路径
                    load_time: 100               // 图片载入时间
                },
                ...
            ]
        }

    """

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
        'thumbnail': str(course.thumbnail),
        'images': []
    }
    for image in images:
        json_data['images'].append(image.as_dict())

    return JsonResponse(json_data)


@permission_required('courses.view_comment')
def get_comment_list(request):
    """获取留言列表

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/comment-management/get-comment-list/

    **传入参数**

    =============== ==== ====================
    参数            方法 说明
    =============== ==== ====================
    page            GET  当前页码
    page_limit      GET  每页最大显示数量
    username        GET  筛选参数：用户名
    course_codename GET  筛选参数：课程代码
    course_title    GET  筛选参数：课程名
    is_deleted      GET  筛选参数：是否被删除
    =============== ==== ====================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            username: '',                                           // 筛选参数：用户名
            course_codename: '',                                    // 筛选参数：课程代码
            course_title: '',                                       // 筛选参数：课程名
            is_deleted: '0',                                        // 筛选参数：是否被删除
            count: 2,                                               // 总条数
            page: 2,                                                // 当前页码
            num_pages: 1,                                           // 总页数
            content: [
                {
                    comment_id: 1,
                    created_at: '2018-08-31 16:46:44.794596+00:00', // 创建时间
                    username: 'John',                               // 用户名
                    course_codename: 'SOFT001',                     // 课程代码
                    course_title: 'Data Structure',                 // 课程名
                    content: '...',                                 // 留言内容
                    is_deleted: false                               // 是否被删除
                },
                ...
            ]
        }

    """

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
    """获取留言详情

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/comment-management/get-comment-detail/

    **传入参数**

    ========== ==== ======
    参数       方法 说明
    ========== ==== ======
    comment_id GET  留言ID
    ========== ==== ======

    **返回值**

    HTTP404：留言未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            comment_id: 1,                                  // 留言ID
            created_at: '2018-08-31 16:46:44.794596+00:00', // 创建时间
            username: 'John',                               // 用户名
            course_codename: 'SOFT001',                     // 课程代码
            course_title: 'Data Structure',                 // 课程名
            is_deleted: false,                              // 是否已删除
            deleted_at: null,                               // 删除时间
            up_votes: 1,                                    // 点赞数
            down_votes: 0,                                  // 点踩数
            content: '...'                                  // 内容
        }

    """

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
    """回复评论

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/comment-management/add-comment/

    **传入参数**

    =============== ==== ==============
    参数            方法 说明
    =============== ==== ==============
    reply_to_id     POST 要回复的评论ID
    comment_content POST 回复内容
    =============== ==== ==============

    **返回值**

    HTTP404：留言未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP403：课程禁止评论

    .. code-block:: javascript

        {
            message: 'Commenting is not allowed.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

    reply_to_id = request.POST.get('reply_to_id', '-1')
    comment_content = request.POST.get('comment_content')

    try:
        reply_to = Comment.objects.get(id=int(reply_to_id))
    except Comment.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    course = reply_to.course
    if not course.can_comment:
        return JsonResponse(
            {'message': ERROR['comment_not_allowed']},
            status=403
        )

    reply = Comment.objects.create(
        user=request.user,
        course=course,
        content=comment_content
    )
    if reply_to.parent is None:
        reply.parent = reply_to
    else:
        reply.parent = reply_to.parent
    reply.save()

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['reply_comment'],
        new_data=reply_to.id,
        object_id=reply.id
    )

    return JsonResponse({'message': INFO['success']})


@permission_required('courses.delete_comment')
def delete_comment(request):
    """删除留言

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/comment-management/delete-comment/

    **传入参数**

    ========== ==== ======
    参数       方法 说明
    ========== ==== ======
    comment_id POST 留言ID
    ========== ==== ======

    **返回值**

    HTTP404：留言未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Object deleted.'
        }

    """

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
    """添加头图

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/add-hero/

    **传入参数**

    ======== ==== ========
    参数     方法 说明
    ======== ==== ========
    heroes   POST 头图图片
    captions POST 头图文字
    ======== ==== ========

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

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
    """删除头图

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/backstage/course-management/delete-hero/

    **传入参数**

    =========== ==== ==================
    参数        方法 说明
    =========== ==== ==================
    delete_list POST 要删除的头图ID列表
    =========== ==== ==================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            deleted: [ // 已删除的头图ID列表
                1,
                ...
            ]
        }

    """

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
