from MySQLdb._exceptions import IntegrityError
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from polls import test
from polls.models import UserInfo, GoodsInfo, StoreInfo, SearchHistory
from yiguoman import settings


def index(request):
    latest_question_list = [{'id': '1', 'question_text': '9102'},{'id': '2', 'question_text': '9102'},{'id': '23', 'question_text': '9102'}]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

#解析地址中间数字，显示
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

# 网页显示字典内容
def list_output_data(request):
    template = loader.get_template('polls/list_output_data.html')
    context = {
        'test': "www.baidu.com",
    }
    return HttpResponse(template.render(context, request))

def outputdata(request):
    print(request.get_port())
    goodinfo = GoodsInfo.objects.all()
    searchHistory = SearchHistory.objects.all()
    storeInfo = StoreInfo.objects.all()[0:3]#不包含3这个行，从0开始算
    userInfo = UserInfo.objects.all()
    return render(request, "polls/outputdata.html", context={"goodinfos": goodinfo,"searchHistorys": searchHistory,"storeInfos": storeInfo,"userInfos": userInfo})

def uploadpic(request):
    return render(request,'polls/uploadpic.html')
#　发来表单　实现上传功能

def upload(request):
    print("in upload")
    # 从请求当中　获取文件对象
    f1 = request.FILES.get('picture')
    #　利用模型类　将图片要存放的路径存到数据库中
    # p = Pictures()
    # p.pic = "polls/" + f1.name
    # p.save()
    # 在之前配好的静态文件目录static/media/booktest 下 新建一个空文件
    # 然后我们循环把上传的图片写入到新建文件当中
    fname = settings.MEDIA_ROOT + "/polls/" + f1.name
    with open(fname,'wb') as pic:
        for c in f1.chunks():
            pic.write(c)
    result=test.image_classification(fname)
    print("sssss"+request.GET.get("fruit"))
    # return template(request)

#　显示图片
def show_pic(request):
    # pic_obj = Pictures.objects.get(id=1)
     return render(request, 'polls/show_pic.html', {'pic_obj':"1"})

#　模板测试
def template(request):
    Hami_melon_infos = StoreInfo.objects.filter(goods_sort="哈密​​瓜",source_site__in = ["Taobao","Jingdong"] )[:8]
    cherry_infos = StoreInfo.objects.filter(goods_sort="樱桃",source_site__in = ["Taobao","Jingdong"])[:8]
    store_infos_ranking_lists= StoreInfo.objects.order_by("-sale_rating")[:5]
    store_infos_new_goods = StoreInfo.objects.order_by("-key1")[:3]
    store_infos_top_rated_goods = StoreInfo.objects.order_by("sale_rating")[:5]
    image= '//g-search2.alicdn.com/img/bao/uploaded/i4/i2/3354851036/O1CN0169MvmQ1JWWpizTKGl_!!0-item_pic.jpg_250x250.jpg_.webp'
    url='//item.taobao.com/item.htm?id=587180017670&ns=1&abbucket=2#detail'
    context = {

        'Hami_melon_infos': Hami_melon_infos,
        'cherry_infos': cherry_infos,
        'store_infos_ranking_lists': store_infos_ranking_lists,
        'store_infos_new_goods':   store_infos_new_goods,
        'store_infos_top_rated_goods': store_infos_top_rated_goods,

    }

    return render(request, 'polls/template.html', context)

# 搜索结果页面
def search_result(request):
    print(request.method)
    if request.method=='POST':
        fruit = request.GET.get("fruit", "水蜜桃")
        shop1=request.POST.get("shop1","Taobao")
        shop2 = request.POST.get("shop2", "Pingduoduo")
        shop3 = request.POST.get("shop3", "Jingdong")
        select_opt = request.POST.get("select_opt", "推荐")
        price_range = request.POST.get("price_range", "$20 - $400")
        print("post  "+shop1+shop2+shop3+select_opt+price_range)

    if request.method=='GET':
        fruit=request.GET.get("fruit","水蜜桃")
        shop1=request.GET.get("shop1","Taobao")
        shop2 = request.GET.get("shop2", "Pingduoduo")
        shop3 = request.GET.get("shop3", "Jingdong")
        select_opt = request.GET.get("select_opt", "trend")
        price_range = request.GET.get("price_range", "$10 - $100")
        print("get  " + shop1 + shop2 + shop3 + select_opt + price_range)

    f1 = request.FILES.get('picture')
    if f1:
        fname = settings.MEDIA_ROOT + "/polls/" + f1.name
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        result = test.image_classification(fname)
        print("图片识别结果"+result)
        fruit = result
    #数据库数据筛选
    store_infos = StoreInfo.objects.all()
    store_infos = store_infos.filter(goods_sort=fruit)
    store_infos = store_infos.filter(source_site__in = [shop1,shop2,shop3])
    price_range2=price_range
    price_range1 = price_range2.split(" - ")
    down_price = int(price_range1[0].split("$")[1])
    up_price = int(price_range1[1].split("$")[1])
    store_infos = store_infos.filter(price__range =(down_price,up_price))
    if select_opt=='trend':
        print('trend')
    elif select_opt=='sales':
        store_infos = store_infos.filter().order_by('sale_rating')
    elif select_opt == 'price':
        print("price")
        store_infos = store_infos.filter().order_by('price')

    paginator = Paginator(store_infos, 10)
    store_infos = paginator.page(1)
    context = {
                   'store_infos': store_infos,
                    'shop1': shop1,'shop2': shop2,'shop3': shop3,
                    'select_opt': select_opt,
                    'price_range': price_range,
                    'fruit': fruit,
                    'maxs': up_price,
                    'mins': down_price

                }
    return render(request, "polls/search_result.html", context)

#　登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("name:" + username, "mima:" + password)
        re = auth.authenticate(username=username, password=password)  # 用户认证
        if re is not None:  # 如果数据库里有记录（即与数据库里的数据相匹配或者对应或者符合）
            auth.login(request, re)  # 登陆成功||使用它以后网址就不用再次登录，自动识别，直接使用关键字user就可以详情见book.html
            print("登陆成功:")
            return template(request)
        else:  # 数据库里不存在与之对应的数据
            print("数据库里不存在与之对应的数据")
            return render(request, 'login.html', {'error': '用户名或密码错误'})  # 注册失败

    return render(request, 'polls/login.html')

#　注册
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 添加到数据库
        try:
            registAdd = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            print("Error: 重复")
            registAdd="重复"
            #弹出错误的时候registadd本身是没有创建的
        else:
            print( "成功")
            print(registAdd.id)#返回的就是一个user的类，后面直接更列名。
            if username:
                print(username)

        if registAdd=="重复":
            return render(request, 'register.html', {'registAdd': registAdd, 'username': username,'error': '用户名重复或非法字符'})

        else:
            # return HttpResponse('ok')
            #看会不会出现bug
            re = auth.authenticate(username=username, password=password)
            auth.login(request, re)
            return template(request)

    return render(request, 'polls/register.html')

#注销
def logout(request):
    auth.logout(request)
    return template(request)
