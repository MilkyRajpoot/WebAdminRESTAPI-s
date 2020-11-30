from django.contrib import admin
from simple_history import register
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

register(User, app=__package__)
@admin.register(Student, Video, User, News, Video_Post, NoticeImage, Comment, videoF, FAQ_Answer, Stu_Task,NoteiceFire, Teach_Task, Feedback, MCQ_Post, MCQ_Question, MCQ_Answer, MCQ_Result)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ('userid', 'name','category', 'mobileNum')
    odering = ['name']
    # list_display = ( 
    # 			'regNum',
    # 			'name',
    # 			'mobileNum',
    #         	)
    