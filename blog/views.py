from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from .models import Blog, BlogType
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator  # 智能分页
from PersonalBlog.settings import PAGING_DATA
from reading.models import Read
from django.contrib.contenttypes.models import ContentType
from PersonalBlog.utils import Image_save


# Create your views here.
# 图片上传后端处理
@csrf_exempt
def upload_image(request):
    file = request.FILES.get('fileName')
    image_save = Image_save(file, 'blog')
    if image_save == 'failure':
        return JsonResponse({"errno": 1})
    return JsonResponse({"errno": 0, "data": [{"url": "/media/images/blog/" + image_save + "/" + str(file)}]})


def blogwrite(request):
    data = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        blogtype = request.POST.get('blogtype')
        content = request.POST.get('content')
        username = request.POST.get('username')
        if title == '' or blogtype == '' or content == '':
            data['message'] = '请填写必填字段'
        else:
            blog_type = get_object_or_404(BlogType, type_name=blogtype)
            user = get_object_or_404(User, name=username)
            blog_create = Blog.objects.create(title=title, blog_type=blog_type, content=content, author=user)
            blog_create.save()
            data['message'] = '提交成功'
    return render(request, 'blog_write.html', data)


def bloglist(request):
    data = {}
    search = request.GET.get('search')
    if search is not None and search!='':
        blog = Blog.objects.filter(title__contains=search)
        data['blogs'] = blog
        return render(request, 'blog_list.html', data)
    page = request.GET.get('page', 1)  # 获取当前页面，如果没有默认为1
    classify = request.GET.get('classify','')
    try:
        blog = Blog.objects.filter(blog_type_id=classify)
    except:
        blog=Blog.objects.all()
    paginator = Paginator(blog, PAGING_DATA)  # 第一个参数分页数据，第二个参数 以几条数据进行分页
    page_obj = paginator.get_page(page)  # 分页
    page_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2,
                                                 on_ends=1)  # 智能分页 第一个参数number为当前页码数, on_each_side为当前页码左右两边的页数，on_ends为首尾页码范围
    data['blogs'] = page_obj.object_list  # 每一页数据
    data['page_range'] = page_range
    data['page_obj'] = page_obj
    data['page'] = 'True'
    response = render(request, 'blog_list.html', data)
    # 设置当前页的cookie
    response.set_cookie('page', page_obj.number)
    return response


def blogdetailed(request, blog_id):
    blog_data = Blog.objects.get(id=blog_id)
    content_type = ContentType.objects.get_for_model(blog_data)
    key = "%s_%s_read" % (content_type.model, blog_data.id)
    if not request.COOKIES.get(key):
        read, create = Read.objects.get_or_create(content_type=content_type, object_id=blog_data.id)
        read.read_num += 1
        read.save()
    previous_blog = Blog.objects.filter(id__gt=blog_id).last()  # 上一篇博客
    next_blog = Blog.objects.filter(id__lt=blog_id).first()  # 下一篇博客
    response = render(request, 'blog_detailed.html',
                      {'blog_data': blog_data, 'previous_blog': previous_blog, 'next_blog': next_blog})
    response.set_cookie(key, 'true')  # 阅读标记
    return response
