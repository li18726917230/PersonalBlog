from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    phone = models.CharField(max_length=128)
    email = models.EmailField()
    nickname = models.TextField()
    imagepath = models.CharField(max_length=128)
    createtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 添加唯一约束
        constraints = [
            models.UniqueConstraint(fields=['name'], name='user')
        ]

    def __str__(self):
        return self.name


class User_other(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    the_name = models.CharField(max_length=128)
    age = models.CharField(max_length=4)
    sex = models.CharField(max_length=4)
    id_card = models.CharField(max_length=128, null=True)
    home_add = models.CharField(max_length=128, null=True)
    marital_status=models.CharField(max_length=128)
    worku_nits=models.CharField(max_length=128,null=True)
    monthly_income=models.CharField(max_length=128,null=True)
    motto=models.TextField()