from django.shortcuts import render
from .models import LikeRecord, LikeCount
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from user.models import User


# Create your views here.
def like(request):
    if request.session.get('user_name') is None:
        return JsonResponse({'status': 'ERROR'})
    user = User.objects.get(name=request.session.get('user_name'))
    content_type = request.GET.get('content_type')
    try:
        content_type = ContentType.objects.get(model=content_type)
    except ObjectDoesNotExist:
        return JsonResponse('失败', safe=False)
    object_id = request.GET.get('object_id')
    is_like = request.GET.get('is_like')
    if is_like == 'true':
        # 点赞操作
        like_record, create = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                               user=user)
        like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
        like_count.liked_num += 1
        like_count.save()
        return JsonResponse({'status': 'SUCCESS', 'liked_num': like_count.liked_num})
    else:
        like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
        like_record.delete()
        # 点赞数量减一
        like_count = LikeCount.objects.get(object_id=object_id, content_type=content_type)
        like_count.liked_num -= 1
        like_count.save()
        return JsonResponse({'status': 'SUCCESS', 'liked_num': like_count.liked_num})
