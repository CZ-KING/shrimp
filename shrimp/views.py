from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .error import ErrorCode,MESSAGE
from .import utils as UTILS
from  utils import es
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
import time
from django.core.cache import cache
import pypinyin
from pypinyin import pinyin
from django.db.models import Q

from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from utils.dal import database
from utils.config import settings
# Create your views here.


class Home(LoginRequiredMixin,View):
    login_url = "login/"

    def get(self,request):
        user_id = request.session.get('uid')
        user = models.User.objects.get(pk=user_id)
        user.username = user.username if user.username else "小虾"
        answers =  models.Answer.objects.order_by("-weight")[:5]



        for answer in answers:
           answer.comments = models.Comment.objects.filter(answer_id=answer.id).order_by('-ct')[:5]


        return render(request,'index.html',{'user':user,'answers':answers})




class Register(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self, request):
        username = request.POST.get('username')
        secret_key = request.POST.get('secret_key')
        register_type = int(request.POST.get('register_type',-1))
        nickname = request.POST.get('nickname','')
        print(request.POST)
        response = {"code":ErrorCode.sucess,"message":MESSAGE[ErrorCode.sucess]}

        # 判断输入的账号，密码，以及注册类型是否合法

        if not username or not nickname or not secret_key or not register_type in {0,1} or \
        (register_type==0 and not UTILS.phone_valid(username)) or \
        (register_type==1 and not UTILS.email_valid(username)):

            response['code'] = ErrorCode.invalid_arguments
            response['message'] = MESSAGE[ErrorCode.invalid_arguments]
        # 手机验证码方式进行注册
        else:
            if register_type==0:
                try:
                    models.User.objects.get(phone=username)
                    response['code'] = ErrorCode.user_exists
                    response['message'] = MESSAGE[ErrorCode.user_exists]
                except:
                    try:
                        phone_number = int(username)
                        sms =  models.VerificationCode.objects.get(phone=phone_number)
                        current_time = int(time.time())
                        if secret_key != sms.code or current_time>(sms.ct+600):
                            response['code'] = ErrorCode.invalid_arguments
                            response['message'] = MESSAGE[ErrorCode.invalid_arguments]
                        else:
                            user =  models.User(phone=phone_number)
                            user.save()
                    except:
                        # 这里是不是要用数据库错误，因为手机号是合法的，只是还没有及时写入数据库？？？？？
                        response['code'] = ErrorCode.request_invalid
                        response['message'] = MESSAGE[ErrorCode.request_invalid]


            # 由于一开始已经有判断secret_key的取值范围，所以这里不用elif，直接else就行
            # 邮箱方式进行注册
            else:
                try:
                    # 判断是否有这个用户，有的话返回已存在

                    models.User.objects.get(email=username)
                    response['code'] = ErrorCode.user_exists
                    response['message'] = MESSAGE[ErrorCode.user_exists]
                except:
                    # 用户为新用户，此时将密码进行加密后存入数据库
                    pinyins = pinyin(nickname,style=pypinyin.Style.NORMAL)
                    url_token = ""

                    for _ in pinyins:

                        url_token += "".join(_)
                    try:
                        token = models.UrlToken.objects.get(url_token=url_token)
                        amount = token.amount+1
                        token.amount = amount
                        token.save()
                        url_token = url_token + str(amount)
                    except:
                        models.UrlToken.objects.create(url_token=url_token)

                    user = models.User.objects.create_user(username,secret_key,url_token=url_token,username=nickname)
                    user.save()

        return JsonResponse(response)





class Login(View):

    def get(self,request):
        return  render(request,'login.html')

    def post(self,request):
        username = request.POST.get("username","")
        secret_key = request.POST.get('secret_key',"")
        veri_type = int(request.POST.get('veri_type',-1))
        response = {"code": ErrorCode.sucess, "message": MESSAGE[ErrorCode.sucess]}
        # 判断输入的账号，密码，以及注册类型是否合法
        print(username,secret_key,veri_type)
        if not username or not secret_key or not veri_type in {0, 1} or \
        (veri_type == 0 and not UTILS.phone_valid(username)) or \
        (veri_type == 1 and not UTILS.email_valid(username)):

            response['code'] = ErrorCode.invalid_arguments
            response['message'] = MESSAGE[ErrorCode.invalid_arguments]

        else:

            if veri_type == 0:
                try:
                    models.User.objects.get(phone=username)
                    user_code = models.VerificationCode.objects.get(phone=username)
                    current_time = time.time()
                    if user_code.code != secret_key or current_time > (user_code.ct+600):
                        response['code'] = ErrorCode.captcha_invalid
                        response['message'] = MESSAGE[ErrorCode.captcha_invalid]
                except:
                    response['code'] = ErrorCode.user_not_exists
                    response['message'] = MESSAGE[ErrorCode.user_not_exists]

            # 邮箱登录方式
            else:
                # 查询是否有该用户，然后比对加密后的密码
                user = authenticate(username=username, password=secret_key)

                # 判断user是否有效，如果无效则表示认证失败
                if not user:
                    response['code'] = ErrorCode.user_not_exists
                    response['message'] = MESSAGE[ErrorCode.user_not_exists]

                else:
                    request.session["uid"] = user.id
                    request.session['usename'] = user.username
                    # 调用login方法来为认证通过的用户创建会话
                    login(request, user)


        return JsonResponse(response)


class Sms(View):
    def post(self,request):
        phone_number = request.POST.get('phone_number')
        response = {"code":ErrorCode.sucess,"message":MESSAGE[ErrorCode.sucess]}

        # 判断输入的账号是否为正常手机号，如不是则返回参数无效
        if not phone_number or not UTILS.phone_valid(phone_number):

             response['code'] = ErrorCode.invalid_arguments
             response['message'] = MESSAGE[ErrorCode.sucess]
             return JsonResponse(response)
        else:
            phone_number = int(phone_number)
            sms_code = UTILS.get_sms_captcha()
            current_time = int(time.time())
            try:
                # 查找该手机是否接收过验证码
                sms = models.VerificationCode.objects.get(phone=phone_number)
                # 当前时间超过60秒后可以再次请求发送验证码，覆盖原验证码
                if current_time > sms.ct + 60:
                    sms.code = sms_code
                    sms.ct = current_time
                    sms.save()
                    response["data"] = {"captcha":sms_code}
                # 当前时间小于60秒，则返回请求无效
                else:
                    response['code'] = ErrorCode.invalid_arguments
                    response['message'] = MESSAGE[ErrorCode.invalid_arguments]
            # 如未收到过验证码则将该手机用户建立记录
            except:
                sms = models.VerificationCode(phone = phone_number,code = sms_code,ct=current_time)
                sms.save()
                response['data'] = {"captcha":sms_code}

        return JsonResponse(response)



class Question(LoginRequiredMixin,View):
    login_url = "login/"

    def post(self,request):
        userid = request.session.get('uid')
        username = request.POST.get('username','')
        title = request.POST.get('title','')
        description = request.POST.get('description','')
        classfication = request.POST.get('classfication','')
        response = {"code": ErrorCode.sucess, "message": MESSAGE[ErrorCode.sucess]}


        if  not username or not title or not classfication:
            response = {"code": ErrorCode.invalid_arguments, "message": MESSAGE[ErrorCode.invalid_arguments]}

        else:
            question_=models.Question.objects.create(userid=userid,username=username,title=title,description=description,classification=classfication)
            response['data'] = {"question_id":question_.id}
        return JsonResponse(response)



class QuestionPage(View):
    def get(self,request,question_id):
        try:
            question_obj = models.Question.objects.get(id=question_id)
            userid = request.session.get('uid',None)
            answers = models.Answer.objects.filter(question_id=question_id)
            try:
                user = models.User.objects.get(pk=userid)
            except:
                user = None

        except:
            response = {"code": ErrorCode.database_error, "message": MESSAGE[ErrorCode.database_error]}
            return JsonResponse(response)

        return render(request,"question.html",{"question_obj":question_obj, "user": user, "answers":answers})



class Answer(View):


    def post(self,request):
        userid = request.session.get('uid',None)
        username = request.POST.get('username','')
        avatar_url= request.POST.get('avatar_url','')
        slogan = request.POST.get('slogan','')
        url_token = request.POST.get('url_token','')
        question_id = request.POST.get('question_id','')
        question_title = request.POST.get('question_title','')
        content = request.POST.get('content','')

        response = {"code": ErrorCode.sucess, "message": MESSAGE[ErrorCode.sucess]}
        print(request.POST)
        if not username or not question_id or not content:
            response["code"]= ErrorCode.invalid_arguments
            response["message"] = MESSAGE[ErrorCode.invalid_arguments]

        else:
            answer_obj = models.Answer.objects.create(userid=userid,username=username,question_id=question_id,
                                               question_title=question_title,content=content,
                                                slogan=slogan, status=0)

            response["data"] = {'question_id':question_id,'answer_id':answer_obj.id}
        return JsonResponse(response)

class AnswerPage(View):
    def get(self,request,question_id,answer_id):
        try:

            answer_obj = models.Answer.objects.filter(Q(id__exact=answer_id) & Q(question_id__exact=question_id))

            userid = request.session.get('uid',None)



        except:

            return render(request,"404.html")

        return render(request,"question.html",{"answers":answer_obj})



class Profile(View):
    # login_url = "login/"

    def get(self,request,url_token):

        try:
            user = models.User.objects.get(url_token=url_token)
            return render(request, "profile.html", {"user": user})

        except:

            return render(request,"404.html")


class Comment(View):
    def get(self,request):
        answer_id = request.GET.get('answer_id','')
        page = request.GET.get('page')

        if not answer_id :
            return render(request, "404.html")

        comments_obj = models.Comment.objects.filter(answer_id=answer_id)
        paginator = Paginator(comments_obj, 10)

        try:
            comments = paginator.page(page)

        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            comments = paginator.page(1)

        except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
            return render(request, "404.html")

        except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            comments_page = paginator.page(paginator.num_pages)

        return render(request,'comments.html',{'comments':comments})




    def post(self,request):
        user_id = request.session.get('uid')
        answer_id = request.POST.get('answer_id')
        comment = request.POST.get("comment","")
        comment_id = request.POST.get("comment_id")
        other_userid = request.POST.get("other_userid")
        username = request.POST.get("username","")
        other_username = request.POST.get("other_username","")
        url_token = request.POST.get("url_token","")
        other_url_token = request.POST.get("other_url_token","")
        response = {"code": ErrorCode.sucess, "message": MESSAGE[ErrorCode.sucess]}
        print(request.POST)

        if  answer_id and comment and url_token and username :


            if comment_id and other_url_token and other_username:
                comment_obj = models.Comment.objects.create(answer_id=answer_id,comment=comment,comment_id=comment_id,user_id=user_id
                                                     ,other_userid=other_userid,url_token=url_token,
                                                     other_url_token=other_url_token,username=username,
                                                     other_username=other_username)

            else:
                comment_obj = models.Comment.objects.create(answer_id=answer_id, comment=comment,username = username,
                                                            user_id=user_id, url_token=url_token)
            weight = UTILS.calc_weight(comments=1)
            try:
                answer_obj = models.Answer.objects.get(id=answer_id)
                answer_obj.weight += weight
                answer_obj.save()
            except:
                response['code'] = ErrorCode.invalid_arguments
                response['message'] = MESSAGE[ErrorCode.invalid_arguments]


            response['data'] = {'comment_id': comment_obj.id}

        else:
            response['code'] = ErrorCode.invalid_arguments
            response['message'] = MESSAGE[ErrorCode.invalid_arguments]

        return JsonResponse(response)


class Search(View):
    es_instance = database.Database.get_instance(settings.DatabaseType.ELASTICSEARCH)

    def get(self,request):

        query = request.GET.get("query", "")

        query = {"query": {
            "multi_match": {"query": query,
                      "fields":["title","description"]
                      }
            }
        }
        print(query)
        hits = self.es_instance.query(query, es_index="shrimp")
        print('hits查询结果：',hits)
        questions = []

        for data in hits["hits"]["hits"]:
            question_obj = {}
            question_obj['title'] = data["_source"]["title"]
            question_obj['description'] = data["_source"]["description"]
            questions.append(question_obj)
        return render(request, "search.html", {"questions": questions})


# Comment视图中的get和post可以在同一视图吗？get就是获得该问题下所有的评论，post就是新添加一个评论；
# 是不是Comment这个接口就是点击“发表评论”后的请求，应该只有post这个请求
# 然后再新建立一个CommentPage视图，就是点击"评论"按钮后的请求，然后显示该问题下的所有评论
# 再向老师问一下前后端交互的过程，以及前端参数在哪里获得，能获得哪些参数，如何判断这个参数前端是否能够获得
# 向数据库里写入数据，需要判断一下是否写入成功吗？等成功再返回成功状态给前端，比如是否可能因为网络等原因导致没有写入


# json可以返回对象吗
# 首页那里怎么获得问题的回答的id号
# 分页的时候href连接那里怎么获得回答的id





































