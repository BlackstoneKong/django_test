# -*- coding: utf-8 -*-
#视图文件，实际相当于MVC结构中的控制器。通过定义各种函数干以下这些事儿：
#页面的渲染，URL定位至某个Views然后，进行相应的逻辑操作，最终渲染成相关页面。
from django.shortcuts import get_object_or_404,render,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth,messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.template.context import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.context_processors import csrf
from .models import Choice_Question,Question,Duoxuan,Panduan,Tiankong,Jianda
from .models import lunshu
from .forms import UserForm,UserProfileForm
from .form  import RegisterForm,LoginForm
import random
#from bootstrap_toolkir.widgets import BootstrapUneditableInput
#验证视图（登录和注册用到）
def login_validate(request,username,password):
	rtvalue=False
	user=authenticate(username=username,password=password)
	if user is not None:
		if user.is_active:
			login(request,user)
			return True
	return rtvalue
#登录
def mylogin(request):
	error=[]
	if request.method=='POST':
		form=LoginForm(data=request.POST)
		if form.is_valid():
			data=form.cleaned_data
			username=data['username']
			password=data['password']
			if username or password:
				if username:
					if password:
						if login_validate(request,username,password):
							#HttpResponseRedirect('/jys/')到底是用哪个才能实现跳转,用render不会实现URL的跳转
							#template = loader.get_template('jys/index.html')
							#context = RequestContext(request, {
							#	'username': username, })
							#request.getSession.setAttribute("username","username")
							return render(request,'jys/data_query.html',{'username':username})
							#return render(request,'jys/index.html',RequestContext(request,{'username':username}))
							#return render_to_response('jys/welcome.html',{'user':username})
						else:
							error.append('账户或密码不正确,请重试')
					else:
						error.append('请输入密码')
				else:
					error.append('请输入用户名')
			else:
				error.append('请输入用户名和密码')
	else:
		form=LoginForm()
	return render(request,'jys/login.html',{'error':error,'form':form})
#注册
def myregister(request):
	error=[]
	if request.method=="POST":#是不是POST方式提交表单
		form=RegisterForm(data=request.POST)#如果是则将POST的数据交给函数RegisterForm进行合法性验证
		if form.is_valid():#如果验证合格，则把有效数据提取出来
			data=form.cleaned_data
			username=data['username']
			password=data['password']
			password2=data['password2']
			if username or password or password2:
				if username:
					if password:
						if password2:
							if not User.objects.all().filter(username=username):#如果原数据库中没有新注册的username
								if form.pwd_validate(password,password2):#如果两次输入데密码相同
									user=User.objects.create_user(username,"a@outlook.com",password)#创建新用户
									user.save()
									login_validate(request,username,password)
									return HttpResponseRedirect(reverse('jys:login_index',args=(username,)))
								else:
									error.append('两次填入密码不一致，请重新输入')
							else:
								error.append('用户名已存在')
						else:
							error.append('请填写确认密码')
					else:
						error.append('请填写密码')
				else:
					error.append('请填写用户名')
			else:
				error.append('请填写用户名和密码')
	else:
		form=RegisterForm()
	return render(request,'jys/register.html',{'error':error,'form':form})
#修改密码
def changepassword(request,username):
	error=[]
	if request.method=='POST':
		form=ChangepwdForm(request.POST)
		if form.is_valid():
			data=form.cleaned_data
			user=authenticate(username=username,password=data['old_pwd'])
			if user is not None:
				if data['new_pwd']==data['new_pwd2']:
					newuser=User.objects.get(username_exact=username)
					newuser.set_password(data['new_pwd'])
					newuser.save()
					return HttpResponseRedirect('/jys/login/')
				else:
					error.append('Please input the same password')
			else:
				error.append('Please correct the old password')
		else:
			error.append('Please input the required domain')
	else:
		form=ChangepwdForm()
	return render_to_response('jys/changepassword.html',{'form':form,'error':error})
#测试装饰器
@login_required
def restricted(request):
	
    return HttpResponse("Since you're logged in, you can see this text!")
#登出
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/jys/login/')
#初始页
@login_required
def index(request,username):
	#加入验证  1、如果在地址栏输入的用户名已经是登录过的，则直接跳转至首页
	#          2、否则跳转至登录界面
	#存在问题:如果在URL中输入一个存在的username，也会出现跳转
	#usernamee=request.getSession.getAttribute("username")
	#print usernamee
	newuser=User.objects.filter(username=username)
	if newuser:
		return render(request, 'jys/index.html',{'username':username})
	else:
		logout(request)
   		 # Take the user back to the homepage.
    	return HttpResponseRedirect('/jys/login/')
#数据管理
@login_required
def data_manage(request):

    return render(request, 'jys/data_manage.html')

#试卷生成
@login_required
def paper_create(request):
    #通过表单传递的数值n，随机生成n个范围内的随机数列表，然后通过for循环，传递随机数给pk
	cq=Choice_Question.objects.all()
	return render(request, 'jys/paper_create.html', {'cq':cq})
#试卷生成完毕
@login_required
def paper_created(request):
	a=0
	b=0
	cc=['','','','','','']
	d=['一','二','三','四','五','六','七','八','九','十']
	e=['单选题','多选题','判断题','填空题','简答题','论述题']
	dxno=[]
	dxc=[]
	dx=request.GET['dx']
	#	
	if int(dx)!=0:
		cc[0]=(d[a]+'、'+e[0])
		a=a+1
	else:
		cc[0]=""

	for i in range(1,int(dx)+1):
		c=random.randint(0,len(Question.objects.all()))
		while c in dxno:
			c=random.randint(0,len(Question.objects.all()))
		dxno.append(random.randint(0,len(Question.objects.all())))
		dxc.append(Question.objects.all()[c])

	pd=request.GET['pd']
	tk=request.GET['tk']
	jd=request.GET['jd']
	ls=request.GET['ls']

	
	duoxno=[]
	duoxc=[]
	duox=request.GET['duox']
	if int(duox)!=0:
		cc[1]=(d[a]+'、'+e[1])
		a=a+1
	else:
		cc[1]=""
	
	for i in range(1,int(duox)+1):
		c=random.randint(0,len(Duoxuan.objects.all())-1)
		while c in duoxno:
			c=random.randint(0,len(Duoxuan.objects.all())-1)
		duoxno.append(c)
		duoxc.append(Duoxuan.objects.all()[c])	

	pdno=[]
	pdc=[]
	pd=request.GET['pd']
	if int(pd)!=0:
		cc[2]=(d[a]+'、'+e[2])
		a=a+1
	else:
		cc[2]=""
	
	for i in range(1,int(pd)+1):
		c=random.randint(0,len(Panduan.objects.all())-1)
		while c in pdno:
			c=random.randint(0,len(Panduan.objects.all())-1)
		pdno.append(c)
		pdc.append(Panduan.objects.all()[c])	

	tkno=[]
	tkc=[]
	tk=request.GET['tk']
	if int(tk)!=0:
		cc[3]=(d[a]+'、'+e[3])
		a=a+1
	else:
		cc[3]=""
	
	for i in range(1,int(tk)+1):
		c=random.randint(0,len(Tiankong.objects.all())-1)
		while c in tkno:
			c=random.randint(0,len(Tiankong.objects.all())-1)
		tkno.append(c)
		tkc.append(Tiankong.objects.all()[c])	

	jdno=[]
	jdc=[]
	jd=request.GET['jd']
	if int(jd)!=0:
		cc[4]=(d[a]+'、'+e[4])
		a=a+1
	else:
		cc[4]=""
	
	for i in range(1,int(jd)+1):
		c=random.randint(0,len(Jianda.objects.all())-1)
		while c in jdno:
			c=random.randint(0,len(Jianda.objects.all())-1)
		jdno.append(c)
		jdc.append(Jianda.objects.all()[c])	

	lsno=[]
	lsc=[]
	ls=request.GET['ls']
	if int(ls)!=0:
		cc[5]=(d[a]+'、'+e[5])
		a=a+1
	else:
		cc[5]=""
	
	for i in range(1,int(ls)+1):
		c=random.randint(0,len(lunshu.objects.all())-1)
		while c in lsno:
			c=random.randint(0,len(lunshu.objects.all())-1)
		lsno.append(c)
		lsc.append(lunshu.objects.all()[c])	

	return render(request,'jys/paper_created.html',{'dxc':dxc,'duoxc':duoxc,'pdc':pdc,'tkc':tkc,'jdc':jdc,'lsc':lsc,'dxtitle':cc[0],'duoxtitle':cc[1],'pdtitle':cc[2],'tktitle':cc[3],'jdtitle':cc[4],'lstitle':cc[5]})

#数据查询
@login_required
def data_query(request):
    return render_to_response('jys/data_query.html')
@login_required
def search(request):
    errors = []
    page_nums=[]
    onepage_flag=1;
    np=1;
    #传递了关键字、分类、页码和序号；
    #添加对关键字q的预处理：去空格、特殊符号、多个关键字等
    if 'q' in request.GET:
        q = request.GET['q']#从表单中获取关键字
        q_init_value=q;#保留原始输入以便将其返回驻留在input框中
        q=q.replace(' ','')#很粗暴的解决办法：直接将空格去掉
        np=request.GET['np']#从表单中获取当前页码以便进行页码切换
        ps=int(request.GET['ps'])#前一页及后一页的处理
        cho=request.GET['cho']
        if q:
        	if int(cho)==0:
	        	subject_search = Question.objects.filter(subject__icontains=q)
	        if int(cho)==1:
        		subject_search = Duoxuan.objects.filter(subject__icontains=q)
        	if int(cho)==2:
        		subject_search = Panduan.objects.filter(subject__icontains=q)
        	if int(cho)==3:
        		subject_search = Tiankong.objects.filter(subject__icontains=q)
        	if int(cho)==4:
        		subject_search = Jianda.objects.filter(subject__icontains=q)
        	if int(cho)==5:
        		subject_search = lunshu.objects.filter(subject__icontains=q)
        	if len(subject_search)%5==0:
        		page_count=len(subject_search)/5+1
	        #处理页码开始
	        if len(subject_search)%5==0:
        		page_count=len(subject_search)/5+1
        	else:
	        	page_count=len(subject_search)/5+2
	        for i in range(1,page_count):
	        	page_nums.append(i)

	        if int(np)%5==0:
	        	forepage=int(np)-5
	        	afterpage=int(np)
	        else:
	        	forepage=int(np)-(int(np)%5)
	        	afterpage=int(np)+(5-(int(np)%5))

	        if len(page_nums)<2 or int(np)==(page_count-1):
	        	onepage_flag=0

	        lownp=int(np)*5-5
	        upnp=int(np)*5
	        thenp=lownp+ps-1;
	        #处理页码结束

        return render_to_response('jys/data_query_result.html',{'subject':len(subject_search),'subject_search': subject_search[thenp:thenp+1], 'query': q_init_value,'page_nums':page_nums[forepage:afterpage],'onepage_flag':onepage_flag,'thenp':thenp+1})
    return render_to_response('jys/data_query.html',{'errors': errors})

@login_required
def search2(request):
    errors = []
    page_nums=[]
    onepage_flag=1
    lastpage_flag=1
    ca=[]
    cb=[]
    cc=[]
    cd=[]
    np=1;
    #添加对关键字q的预处理：去空格、特殊符号、多个关键字等
    if 'q' in request.GET:
        q = request.GET['q']
        q_init_value=q;
        q=q.replace(' ','')
        np=request.GET['np']
        cho=request.GET['cho']

        if not q:
        	return render_to_response('jys/data_query.html',{'errors': errors})
        else:
        	if int(cho)==0:
        		subject_search = Question.objects.filter(subject__icontains=q)
        	if int(cho)==1:
        		subject_search = Duoxuan.objects.filter(subject__icontains=q)
        	if int(cho)==2:
        		subject_search = Panduan.objects.filter(subject__icontains=q)
        	if int(cho)==3:
        		subject_search = Tiankong.objects.filter(subject__icontains=q)
        	if int(cho)==4:
        		subject_search = Jianda.objects.filter(subject__icontains=q)
        	if int(cho)==5:
        		subject_search = lunshu.objects.filter(subject__icontains=q)
        	if len(subject_search)%5==0:
        		page_count=len(subject_search)/5+1
        	else:
	        	page_count=len(subject_search)/5+2
	        #1、当没有任何搜索结果时
	        #2、当结果不足十条只在一页内显示时
	        #3、当结果显示超过不足5页时
	        #4、当结果超过五页时
	        #5、当结果超过
	        
	        for i in range(1,page_count):
	        	page_nums.append(i)

	        if int(np)%5==0:
	        	forepage=int(np)-5
	        	afterpage=int(np)
	        else:
	        	forepage=int(np)-(int(np)%5)
	        	afterpage=int(np)+(5-(int(np)%5))

	        if len(page_nums)<2 or int(np)==(page_count-1):
	        	onepage_flag=0
	        lownp=int(np)*5-5
	        upnp=int(np)*5

        return render_to_response('jys/data_query_result2.html',{'subject':len(subject_search),'subject_search': subject_search[lownp:upnp], 'query': q_init_value,'page_nums':page_nums[forepage:afterpage],'onepage_flag':onepage_flag})
    return render_to_response('jys/data_query.html',{'errors': errors})

#在线考试
@login_required
def online_exam(request):
	#f = open('lunshu.txt')
	#for line in f:
	#	question_id,subject,answer,difficulty,category_id = line.split('*')
	#	print(question_id)
	#	print(subject)
	#	print(answer)
	#	print(difficulty)
	#	print(category_id)
	#	lunshu.objects.create(question_id=question_id,category_id=category_id,subject=subject,difficulty=difficulty,answer=answer)
	#f.close()
	return render(request, 'jys/online_exam.html')
def current_url_view_good(request):
    return HttpResponse("Welcome to the page at %s" % request.META)

def temp(request):
	return render(request,'jys/temp.html')
@login_required
def usercenter(request):
	return render(request, 'jys/usercenter.html')



