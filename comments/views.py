from django.shortcuts import render
from .models import Comments
from django.http import JsonResponse
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType


# Create your views here.
@csrf_exempt
def comments(request):
    username = request.session.get('user_name')
    text = request.POST.get('text')
    blog_id = request.POST.get('blog_id')
    data = {}
    try:
        user = User.objects.get(name=username)
        content_type = ContentType.objects.get(model='blog')
        create = Comments.objects.create(content_type=content_type, object_id=blog_id, text=text, user=user)
        create.save()
        data['msg'] = 'SUCCESS'
        comment = Comments.objects.filter(object_id=blog_id).first()
        data['user'] = comment.user.nickname
        data['user_id'] = comment.user.id
        data['text'] = comment.text
        data['comment_id'] = comment.id
        data['comment'] =0
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(e)
        data['msg'] = 'ERROR'
    return JsonResponse(data)


@csrf_exempt
def reply(request):
    username = request.session.get('user_name')
    username = User.objects.get(name=username)
    text = request.POST.get('text')
    blog_id = request.POST.get('blog_id')
    comment_id = request.POST.get('comment_id')
    topcomment = Comments.objects.get(id=comment_id)
    reply_id = int(request.POST.get('reply_id'))
    if reply_id != 0:
        replycomment = Comments.objects.get(id=reply_id)
    else:
        replycomment = topcomment
    replyuser = request.POST.get('replyuser')
    replyuser = User.objects.get(id=replyuser)
    content_type = ContentType.objects.get(model='blog')
    data = {}
    try:
        create = Comments.objects.create(content_type=content_type, object_id=blog_id, text=text, user=username,
                                         topcomment=topcomment,
                                         replycomment=replycomment, replyuser=replyuser)
        create.save()
        data['msg'] = 'SUCCESS'
    except Exception as e:
        data['msg'] = 'ERROR'
    comment = Comments.objects.filter(object_id=blog_id).first()
    data['user'] = comment.user.nickname
    data['replyuser'] = comment.replyuser.nickname
    data['text'] = comment.text
    data['topcomment'] = comment_id
    data['replyuser_id'] = comment.replyuser.id
    data['comment_reoly_id'] = comment.id
    data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
    return JsonResponse(data)
