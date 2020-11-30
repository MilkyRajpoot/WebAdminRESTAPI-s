from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView

urlpatterns = [
# Dashboard Page Panel
    url(r'^home/$', views.home, name='home'),
    url(r'^Taskhome/$', views.TaskHome, name='TaskHome'),  
    # url(r'^feedback/$', views.feedback, name='feedback'),
# Home Function
    path('home/create/', views.create_view,name='createUser'),  
    url(r'^home/stuTeachList$', views.stuTeachList, name='UsersList'),
    # url(r'^home/TechTeachList$', views.TechTeachList, name='TeachersList'),
    url(r'^home/usersList/$', views.usersList, name='AuthUsersList'),
    url(r'^home/stulist(?P<userid>[\w-]+)/$', views.detail_view,name='stulistUser'), 
    url(r'^home/usersList/stulistAuth(?P<id>\d+)/$', views.detail_view_user,name='stulistAuthUser'), 
    url(r'^home/stulist(?P<userid>[\w-]+)/edit/$', views.update_view, name='updateUser'), 
    url(r'^home/usersList/stulistAuth(?P<id>\d+)/edit/$', views.update_view_user, name='updateAuthUser'),
    url(r'^home/stulist(?P<userid>[\w-]+)/delete/$', views.delete_view, name='deleteUser'), 
    url(r'^home/usersList/stulistAuth(?P<id>\d+)/delete/$', views.delete_view_user, name='deleteAuthUser'),
    # url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    # url(r'^empanellist(?P<id>\d+)/edit/$', views.update_view, name='update'),
# Auth and User Login/Logout
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="userlogout.html"), name='logout'),
    path('userlogin/', views.Userdata,name='userlogin'),
    path('userlogout/', views.userlogout,name='userlogout'),
    path('signin/', views.loginpage, name='loginpage'),
    url(r'^MCQ_Reslogout/$', auth_views.LogoutView.as_view(template_name="resLogout.html"), name='Resultlogout'),
# Student's Task URL's  techtasklist
    # path('home/allTask', views.stuTaskList,name='allTaskList'), 
    # path('home/addTask', views.create_Taskview,name='createTask'),  
    # url(r'^home/tasklist(?P<id>\d+)/edit/$', views.update_Taskview, name='updateTask'), 
    # url(r'^home/tasklist(?P<id>\d+)/delete/$', views.delete_Taskview, name='deleteTask'), 
    # url(r'^home/clasSearch/(?P<clas>[\w\-]+)/search/$', views.clasSearch, name='clasSearch'),

    path('home/authallTask', views.authStuTaskList,name='authallTaskList'),
    path('Taskhome/allTechTask', views.stuTaskList2,name='allTaskList2'),
    path('Taskhome/techaddTask', views.create_Taskview2,name='techcreateTask'),
    url(r'^home/techtasklist(?P<id>\d+)/edit/$', views.update_Taskview2, name='techupdateTask'), 
    url(r'^home/techtasklist(?P<id>\d+)/delete/$', views.delete_Taskview2, name='techdeleteTask'), 
    url(r'^home/techclasSearch/(?P<clas>[\w\-]+)/search/$', views.clasSearch2, name='techclasSearch'),  
# News's Details URL's
    path('home/allNewsData', views.NewsDataList,name='allNewsDataList'),
    path('home/addNewsData', views.create_NewsData,name='create_NewsData'),   
    url(r'^home/newsData(?P<id>\d+)/edit/$', views.update_NewsData, name='update_NewsData'), 
    url(r'^home/newsData(?P<id>\d+)/delete/$', views.delete_NewsData, name='delete_NewsData'), 
    # url(r'^home/dateSearch/search/$', views.dateSearch, name='dateSearch'), 
# Teacher's Details URL's
    path('home/addTeachTask', views.create_Teachview,name='createTeachview'), 
    path('home/allTeachTask', views.teachTaskList,name='allTeachTaskList'), 
    url(r'^home/techtasklist(?P<id>\d+)/edit/$', views.update_TechTaskview, name='updateTechTask'), 
    url(r'^home/techtasklist(?P<id>\d+)/delete/$', views.delete_TechTaskview, name='deleteTechTask'),
    url(r'^home/clasTechSearch/(?P<clas>[\w\-]+)/search/$', views.clastechSearch, name='clastechSearch'), 
# Feedback URL's
    path('home/allFeedback', views.feedList,name='feedList'), 
    url(r'^home/feedlist(?P<id>[\w\-]+)/edit/$', views.update_feedview, name='updateFeed'), 
    path('feedback/authFeed', views.authFeedList,name='authFeedLogin_before_allFeedList'),
    path('feedback/allFeedback', views.allfeedList,name='allfeedList'), 
    url(r'^feedback/feedlist(?P<id>[\w\-]+)/edit/$', views.authupdate_feedview, name='authUpdateFeed'), 
    url(r'^feedback/feedlist(?P<id>[\w\-]+)/delete/$', views.delete_feedview, name='deleteFeed'), 
# MCQ Panel 
    path('home/createMCQ/', views.create_MCQCourseview,name='createMCQTopic'),
    url(r'^home/createMCQue(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/', views.create_MCQ_Queview,name='createMCQue'),
    path('home/allMCQ_Topic/', views.MCQ_TopicList,name='AllMCQ_Topic_List'),
    path('home/allMCQ_Stu/', views.MCQ_StuList,name='AllMCQ_Student_List'), 
    url(r'^home/allMCQ_Que(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/', views.MCQ_QuizQueList,name='AllMCQ_Que_ListBased_onTitle'), 
    url(r'^home/MCQ_UpdateTopic(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/edit/$', views.update_MCQCourseview, name='updateMCQTopic'), 
    url(r'^home/MCQ_DeleteTopic(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/delete/$', views.delete_MCQCourseview, name='deleteMCQTopic'), 
    url(r'^home/MCQ_Updateque(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/(?P<id>\d+)/edit/$', views.update_MCQ_Queview, name='updateMCQ_Que'), 
    url(r'^home/MCQ_Deleteque(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/(?P<id>\d+)/delete/$', views.delete_MCQ_Queview, name='deleteMCQ_Que'),  
    url(r'^home/MCQ_deleteStu(?P<id>[\w\-]+)/delete/$', views.delete_MCQStu, name='deleteMCQStudent_Result'),
    # MCQ's for Teacher's
    path('Taskhome/authallMCQ', views.authMCQList,name='authallMCQList'),
    path('Taskhome/createMCQ/', views.create_MCQCourseview2,name='authcreateMCQTopic'),
    url(r'^Taskhome/createMCQue(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/', views.create_MCQ_Queview2,name='authcreateMCQue'),
    path('Taskhome/allMTopic/', views.MCQ_TopicList2,name='authAllMCQ_Topic_List'),
    path('Taskhome/allMStu/', views.MCQ_StuList2,name='authAllMCQ_Student_List'), 
    url(r'^Taskhome/allMQue(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/', views.MCQ_QuizQueList2,name='authAllMCQ_Que_ListBased_onTitle'), 
    url(r'^Taskhome/MupdateTopic(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/edit/$', views.update_MCQCourseview2, name='authupdateMCQTopic'), 
    url(r'^Taskhome/MdeleteTopic(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/delete/$', views.delete_MCQCourseview2, name='authdeleteMCQTopic'), 
    url(r'^Taskhome/Mupdateque(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/(?P<id>\d+)/edit/$', views.update_MCQ_Queview2, name='authupdateMCQ_Que'), 
    url(r'^Taskhome/Mdeleteque(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/(?P<id>\d+)/delete/$', views.delete_MCQ_Queview2, name='authdeleteMCQ_Que'),  
    url(r'^Taskhome/MQueDetails/(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/(?P<id>[\w\-]+)/details$', views.detail_MCQ_Queview2, name='authDetailsMCQ_Question_data'),
    url(r'^Taskhome/topicclasSearch/(?P<clas>[\w\-]+)/search/$', views.clasSearchTopic2, name='topic_clasSearch'), 
    url(r'^Taskhome/MdeleteStu(?P<id>[\w\-]+)/(?P<userid>[\w\-]+)/(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/delete/$', views.delete_MCQStu2, name='authdeleteMCQStudent_Result'), 
    url(r'^Taskhome/MCQresDetails/(?P<userid>[\w\-]+)/(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/details$', views.detail_MCQ_StuList2, name='User_ResultWith_Details'),
    url(r'^Taskhome/MCQtestDetails/(?P<userid>[\w\-]+)/(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/details$', views.detail_MCQ_StuTestList2, name='User_Test_Details'),
    url(r'^Taskhome/MCQ_NoResDetails/details$', views.detail_MCQStu_NoRes_List2, name='User_Details_Those_NOresult'),
    url(r'^Taskhome/MCQ_NoRes_Delete/(?P<userid>[\w\-]+)/(?P<title>[\w\-\.\@\[(.*)\]\ ]+)/delete$', views.delete_MCQStu3, name='User_Answer_NoRes_Delate'),
    path('home/alltimedOut', views.timedOutList,name='timedOutList'),  
    url(r'^home/alltimedOut/details/(?P<userid>[\w-]+)', views.timedOutDetail,name='timedOutDetail'), 
    path('home/alloptionalUnit', views.Optional_colDetails, name='detail'), 
    path('Taskhome/createNotesF', views.create_Notesview, name='create_notesFirestore'),  
    path('Taskhome/alllistNotes', views.NotesFire_FileList, name='All-Notes_FireFile_Data'), 
    path('Taskhome/alllistNotesNonAuth', views.NotesFile_ListFire, name='NonAuth_All-Notes_FireFile_Data'),
    url(r'^Taskhome/NotesFlist(?P<id>[\w\-]+)/edit/$', views.update_Notesview, name='authUpdate_NotesFile'),
    url(r'^Taskhome/NotesFlist(?P<id>[\w\-]+)/delete/$', views.delete_Notesview, name='authdelete_NotesFile'),
    url(r'^Taskhome/NotesFlist/(?P<clas>[\w\-]+)/search/$', views.clasSearchNotesview, name='NotesFIleFirebase_clasSearch'),
    path('notesFList/', views.NotesFireFileData.as_view()), 
    path('Taskhome/createNoteiceF', views.create_Noteicesview, name='create_noteiceFirestore'),  
    path('Taskhome/alllistNoteice', views.NoteiceFire_ImageList, name='All-Noteice_FireFile_Data'), 
    path('Taskhome/alllistNoteiceNonAuth', views.NoteiceFile_ListFire, name='NonAuth_All-Noteice_FireFile_Data'),
    url(r'^Taskhome/NoteiceFlist(?P<id>[\w\-]+)/edit/$', views.update_Noteiceview, name='authUpdate_NoteiceFile'),
    url(r'^Taskhome/NoteiceFlist(?P<id>[\w\-]+)/delete/$', views.delete_Noteiceview, name='authdelete_NoteiceFile'),
    url(r'^Taskhome/NoteiceFlist/(?P<clas>[\w\-]+)/search/$', views.clasSearchNoteiceview, name='NoteiceFIleFirebase_clasSearch'),
    # path('noteiceFList/', views.NoteiceFireFileData.as_view()),
    path('Taskhome/listVideo/', views.list_videoF,name='ListVideoData'),
    path('Taskhome/listVideoo/', views.list_videoFL,name='ListVideoData2'), 
    url(r'^Taskhome/updateTVideo(?P<id>[\w\-]+)/', views.updateT_view,name='updateTVideoData'),
    url(r'^Taskhome/updateFVideo(?P<id>[\w\-]+)/', views.updateF_view,name='updateFVideoData'),
    # path('Taskhome/Ncreate/', views.create_Nview,name='createUser'),
# TRY
        # path('profile/', views.profile, name='profile'),
    # path('logout/', views.logout, name='logout')

# UnitTest Data From Firebase
]



