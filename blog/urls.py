from django.urls import path
from . import  views

urlpatterns = [
    path('upload_image/',views.upload_image,name='upload_image'),
    path('blogwrite/', views.blogwrite, name='blogwrite'),
    path('bloglist/',views.bloglist,name='bloglist'),
    path('blogdetailed/<int:blog_id>',views.blogdetailed,name='blogdetailed'),
]