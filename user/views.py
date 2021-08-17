from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from .models import User, User_other
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password  # 数据加密解密
from django.views.decorators.csrf import csrf_exempt
from PersonalBlog.utils import Image_save
import random
import string
from django.core.cache import cache
# Create your views here.
# 手机验证码发送
import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


def send_sms_single(phone_num, template_id, template_param_list):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    appid = 1400553628  # 自己应用ID
    appkey = "3269ca4a677a5baa1657cf42b952b950"  # 自己应用Key
    sms_sign = "致未来的一封信"  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response


# 登录
def login(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        if username != None:
            # 用户名登录
            password = request.POST.get('password')
            if request.session.get('user_name') != username:
                try:
                    user = User.objects.get(name=username)
                    check = check_password(password, user.password)
                    if check:
                        request.session['is_login'] = True
                        request.session['user_name'] = user.name
                        # request.COOKIES=
                        return redirect(request.GET.get('from', reverse('bloglist')))
                    else:
                        data['message'] = '用户名或密码不正确'
                except ObjectDoesNotExist:
                    data['message'] = '用户名或密码不正确'
            else:
                data['message'] = '当前用户已经登录了'
        else:
            # 手机号登录
            tel = request.POST.get('tel')
            code = request.POST.get('code')
            if code == cache.get(tel):
                user = User.objects.get(phone=tel)
                request.session['is_login'] = True
                request.session['user_name'] = user.name
                return redirect(request.GET.get('from', reverse('bloglist')))
            else:
                data['message'] = '验证码不正确'
    return render(request, 'login.html', data)


# 注册
def register(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        headportrait = request.FILES.get('headportrait')
        image_save = Image_save(headportrait, 'user')
        if image_save == 'failure':
            data['message'] = "请上传以['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']结尾的图片格式"
            return render(request, 'register.html', data)
        imagepath = "/media/images/user/" + image_save + "/" + str(headportrait)
        try:
            user = User.objects.create(name=username, password=make_password(password1), phone=tel, email=email,
                                       nickname=nickname, imagepath=imagepath)
            user.save()
            data['from'] = request.GET.get('from')
            return render(request, 'jump.html', data)
        except Exception as e:
            print(e)
    return render(request, 'register.html', data)


# 退出登录
def logout(request):
    del request.session['user_name']  # 删除指定的， 删除的是保存在服务器上的session的值
    # request.session.flush() 删除所有的session
    return redirect(reverse('home'))


# 生成验证码
@csrf_exempt
def code_send(request):
    tel = request.POST.get('tel')
    username = request.session.get('user_name')
    try:
        user = User.objects.get(name=username)
        if user.phone == tel:
            # 修改信息，不修改手机号
            # 随机生成6位验证码
            code = ''.join(random.sample(string.digits, 6))
        else:
            # 修改手机号，判断手机号是否已经使用
            exists = User.objects.filter(phone=tel).exists()
            if exists:
                return JsonResponse({'result': 2})
            code = ''.join(random.sample(string.digits, 6))
    except User.DoesNotExist:
        # 注册用户，判断手机号是否已经使用
        exists = User.objects.filter(phone=tel).exists()
        if exists:
            return JsonResponse({'result': 2})
        code = ''.join(random.sample(string.digits, 6))
    # 验证码发送频繁，请一分钟之后在次尝试
    if cache.has_key(tel):
        return JsonResponse({'result': 1})
    # 发送验证码
    # single = send_sms_single(tel, 1058548, [code])
    # set存储 get获取 has_key 判断是否有缓存
    cache.set(tel + code, code, 120)  # 1.键 2.值 3.有效时间
    cache.set(tel, tel, 120)  # 1.键 2.值 3.有效时间
    return JsonResponse({'result': 0})


# 短信验证
@csrf_exempt
def code_val(request):
    data = {}
    code = request.POST.get('code')
    tel = request.POST.get('tel')
    tel_code = cache.get(tel + code)
    if tel_code == code:
        data['result'] = 0
    else:
        data['result'] = 1
    return JsonResponse(data)


# 判断用户名是否存在
@csrf_exempt
def user_val(request):
    data = {}
    username = request.POST.get('username')
    exists = User.objects.filter(name=username).exists()
    if exists:
        data['result'] = 0
    else:
        data['result'] = 1
    return JsonResponse(data)


# 登录手机号验证
@csrf_exempt
def login_phone_val(request):
    data = {'result': 1}  # 手机号未注册
    tel = request.POST.get('tel')
    phone = User.objects.filter(phone=tel).exists()
    if phone:
        code = ''.join(random.sample(string.digits, 6))
        print(code)
        # 发送验证码
        # single = send_sms_single(tel, 1058548, [code])
        cache.set(tel, code, 120)
        data['result'] = 0
    return JsonResponse(data)


# 信息修改
@csrf_exempt
def user_alter(request):
    data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        tel = request.POST.get('tel')
        if cache.get(tel) != tel:
            return render(request, 'user_alter.html', {'message': '手机号错误，修改失败'})
        headportrait = request.FILES.get('headportrait')
        user = User.objects.get(name=username)
        user.nickname = nickname
        user.phone = tel
        # 判断图片是否为空，如果为空不修改
        if headportrait != None:
            image_save = Image_save(headportrait, 'user')
            if image_save == 'failure':
                data['message'] = "请上传以['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']结尾的图片格式"
            imagepath = "/media/images/user/" + image_save + "/" + str(headportrait)
            user.imagepath = imagepath
        user.save()
        data['message'] = '修改成功'
    username = request.session.get('user_name')
    user = User.objects.get(name=username)
    data['user'] = user
    return render(request, 'user_alter.html', data)


# 修改密码
@csrf_exempt
def pwd_alter(request):
    data = {}
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            username = request.session.get('user_name')
            user = User.objects.get(name=username)
            user.password = make_password(password1)
            user.save()
            data['message'] = '修改成功'
        else:
            # 遵从前端不可信原则
            data['message'] = '密码不一致请重新输入'
    return render(request, 'pwd_alter.html', data)


# 信息补充
def user_adder(request):
    username = request.session.get('user_name')
    user = User.objects.get(name=username)
    if request.method == 'POST':
        the_name = request.POST.get('the_name')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        id_card = request.POST.get('id_card', '')
        home_add = request.POST.get('home_add', '')
        marital_status = request.POST.get('marital_status')
        worku_nits = request.POST.get('worku_nits', '')
        monthly_income = request.POST.get('monthly_income', '')
        motto = request.POST.get('motto')
        user_other, create = User_other.objects.get_or_create(user=user)
        user_other.the_name = the_name
        user_other.age = age
        user_other.sex = sex
        user_other.id_card = id_card
        user_other.home_add = home_add
        user_other.marital_status = marital_status
        user_other.worku_nits = worku_nits
        user_other.monthly_income = monthly_income
        user_other.motto = motto
        user_other.save()
        return render(request, 'user_adder.html', {'user_other': user_other, 'message': '修改成功'})
    try:
        user_other = user.user_other_set.get()
    except User_other.DoesNotExist:
        return render(request, 'user_adder.html')
    return render(request, 'user_adder.html', {'user_other': user_other})
