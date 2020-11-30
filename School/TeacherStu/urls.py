from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from . import views

urlpatterns = [

    # path('allTechUserData/', views.Techlist.as_view(),name='Get/Post-Stu/Tech-data'),
    path('data/', views.stulist.as_view()), 
    path('forgetPass/', views.forgetPass, name='Forget_Password'), 
    path('videoFile/', views.FileView.as_view(),name='Get/Post-File'),
    path('getuserData/', views.getUserData, name='POST-Get-UserData-with-userid'),
    path('stuUpload/', views.addShipmentAPIView, name='AddShipmentAPIView'), 
    path('userData/', views.userData, name='userData'),
    path('checkNum/', views.checkMobileNum, name='checkMobileNum'),
    path('newsData/', views.NewsView.as_view(),name='Get/Post-File'), 
    path('newsUpload/', views.addNews, name='addNews'), 
    path('stuListSchool/', views.stuListSchool, name='Student_Data_BasedOn_School_code'),
    url(r'^videoPostUpload/', views.VideoPostUploadView.as_view(), name='VideoPost_Upload'),
    url(r'^commentData/(?P<slug>[\w-]+)/$', views.CommentView.as_view(), name='VideoPostDetail_with_UsersComments'),
    url(r'^commentData/', views.CommentView.as_view(), name='VideoPostDetail_with_UsersComments'),
    url(r'^videoPostDetails/(?P<slug>[\w-]+)/$', views.videoPostDetails, name='VideoPostDetail_with_UsersComments'),
    url(r'^videoPostDetailsData/', views.videoPostDetailsData.as_view(), name='VideoPostDetailData'),
    url(r'^queData/', views.QuestionView.as_view(),name='Upload-FAQ-Que-Ans'), 
    url(r'^ansData/(?P<id>\d+)/$', views.AnswerView.as_view(), name='FAQ_Ques-&-Ans'), 
    path('stuTaskData/', views.stuTaskList.as_view(),name="Student's Task"), 
    path('notesData/', views.notesList.as_view(), name=""),
    path('feedBackData/', views.feedBackList.as_view()), 
    url(r'^MCQViewData/', views.MCQ_PostTopicView.as_view(), name='MCQTopic_Data_WithGET_Data_classAndSchool'), 
    url(r'^MCQ_QueData/', views.MCQ_QueView, name='MCQ_QuestionData_AnswerData_AccToTitle_SchoolandClass'),
    url(r'^MCQansData/', views.MCQ_AnswerData.as_view(), name='MCQAnswerData'), 
    url(r'^MCQcheckansData/', views.MCQ_FansView, name='MCQ_CheckAnswerData'), 
    url(r'^MCQResData/', views.MCQ_ResultData.as_view(), name="MCQ_ResultData_and_GettingListof_Quizz_those_StudentDon't_attendQuiz"), 
    url(r'^MCQ_stuResultData/', views.MCQ_stuResult, name='MCQ_Student_Result_Data'), 
    url(r'^MCQ_stuResultDetails/', views.MCQ_stuResultDetails, name='MCQ_Student_Result_Details'),
    url(r'^videoFData/', views.VideoFormData.as_view(),name='Upload-FAQ-Que-Ans'), 
    url(r'^noteiceFList/', views.NoteiceFireFileData.as_view(),name='NoticeImageData'), 
    # path('videoFile/<int:id>/', views.FileView.as_view()),
    # url(r'^upload/, FileView.as_view(), name='file-upload'),

]


