from django.urls import path

from . import views

urlpatterns = [

    #基本测试页面，没啥用
    path('index/', views.index, name='index'),

    #读取地址中间的值
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # ex:传入list读取数据
    path('a1/list_output_data/', views.list_output_data, name='list_output_data'),

    # 读取数据库显示在网页上
    path('a1/outputdata/', views.outputdata, name='add'),

    # 图片上传的整个
    # 过程三个页面
    path('uploadpic/', views.uploadpic, name='uploadpic'),
    #下面这个用于上传图片的，不能直接访问，因为缺少表单信息
    path('upload/', views.upload, name='uploadpic'),
    #name不能取show,注意这些保留字，用了会提示找不到该name。
    path('uploadpic/show/', views.show_pic, name='show123'),

    #template使用测试
    path('template/', views.template, name='index'),

    #search_detail
    path('search_result/', views.search_result, name='index'),
    #login
    path('login/', views.login, name='index'),
    #register
    path('register/', views.register, name='index'),
    #logout
    path('logout/', views.logout, name='index'),
]