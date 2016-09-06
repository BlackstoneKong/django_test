# -*- coding: utf-8 -*-
#models.py包含两个模型，一个是单选题模型，一个是用户信息模型。
#后期还要添加更多的模型。
#针对数据库的一些操作指令：
#同步数据库命令：
#python manage.py makemigrations以及python manage.py migrate
#python manage.py flush 清楚数据库中的所有数据。
#python manage.py createsuperuser创建超级管理员
#导入导出数据命令：
#python manage.py dumpdata appname > appname.json
#python manage.py loaddata appname.json

#数据库的命令行操作：
#调出命令行:python manage.py shell
#三种新增数据库的方式：(假设数据库名为Blog,两个列名为title和content)
#1、Blog.objects.create(title="",content="")
#2、blog=Blog() blog.title="" blog.content="" blog.save()
#3、blog=Blog(title="",content="") blog.save() 

#避免重复导入的方法：Blog.objects.get_or_create(title=title,content=content)
#一次导入多个数据的方法：Blog.objects.create()

#简单的数据导入的导出：
#python manage.py dumpdata [appname]>appname_data.json
#python manage.py loaddata appnmae_data.json
#导出用户数据：python manage.py dumpdata auth>auth.json

#数据库的整体迁移比如由sqlite3导出至PostgreSQL、MySQL
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jdd.settings")

#Choice_Question是单选题模块，生成单选题数据库
class Choice_Question(models.Model):
    question_content=models.TextField(blank = True, null = True)#题干
    choice_content=models.CharField(max_length=500)#备选项
    correct_choice=models.CharField(max_length=4)#正确答案
    #会在数据库命令行的操作中返回以下函数的内容
    def __str__(self):
        return self.question_content

#用户模块，与Django自带用户模型是一一对应的关系。
class UserProfile(models.Model):
	user=models.OneToOneField(User)
    #以下两行考虑删除，注册时不需要添加用户网页信息和图片信息。
	website=models.URLField(blank=True)
	picture=models.ImageField(upload_to='profile_images',blank=True)
	def __str__(self):
		return self.user.username
#定义数据库
#试题库
class Question(models.Model):
    question_id=models.CharField(u'题目编号',max_length=20,blank=True)#题目编号、主键
    category_id=models.CharField(u'题目类型',max_length=10,blank=True)#单择、多选、填空、问答
    subject=models.CharField(u'题目内容',max_length=500,blank=True)#题干
    choice_a=models.CharField(u'选项A',max_length=100,blank=True)#选项，填空问答亦可作为一个选项
    choice_b=models.CharField(u'选项B',max_length=100,blank=True)
    choice_c=models.CharField(u'选项C',max_length=100,blank=True)
    choice_d=models.CharField(u'选项D',max_length=100,blank=True)
    difficulty=models.CharField(u'难度',max_length=10,blank=True)
    answer=models.CharField(u'答案',max_length=500,blank=True)
    be_supported=models.CharField(u'点赞',max_length=10,blank=True)#被点赞
    be_collected=models.CharField(u'收藏',max_length=10,blank=True)#被收藏
    be_selected=models.CharField(u'采纳',max_length=10,blank=True)#被采纳
    be_reposted=models.CharField(u'转发',max_length=10,blank=True)#被转发
class Duoxuan(models.Model):
    question_id=models.CharField(u'题目编号',max_length=20,blank=True)#题目编号、主键
    category_id=models.CharField(u'题目类型',max_length=10,blank=True)#单择、多选、填空、问答
    subject=models.CharField(u'题目内容',max_length=500,blank=True)#题干
    choice_a=models.CharField(u'选项A',max_length=100,blank=True)#选项，填空问答亦可作为一个选项
    choice_b=models.CharField(u'选项B',max_length=100,blank=True)
    choice_c=models.CharField(u'选项C',max_length=100,blank=True)
    choice_d=models.CharField(u'选项D',max_length=100,blank=True)
    choice_e=models.CharField(u'选项E',max_length=100,blank=True)
    choice_f=models.CharField(u'选项F',max_length=100,blank=True)
    difficulty=models.CharField(u'难度',max_length=10,blank=True)
    answer=models.CharField(u'答案',max_length=500,blank=True)
    be_supported=models.CharField(u'点赞',max_length=10,blank=True)#被点赞
    be_collected=models.CharField(u'收藏',max_length=10,blank=True)#被收藏
    be_selected=models.CharField(u'采纳',max_length=10,blank=True)#被采纳
    be_reposted=models.CharField(u'转发',max_length=10,blank=True)#被转发
class Panduan(models.Model):
    question_id=models.CharField(u'题目编号',max_length=20,blank=True)#题目编号、主键
    category_id=models.CharField(u'题目类型',max_length=10,blank=True)#单择、多选、填空、问答
    subject=models.CharField(u'题目内容',max_length=500,blank=True)#题干
    difficulty=models.CharField(u'难度',max_length=10,blank=True)
    answer=models.CharField(u'答案',max_length=500,blank=True)
    be_supported=models.CharField(u'点赞',max_length=10,blank=True)#被点赞
    be_collected=models.CharField(u'收藏',max_length=10,blank=True)#被收藏
    be_selected=models.CharField(u'采纳',max_length=10,blank=True)#被采纳
    be_reposted=models.CharField(u'转发',max_length=10,blank=True)#被转发
class Tiankong(models.Model):
    question_id=models.CharField(u'题目编号',max_length=20,blank=True)#题目编号、主键
    category_id=models.CharField(u'题目类型',max_length=10,blank=True)#单择、多选、填空、问答
    subject=models.CharField(u'题目内容',max_length=500,blank=True)#题干
    difficulty=models.CharField(u'难度',max_length=10,blank=True)
    answer=models.CharField(u'答案',max_length=500,blank=True)
    be_supported=models.CharField(u'点赞',max_length=10,blank=True)#被点赞
    be_collected=models.CharField(u'收藏',max_length=10,blank=True)#被收藏
    be_selected=models.CharField(u'采纳',max_length=10,blank=True)#被采纳
    be_reposted=models.CharField(u'转发',max_length=10,blank=True)#被转发
class Jianda(models.Model):
    question_id=models.CharField(u'题目编号',max_length=20,blank=True)#题目编号、主键
    category_id=models.CharField(u'题目类型',max_length=10,blank=True)#单择、多选、填空、问答
    subject=models.CharField(u'题目内容',max_length=500,blank=True)#题干
    difficulty=models.CharField(u'难度',max_length=10,blank=True)
    answer=models.CharField(u'答案',max_length=500,blank=True)
    be_supported=models.CharField(u'点赞',max_length=10,blank=True)#被点赞
    be_collected=models.CharField(u'收藏',max_length=10,blank=True)#被收藏
    be_selected=models.CharField(u'采纳',max_length=10,blank=True)#被采纳
    be_reposted=models.CharField(u'转发',max_length=10,blank=True)#被转发
class lunshu(models.Model):
    question_id=models.CharField(u'题目编号',max_length=20,blank=True)#题目编号、主键
    category_id=models.CharField(u'题目类型',max_length=10,blank=True)#单择、多选、填空、问答
    subject=models.CharField(u'题目内容',max_length=500,blank=True)#题干
    difficulty=models.CharField(u'难度',max_length=10,blank=True)
    answer=models.CharField(u'答案',max_length=500,blank=True)
    be_supported=models.CharField(u'点赞',max_length=10,blank=True)#被点赞
    be_collected=models.CharField(u'收藏',max_length=10,blank=True)#被收藏
    be_selected=models.CharField(u'采纳',max_length=10,blank=True)#被采纳
    be_reposted=models.CharField(u'转发',max_length=10,blank=True)#被转发
class Paper(models.Model):
    paper_id=models.IntegerField()
    paper_name=models.CharField(max_length=40)
class PaperDuplicate(models.Model):
    paper_id=models.IntegerField()
    paper_name=models.CharField(max_length=40)
    





