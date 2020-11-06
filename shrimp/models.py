from django.db import models
import time
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.




class VerificationCode(models.Model):
    phone = models.BigIntegerField(unique=True, verbose_name="手机号")
    code = models.CharField(max_length=6,blank=False, verbose_name="验证码")
    ct = models.IntegerField(default=int(time.time()), verbose_name="创建时间")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("请填入邮箱！")
        if not password:
            raise ValueError("请填入密码!")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    phone = models.BigIntegerField(unique=True,null=True,verbose_name="手机号")
    username =  models.CharField(max_length=32,null=True,db_index=True,verbose_name="昵称")
    email = models.CharField(max_length=30, unique=True, null=True, verbose_name="邮箱")
    USERNAME_FIELD = 'email'
    slogan = models.CharField(max_length=50, blank=True, verbose_name="个性签名")
    sex = models.IntegerField(default=0, verbose_name="性别")
    brief_introduction = models.CharField(max_length=250, blank=True, verbose_name="slogan")
    url_token = models.CharField(max_length=30, blank=False, unique=True, verbose_name="用户标识")
    last_login = models.DateTimeField(auto_now=True,verbose_name="上次登录时间")
    ct = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # USERNAME_FIELD对应的'telephone'字段和密码字段默认是必须的字段
    # 下[]可以添加其它必须的字段, 比如['username', 'email']
    REQUIRED_FIELDS = []

    # 重新定义Manager对象，在创建user的时候使用telephone和
    # password，而不是使用username和password
    objects = UserManager()



class Question(models.Model):
    username = models.CharField(max_length=20, default="匿名", db_index=True, verbose_name="昵称")
    title = models.CharField(max_length=100, blank=False, db_index=True, verbose_name="标题")
    description = models.CharField(max_length=500, blank=True, db_index=True, verbose_name="问题描述")
    classification = models.CharField(max_length=200, blank=False, db_index=True, verbose_name="问题分类")
    userid = models.BigIntegerField(null=False,db_index= True,verbose_name='用户id')
    modify_time = models.DateTimeField(auto_now=True,verbose_name="问题修改时间")
    ct = models.DateTimeField(auto_now_add=True,verbose_name="提问时间")



class Answer(models.Model):
    userid = models.IntegerField(null=False,verbose_name="回答者ID")
    username = models.CharField(max_length=20, default="匿名", db_index=True, verbose_name="昵称")
    question_id = models.BigIntegerField(null=False,verbose_name='问题编号')
    question_title =  models.CharField(max_length=200,null=False,verbose_name="回答的问题标题")
    content = models.CharField(max_length=4096,null=False,verbose_name='回答内容')
    picture = models.CharField(max_length=200,null=False,verbose_name="回答者头像")
    slogan = models.CharField(max_length=25,null=True,verbose_name="回答者简介")
    status = models.SmallIntegerField(null=False,verbose_name="审核状态")
    weight = models.IntegerField(default=1,verbose_name="权重")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="回答修改时间")
    ct = models.DateTimeField(auto_now_add=True, verbose_name="回答时间")



class UrlToken(models.Model):
    url_token = models.CharField(max_length=100,unique=True)
    amount = models.IntegerField(default=0)


class Comment(models.Model):
    answer_id = models.BigIntegerField(null=False,db_index=True, verbose_name='回答编号')
    user_id = models.IntegerField(null=False, verbose_name="评论者ID")
    comment = models.CharField(max_length=500, null=False, verbose_name='评论/回复内容')
    comment_id = models.IntegerField(null=True, verbose_name="评论ID")
    username = models.CharField(max_length=30,null=False, verbose_name="评论者昵称")
    other_userid = models.IntegerField(null=True,verbose_name="回复者ID")
    other_username = models.CharField(max_length=30, null=True, verbose_name="回复者昵称")
    url_token = models.CharField(max_length=30,null=True, verbose_name="评论者url_token")
    other_url_token = models.CharField(max_length=30,null=True, verbose_name="回复者url_token")
    ct = models.DateTimeField(auto_now_add=True,verbose_name="评论/回复时间")





















