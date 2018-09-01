"""课程模块前台操作"""

import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.constants import ERROR, INFO
from core.utils import get_page
from courses import utils
from courses.models import Hero, Course, Image, Comment, CourseUpVotes
from customers.models import LearningLog, OrderLog


def get_heroes(request):
    """获取头图

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/main/get-heroes/

    **传入参数**

    无

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            count: 2,                       // 头图总数
            content: [
                {
                    hero_id: 1,             // 头图ID
                    image: 'uploads/1.png', // 路径
                    caption: '...'          // 说明文字
                },
                ...
            ]
        }

    """

    heroes = Hero.objects.all()
    count = heroes.count()
    json_data = {
        'count': count,
        'content': []
    }
    for hero in heroes:
        json_data['content'].append(hero.as_dict())
    return JsonResponse(json_data)


def get_recent_courses(request):
    """获取最近课程

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/course/get-recent-courses/

    **传入参数**

    无

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            free_courses: [                     // 最近8个免费课程
                {
                    course_id: 1,               // 课程ID
                    thumbnail: 'uploads/1.png', // 缩略图
                    title: 'Data Structure',    // 课程名
                    description: '...'          // 简介
                },
                ...
            ],
            paid_courses: [                     // 最近8个付费课程
                {
                    course_id: 2,               // 课程ID
                    thumbnail: 'uploads/2.png', // 缩略图
                    title: 'Math',              // 课程名
                    description: '...'          // 简介
                },
                ...
            ]
        }

    """

    free_courses = utils.get_courses('free', 8)
    paid_courses = utils.get_courses('paid', 8)
    json_data = {
        'free_courses': [],
        'paid_courses': []
    }
    for free_course in free_courses:
        json_data['free_courses'].append(free_course.as_dict())
    for paid_course in paid_courses:
        json_data['paid_courses'].append(paid_course.as_dict())
    return JsonResponse(json_data)


def get_course_list(request):
    """获取课程列表

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/course/get-course-list/

    **传入参数**

    =========== ==== ================
    参数        方法 说明
    =========== ==== ================
    course_type GET  课程类型
    page        GET  当前页码
    page_limit  GET  每页最大显示数量
    =========== ==== ================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            count: 2,                           // 总条数
            page: 2,                            // 当前页码
            num_pages: 1,                       // 总页数
            content: [
                {
                    course_id: 1,               // 课程ID
                    thumbnail: 'uploads/1.png', // 缩略图
                    title: 'Data Structure',    // 课程名
                    description: '...'          // 简介
                },
                ...
            ]
        }

    """

    course_type = request.GET.get('course_type')

    courses = utils.get_courses(course_type).order_by('-updated_at')
    return get_page(request, courses)


def get_course_detail(request):
    """获取课程详情

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/course/get-course-detail/

    **传入参数**

    ========== ==== ========
    参数       方法 说明
    ========== ==== ========
    course_id  GET  课程ID
    referer_id GET  推荐人ID
    ========== ==== ========

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            course_id: 1,               // 课程ID
            thumbnail: 'uploads/1.png', // 缩略图
            title: 'Data Structure',    // 课程名
            description: '...',         // 简介
            price: '0.00',              // 价格
            reward_percent: '0.50',     // 奖励金比例
            up_votes: 1,                // 点赞数
            up_voted: false,            // 是否已点赞
            expire_duration: 0,         // 课程时效
            expire_time: null,          // 过期时间
            can_access: false           // 能否访问
        }

    """

    course_id = request.GET.get('course_id')
    request.session['referer_id'] = request.GET.get('referer_id', '')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    course_detail = {
        'course_id': course.id,
        'thumbnail': str(course.thumbnail),
        'title': course.title,
        'description': course.description,
        'price': course.price,
        'reward_percent': course.reward_percent,
        'up_votes': course.up_votes.count(),
        'up_voted': request.user in course.up_votes.all(),
        'expire_duration': course.expire_duration.total_seconds(),
        'expire_time': None,
        'can_access': False
    }
    if request.user.is_authenticated:
        try:
            learning_log = LearningLog.objects.get(
                course=course,
                customer=request.user
            )
            expire_time = learning_log.expire_time
            if expire_time is not None:
                course_detail['expire_time'] = expire_time
        except LearningLog.DoesNotExist:
            pass
        course_detail['can_access'] = utils.can_access(course, request.user)
    return JsonResponse(course_detail)


@login_required
def up_vote_course(request):
    """点赞课程

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/course/up-vote-course/

    **传入参数**

    ========== ==== ======
    参数       方法 说明
    ========== ==== ======
    course_id  GET  课程ID
    ========== ==== ======

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            up_voted: true, // 是否已点赞
            up_votes: 2     // 总点赞数
        }

    """

    course_id = request.GET.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    customer = request.user
    if customer in course.up_votes.all():
        up_voted = False
        CourseUpVotes.objects.get(course=course, customer=customer).delete()
    else:
        up_voted = True
        CourseUpVotes.objects.create(
            course=course,
            customer=customer
        )
    return JsonResponse(
        {
            'up_voted': up_voted,
            'up_votes': course.up_votes.count()
        }
    )


@login_required
def buy_course(request):
    """购买课程并完成分销

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/course/buy-course/

    **传入参数**

    ============== ==== ========
    参数           方法 说明
    ============== ==== ========
    course_id      POST 课程ID
    payment_method POST 支付方式
    ============== ==== ========

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP400：课程已购买

    .. code-block:: javascript

        {
            message: 'This course has already been purchased.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

    course_id = request.POST.get('course_id')
    payment_method = request.POST.get('payment_method')

    customer = request.user

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    try:
        OrderLog.objects.get(customer=customer, course=course, refunded_at=None)
        return JsonResponse(
            {'message': ERROR['course_already_purchased']},
            status=400
        )
    except OrderLog.DoesNotExist:
        pass

    price = course.price
    reward_coin = customer.reward_coin
    referer_id = request.session['referer_id']
    reward_percent = course.reward_percent

    if price > reward_coin:
        cash_spent = price - reward_coin
        reward_spent = reward_coin
        reward_coin = 0
    else:
        cash_spent = 0
        reward_spent = price
        reward_coin -= price

    customer.reward_coin = reward_coin
    customer.save()

    if referer_id != '' and int(referer_id) != int(customer.id):
        referer_id = int(referer_id)
        try:
            referer = get_user_model().objects.get(id=referer_id)
            reward_get = reward_percent * price
            referer.reward_coin += reward_get
            referer.save()
        except Course.DoesNotExist:
            pass

    OrderLog.objects.create(
        order_no=uuid.uuid1(),
        customer=customer,
        course=course,
        cash_spent=cash_spent,
        reward_spent=reward_spent,
        payment_method=int(payment_method)
    )

    return JsonResponse({'message': INFO['success']})


@login_required
def get_course_assets(request):
    """获取课程资源

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/get-course-assets/

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

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP200

    .. code-block:: javascript

        {
            course_id: 1,                        // 课程ID
            title: 'Data Structure',             // 课程名
            description: '...',                  // 简介
            audio: 'uploads/1.mp3',              // 课程音频资源
            images: [                            // 课程图片资源
                {
                    image_id: 1,                 // 图片ID
                    image_path: 'uploads/1.png', // 图片路径
                    load_time: 100               // 图片载入时间
                },
                ...
            ],
            progress: 86400                      // 学习进度
        }

    """

    course_id = request.GET.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    if not utils.can_access(course, request.user):
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    progress = utils.check_learning_log(course, request.user)
    images = Image.objects.filter(course=course).all().order_by('load_time')
    json_data = {
        'course_id': course.id,
        'title': course.title,
        'description': course.description,
        'audio': str(course.audio),
        'images': [],
        'progress': progress
    }
    for image in images:
        json_data['images'].append(image.as_dict())

    return JsonResponse(json_data)


@login_required
def save_learning_log(request):
    """保存学习进度

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/save-learning-log/

    **传入参数**

    ========= ==== ========
    参数      方法 说明
    ========= ==== ========
    course_id GET  课程ID
    progress  GET  学习进度
    ========= ==== ========

    **返回值**

    HTTP404：课程或学习记录未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

    course_id = request.GET.get('course_id')
    progress = request.GET.get('progress')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    if not utils.can_access(course, request.user):
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    try:
        learning_log = LearningLog.objects.get(
            course=course,
            customer=request.user
        )
    except LearningLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    learning_log.progress = progress
    learning_log.save()

    return JsonResponse({'message': INFO['success']})


@login_required
def get_course_comments(request):
    """获取课程下的留言

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/get-course-comments/

    **传入参数**

    ========== ==== ================
    参数       方法 说明
    ========== ==== ================
    course_id  GET  课程ID
    page       GET  当前页码
    page_limit GET  每页最大显示数量
    ========== ==== ================

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP200

    .. code-block:: javascript

        {
            count: 2,                                                      // 总条数
            page: 1,                                                       // 当前页码
            num_pages: 2,                                                  // 总页数
            content: [
                {
                    comment_id: 1,                                         // 评论ID
                    username: 'John',                                      // 用户名
                    user_id: 1,                                            // 用户ID
                    user_is_vip: false,                                    // 是否是认证用户
                    avatar: 'uploads/1.png',                               // 用户头像
                    course_id: 1,                                          // 课程ID
                    content: '...',                                        // 内容
                    up_votes: 1,                                           // 点赞数
                    down_votes: 0,                                         // 点踩数
                    up_voted: false,                                       // 是否点赞
                    down_voted: false,                                     // 是否点踩
                    created_at: '2018-08-31 16:46:44.794596+00:00',        // 创建时间
                    reply_count: 2,                                        // 回复总数
                    replies: [                                             // 回复列表
                        {
                            comment_id: 1,                                 // 回复ID
                            username: 'John',                              // 用户名
                            user_id: 1,                                    // 用户ID
                            user_is_vip: false,                            // 是否是认证用户
                            content: '...',                                // 内容
                            up_votes: 1,                                   // 点赞数
                            down_votes: 0,                                 // 点踩数
                            up_voted: false,                               // 是否点赞
                            down_voted: false,                             // 是否点踩
                            created_at: '2018-08-31 16:46:44.794596+00:00' // 创建时间
                        },
                        ...
                    ]
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

    if not utils.can_access(course, request.user):
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    if not course.can_comment:
        return JsonResponse(
            {'message': ERROR['comment_not_allowed']},
            status=403
        )

    comments = Comment.objects.filter(
        course=course,
        parent__isnull=True
    ).order_by('-created_at')
    return utils.get_comment_page(request, comments)


@login_required
def delete_comment(request):
    """删除留言

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/delete-comment/

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

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
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
    except Comment.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    if not request.user.id == comment.user.id:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    comment.delete()
    return JsonResponse({'message': INFO['object_deleted']})


@login_required
def up_vote_comment(request):
    """点赞留言

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/up-vote-comment/

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

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP200

    .. code-block:: javascript

        {
            up_voted: true, // 是否已点赞
            up_votes: 2     // 总点赞数
        }

    """

    comment_id = request.GET.get('comment_id')

    customer = request.user

    try:
        comment = Comment.objects.get(id=comment_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    if not utils.can_access(comment.course, customer):
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    if customer in comment.up_votes.all():
        up_voted = False
        comment.up_votes.remove(customer)
    else:
        up_voted = True
        comment.up_votes.add(customer)
    return JsonResponse(
        {
            'up_voted': up_voted,
            'up_votes': comment.up_votes.count()
        }
    )


@login_required
def down_vote_comment(request):
    """点踩留言

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/down-vote-comment/

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

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP200

    .. code-block:: javascript

        {
            down_voted: true, // 是否已点踩
            down_votes: 2     // 总点踩数
        }

    """

    comment_id = request.GET.get('comment_id')

    customer = request.user

    try:
        comment = Comment.objects.get(id=comment_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    if not utils.can_access(comment.course, customer):
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    if customer in comment.down_votes.all():
        down_voted = False
        comment.down_votes.remove(customer)
    else:
        down_voted = True
        comment.down_votes.add(customer)
    return JsonResponse(
        {
            'down_voted': down_voted,
            'down_votes': comment.down_votes.count()
        }
    )


@login_required
def add_comment(request):
    """添加评论

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/add-comment/

    **传入参数**

    =========== ==== ==========
    参数        方法 说明
    =========== ==== ==========
    course_id   POST 课程ID
    reply_to_id POST 回复对象ID
    content     POST 回复内容
    =========== ==== ==========

    **返回值**

    HTTP404：课程未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP403：课程禁止评论或被禁言

    .. code-block:: javascript

        {
            message: 'Commenting is not allowed.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.',
            comment_id: 2       // 回复ID
        }

    """

    course_id = request.POST.get('course_id')
    reply_to_id = request.POST.get('reply_to_id', '')
    comment_content = request.POST.get('content')

    user = request.user

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    if not utils.can_access(course, request.user):
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    if (not course.can_comment) or user.is_banned:
        return JsonResponse(
            {'message': ERROR['comment_not_allowed']},
            status=403
        )

    comment = Comment.objects.create(
        user=user,
        course=course,
        content=comment_content
    )

    if reply_to_id != '':
        try:
            reply_to = Comment.objects.get(id=int(reply_to_id))
            comment.parent = reply_to
            comment.save()
        except Comment.DoesNotExist:
            pass

    return JsonResponse(
        {
            'message': INFO['success'],
            'comment_id': comment.id
        }
    )


@login_required
def get_replies(request):
    """获取回复

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/courses/forestage/play/get-replies/

    **传入参数**

    ========== ==== ================
    参数       方法 说明
    ========== ==== ================
    comment_id GET  评论ID
    page       GET  当前页码
    page_limit GET  每页最大显示数量
    ========== ==== ================

    **返回值**

    HTTP404：评论未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP403：没有权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP403：课程禁止评论

    .. code-block:: javascript

        {
            message: 'Commenting is not allowed.'
        }

    HTTP200

    .. code-block:: javascript

        {
            count: 2,                                              // 总条数
            page: 1,                                               // 当前页码
            num_pages: 2,                                          // 总页数
            content: [
                {
                    comment_id: 1,                                 // 回复ID
                    username: 'John',                              // 用户名
                    user_id: 1,                                    // 用户ID
                    user_is_vip: false,                            // 是否是认证用户
                    content: '...',                                // 内容
                    up_votes: 1,                                   // 点赞数
                    down_votes: 0,                                 // 点踩数
                    up_voted: false,                               // 是否点赞
                    down_voted: false,                             // 是否点踩
                    created_at: '2018-08-31 16:46:44.794596+00:00' // 创建时间
                },
                ...
            ]
        }

    """

    comment_id = request.GET.get('comment_id')

    try:
        comment = Comment.objects.get(id=comment_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    if not utils.can_access(comment.course, request.user):
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    if not comment.course.can_comment:
        return JsonResponse(
            {'message': ERROR['comment_not_allowed']},
            status=403
        )

    replies = Comment.objects.filter(parent=comment).order_by('-created_at')
    return utils.get_reply_page(request, replies)
