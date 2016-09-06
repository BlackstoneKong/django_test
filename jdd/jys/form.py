# -*- coding: utf-8 -*-
from django import forms
class RegisterForm(forms.Form):
	username=forms.CharField(label='用户名',required=False)#不想用form表单自带的错误提示所以将required设置为False
	password=forms.CharField(label='密码',widget=forms.PasswordInput,required=False)
	password2=forms.CharField(label='确认密码',widget=forms.PasswordInput,required=False)
	def pwd_validate(self,p1,p2):
		return p1==p2
class LoginForm(forms.Form):
	username=forms.CharField(
		label=u"",
		required=False,
		widget=forms.TextInput(attrs={'placeholder':u"在此输入用户名",} ))
	password=forms.CharField(
		label=u"",
		required=False,
		error_messages={'required':u"请输入密码"},
		widget=forms.PasswordInput(attrs={'placeholder':u"在此输入密码",}))
	