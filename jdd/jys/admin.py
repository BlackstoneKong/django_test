# -*- coding: utf-8 -*-   
import sys  

from django.contrib import admin
from .models import Choice_Question
from .models import UserProfile
from .models import Question,Duoxuan
#admin.site.register(UserProfile)
#admin.site.register(Choice_Question)
admin.site.register(Question)
admin.site.register(Choice_Question)
admin.site.register(Duoxuan)
reload(sys)  
sys.setdefaultencoding('utf8')  