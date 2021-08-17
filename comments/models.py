from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from user.models import User
# Create your models here.
class Comments(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name="user_comment",on_delete=models.CASCADE) #评论用户

    topcomment = models.ForeignKey('self',null=True,related_name="top_comment",on_delete=models.CASCADE) #顶级评论

    replycomment = models.ForeignKey('self', null=True,related_name="reply_comment", on_delete=models.CASCADE)  # self指向自己 被回复的内容
    replyuser = models.ForeignKey(User, null=True,related_name="reply_user", on_delete=models.CASCADE) # 被回复的用户

    def __str__(self):
        return self.text

    class Meta:
        ordering=['-comment_time']