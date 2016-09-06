__author__ = 'sm'
from django.conf.urls import url
from django.contrib import admin
from . import views
app_name='jys'
urlpatterns = [
url(r'^admin/', admin.site.urls),
url(r'^username=(?P<username>\w+)/$',views.index,name='login_index'),
url(r'^logout/$', views.user_logout, name='logout'),
url(r'^restricted/', views.restricted, name='restricted'),
url(r'^login/$',views.mylogin,name='login'),
url(r'^register/$',views.myregister,name='register'),
url(r'^changepassword/$',views.changepassword,name='changepassword'),

url(r'^data_manage/$', views.data_manage, name='data_manage'),
url(r'^paper_create/$', views.paper_create, name='paper_create'),
url(r'^data_query/$', views.data_query, name='data_query'),
url(r'^search/$', views.search,name='data_search'),
url(r'^online_exam/$', views.online_exam, name='online_exam'),
url(r'^paper_created/',views.paper_created,name='paper_created'),
url(r'^data_query/search/$', views.search2,name='data_search2'),
url(r'^usercenter/$', views.usercenter,name='usercenter'),
url(r'^a/$', views.current_url_view_good),

url(r'^temp/$',views.temp,name='temp'),
]