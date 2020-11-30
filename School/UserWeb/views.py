from .forms import *
from TeacherStu.models import *
from django.contrib.auth.models import User as authUser
from . models import Users, FeedbackUser, AuthDeleteUser, ResultUser, MCQUser
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,JsonResponse
from rest_framework import compat
from django.views import View
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.views import APIView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
# These 3 library need to import 
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
from firebase_admin import storage
import json

# Main Dashboard 
def home(request): 
    query = request.GET.get("q", None)
    print(query)
    template = "index.html"
    context = {"object_list": query}
    return render(request, template, context)

# Dashboard for Teacher Login
def TaskHome(request): 
    query = request.GET.get("q", None)
    template = "Taskindex.html"
    context = {"object_list": query}
    return render(request, template, context)

# Create a New Student
def create_view(request):
    query = request.GET.get("q", None)
    form = StuForm(request.POST,request.FILES)
    template = "createUser.html"
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("/home/create/?q="+query)
    else: 
        form = StuForm()   
    return render(request, template, context)


# Get Detail of Particular Student According to Id 
def detail_view(request, userid=None):
    qs = get_object_or_404(Student, userid=userid)
    context = {"object" : qs}
    template = "getUserData.html"
    return render(request, template, context) 

def detail_view_user(request, id=None):
    qs = get_object_or_404(User, id=id)
    context = {"object" : qs}
    template = "getAuthUserData.html"
    return render(request, template, context) 

# Upadate the Data
def update_view(request, userid=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(Student, userid=userid)
    template = "updateUser.html"
    form = StuForm(request.POST or None, instance=obj)
    context = {
                "form": form,
                "code":query
                }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/stuTeachList?q="+query)
    return render(request, template, context)

def update_view_user(request, id=None):
    obj = get_object_or_404(User, id=id)
    template = "updateAuthUser.html"
    form = UserForm(request.POST or None, instance=obj)
    context = {"form": form}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/")
    return render(request, template, context)


# Delete the Data using userid/id
def delete_view(request , userid=None):
    query = request.GET.get("q", None)
    print (query)
    obj = get_object_or_404(Student, userid=userid)
    context = {"object": obj,"code":query}
    template = "delete.html"
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect("/home/stuTeachList?q="+query)
    return render(request, template, context)

def delete_view_user(request , id=None):
    obj = get_object_or_404(User, id=id)
    context = {"object": obj}
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect("/home/")

    template = "deleteAuth.html"
    return render(request, template, context)


# Dashboard Login to acess Data  
def Userdata(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        name = request.POST.get('name')        
        form = UsersLoginForm(request.POST)
        qs = Users.objects.filter(name=name)
        if Users.objects.filter(name=name).exists():
            if (qs.filter(password=password).exists()):
                if form.is_valid():
                    obj = Users.objects.filter(name__iexact=name).values("name")[0]["name"] 
                    context = {"object_list" : obj}
                    template = "index.html" 
                    return render(request, template, context) 
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/userlogin/")
        else:
            messages.info(request, 'Enter the Correct Name!')
            return HttpResponseRedirect("/userlogin/") 
    else: 
        form = UsersLoginForm()   
    return render(request, "userlogin.html", {"form": form})

# Logout Function
def userlogout(request):
    return HttpResponseRedirect("/userlogin/")
 
# Show List of All Data
def stuTeachList(request):
    query = request.GET.get("q", None)
    obj=Student.objects.filter(userid__contains=query).values().order_by('-clas')

    context = {
            "object_list" : obj,
            "code":query
        }
    template = "allList.html"    
    return render(request, template, context)

# def TechTeachList(request):
#     query = request.GET.get("q", None)
#     enable=Student.objects.filter(Enable="True")
#     obj = enable.filter(userid__contains=query,category='TEACHER'
#             ).values("userid","category","clas","name","mobileNum",'Enable').order_by('-clas')
#     context = {
#             "object_list" : obj,
#             "code":query
#         }
#     template = "allList.html"    
#     return render(request, template, context)

@login_required(login_url="/login/")
def usersList(request):
    query = request.GET.get("q", None)
    obj = User.objects.all().values()
    print(authUser.username)
    context = {
            "object_list" : obj,
            "code":query
        }
    template = "allauthList.html"    
    return render(request, template, context)

def authStuTaskList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        form = UsersLoginForm(request.POST)
        if (Users.objects.filter(name=name).exists()):
            qs = name[-3:] 
            user=Users.objects.filter(name=name)
            if (user.filter(password=password).exists()):
                if form.is_valid(): 
                        obj = Stu_Task.objects.filter(school_code=qs).values().order_by('-date')
                        obj_class = Student.objects.order_by().values('clas').distinct()
                        context = {
                                "username" : name,
                                "object_clist" : obj_class,
                                "object_list" : obj,
                                "query":qs
                            }
                        template = "allTaskList2.html" 
                        return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/home/authallTask?q=")
        else:
            messages.info(request, 'Username not exist!!!')
            return HttpResponseRedirect("/home/authallTask?q=")
    else: 
        form = UsersLoginForm()   
    return render(request, "userlogin2.html", {"form": form})

# def stuTaskList(request):
#     query = request.GET.get("q", None)
#     obj = Stu_Task.objects.filter(school_code=query).values().order_by('-date')
#     obj_class = Student.objects.order_by().values('clas').distinct()
#     context = {
#             "object_clist" : obj_class,
#             "object_list" : obj,
#             "code":query
#         }
#     template = "allTaskList.html"    
#     return render(request, template, context)

def stuTaskList2(request):
    query = request.GET.get("q", None)
    obj = Stu_Task.objects.filter(school_code=query).values().order_by('-date')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allTaskList.html"    
    return render(request, template, context)

# def create_Taskview(request):
#     query = request.GET.get("q", None)
#     form = StuTaskForm(request.POST,request.FILES)
#     template = "addNewTask.html"
#     context = {
#             "form" : form,
#             "code":query
#         }
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.save()
#         # messages.success(request, "Successfully Created...!!!")
#         return HttpResponseRedirect("/home/addTask?q="+query)
#     else: 
#         form = StuTaskForm()  
#     return render(request, template, context)

# def update_Taskview(request, id=None):
#     query = request.GET.get("q", None)
#     obj = get_object_or_404(Stu_Task, id=id)
#     template = "updateTask.html"
#     form = StuTaskForm(request.POST or None, instance=obj)
#     context = {"form": form,"code":query}
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.save()
#         return HttpResponseRedirect("/home/allTask?q="+query)
#     return render(request, template, context)

def create_Taskview2(request):
    query = request.GET.get("q", None)
    form = StuTaskForm(request.POST,request.FILES)
    template = "addNewTask2.html"
    context = {
            "form" : form,
            "query":query
        }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Successful...!")
        return render(request, template, context)
    else: 
        form = StuTaskForm()   
    return render(request, template, context)

def update_Taskview2(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(Stu_Task, id=id)
    template = "updateTask2.html"
    form = StuTaskForm(request.POST or None, instance=obj)
    context = {"form": form,"query":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("/home/allTechTask?q="+query)
    return render(request, template, context)

def delete_Taskview2(request , id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(Stu_Task, id=id)
    context = {"object": obj,"query":query}
    template = "deleteTask2.html"
    if request.method == 'POST':
        obj.delete()
        return HttpResponseRedirect("/home/allTechTask?q="+query)
    return render(request, template, context)

def clasSearch2(request, clas=None):
    query = request.GET.get("q", None)
    obj = Stu_Task.objects.filter(school_code=query,clas=clas).values().order_by('-date')
    print(obj)
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allTaskList.html"    
    return render(request, template, context)

def create_Teachview(request):
    query = request.GET.get("q", None)
    form = TeachForm(request.POST,request.FILES)
    template = "addNewTeachTask.html"
    context = {
            "form" : form,
            "code":query
        }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect('/home/allTeachTask?q='+query)
    else: 
        form = TeachForm()   
    return render(request, template, context) 

def teachTaskList(request):
    query = request.GET.get("q", None)
    obj = Teach_Task.objects.filter(school_code=query
            ).values().order_by('id')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }
    template = "allTechTaskList.html"    
    return render(request, template, context)

def update_TechTaskview(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(Teach_Task, id=id)
    template = "updateTask.html"
    form = TeachForm(request.POST or None, instance=obj)
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/allTeachTask?q="+query)
    return render(request, template, context)

def delete_TechTaskview(request , id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(Teach_Task, id=id)
    context = {"object": obj,"code":query}
    template = "deleteTechTask.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allTeachTask?q="+query)
    return render(request, template, context)

def clastechSearch(request, clas=None):
    query = request.GET.get("q", None)
    obj = Teach_Task.objects.filter(school_code=query,clas=clas).values().order_by('id')
    print(obj)
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }
    template = "allTechTaskList.html"    
    return render(request, template, context)

# below code for connecting firebase in the app
# Add new code to get connected with firebase stored data wgich is feedback collections data.
cred = credentials.Certificate("ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'njms-2e633.appspot.com'
}) 
bucket = storage.bucket()
def get_cloud_feed_data(query):
    # firstly connect to cloud frebase. 
    # query = request.GET.get("q", None)
    store = firestore.client()
    datas = store.collection(u'feedback')
    doc_ref = datas.where(u'school',u'==',query)
    # doc = store.collection(u'feedback').document(u'VK1WiKlsROsKzwq8E2lF').get()
    # print(f'Document data: {doc.to_dict()}')
    
    data = []
    try:
        docs = doc_ref.get()
        for doc in docs:
            dic1={}
            dic2=doc.to_dict()            
            dic1['id'] = (doc.id)
            dic1.update(dic2)
            data.append(dic1)
            # print(u'Doc Data:{}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    return data


def feedList(request):
    query = request.GET.get("q", None)
    feedback_list = get_cloud_feed_data(query)
    context = {
            "object_list" : feedback_list,
            "code":query
            }
    template = "allfeedList.html"    
    return render(request, template, context)

def update_feedview(request, id=None):
    query = request.GET.get("q", None)
    template = "updateFeed.html"
    store = firestore.client()
    objs = store.collection(u'feedback').document(id)
    obj = objs.get()
    object_list=obj.to_dict()
    print(object_list)
    form = FeedbackForm(request.POST,request.FILES) 
    context = {
            "form" : form,
            "object_list": object_list,
            "code":query
            }
    if form.is_valid():
        objects = form.save(commit=False)
        objects.save()
        objs.delete()
        return HttpResponseRedirect('/home/allFeedback?q='+query)
    
    template = "updateFeed.html"
    return render(request, template, context) 


def authFeedList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        form = FeedUsersLoginForm(request.POST)
        if (FeedbackUser.objects.filter(name=name).exists()):
            qs = name[-3:] 
            user=FeedbackUser.objects.filter(name=name)
            if (user.filter(password=password).exists()):
                if form.is_valid(): 
                        feedback_list = get_cloud_feed_data(qs)

                        context = {
                                "username" : name,
                                "object_list" : feedback_list,
                                "query":qs
                            }

                        template = "allfeedList2.html"    
                        return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/feedback/authFeed?q=")
        else:
            messages.info(request, 'Username not exist!!!')
            return HttpResponseRedirect("/feedback/authFeed?q=")
    else: 
        form = FeedUsersLoginForm()   
    return render(request, "feeduserlogin.html", {"form": form})

def allfeedList(request):
    qs = request.GET.get("q", None)
    feedback_list = get_cloud_feed_data(qs)
    context = {
            "object_list" : feedback_list,
            "query":qs
            }
    template = "allfeedList2.html"    
    return render(request, template, context)

def authupdate_feedview(request, id=None):
    qs = request.GET.get("q", None)
    template = "updateFeed2.html"
    store = firestore.client()
    objs = store.collection(u'feedback').document(id)
    obj = objs.get()
    object_list=obj.to_dict()
    print(object_list)
    form = FeedbackForm(request.POST,request.FILES) 
    context = {
            "form" : form,
            "object_list": object_list,
            "query":qs
            }
    if form.is_valid():
        objects = form.save(commit=False)
        objects.save()
        objs.delete()
        return HttpResponseRedirect('/feedback/allFeedback?q='+qs)
    
    template = "updateFeed2.html"
    return render(request, template, context) 


def MCQ_TopicList(request):
    query = request.GET.get("q", None)
    obj = MCQ_Post.objects.filter(school=query).values().order_by('title')
    # obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            # "object_clist" : obj_class,
            "object_list" : obj,
            "code":query
        }
    template = "allMCQ_QuizTopic.html"    
    return render(request, template, context)

def create_MCQCourseview(request):
    query = request.GET.get("q", None)
    form = MCQCourseForm(request.POST)
    template = "addMCQ_Topic.html"
    context = {"form": form,"code":query,"message":"Data Save Successfully...!!!"}
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/home/allMCQ_Topic/?q="+query)
    else: 
        form = MCQCourseForm()   
    return render(request, template, context)


def update_MCQCourseview(request, title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    template = "updateMCQTopic.html"
    form = MCQCourseForm(request.POST or None, instance=obj)
    context = {"form": form,"query":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated post!")
        return HttpResponseRedirect("/home/allMCQ_Topic/?q="+query)
    return render(request, template, context)

def delete_MCQCourseview(request , title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    context = {"object": obj,"query":query}
    template = "deleteMCQ_Topic.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allMCQ_Topic?q="+query)
    return render(request, template, context)

def MCQ_QuizQueList(request, title=None):
    # title = 'Quizz'
    query = request.GET.get("q", None)
    objs = MCQ_Question.objects.filter(MCQPost_id__school__contains=query)
    obj = objs.filter(MCQPost_id__title__contains=title).values()
    # obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "title" : title,
            "object_list" : obj,
            "code":query
        }
    template = "allMCQ_QuizQue.html"    
    return render(request, template, context)

def create_MCQ_Queview(request, title=None):
    query = request.GET.get("q", None)
    form = MCQ_QueForm(request.POST,request.FILES)
    template = "addMCQ_Que.html"
    context = {"form": form,"objs": title,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/home/createMCQue"+title+"?q="+query)
    else: 
        form = MCQ_QueForm()   
    return render(request, template, context)

def update_MCQ_Queview(request, title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    template = "updateMCQ_Que.html"
    form = MCQ_QueForm(request.POST or None, instance=obj)
    context = {"obj": obj,"objs": title,"query":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated Post Successfully!")
        return HttpResponseRedirect("/home/allMCQ_Que"+title+"?q="+query)
    return render(request, template, context)

def delete_MCQ_Queview(request,title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    context = {"object": obj,"objs": title,"query":query}
    template = "deleteMCQ_Que.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allMCQ_Que"+title+"?q="+query)
    return render(request, template, context)

def MCQ_StuList(request):
    query = request.GET.get("q", None)
    obj = MCQ_Result.objects.filter(userid__icontains=query).values().order_by('title')
    context = {
            "object_list" : obj,
            "code":query
        }
    template = "allMCQ_AttStuList.html"    
    return render(request, template, context)

def delete_MCQStu(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Result, id=id)
    context = {"object": obj,"code":query}
    template = "deleteMCQ_Stu.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allMCQ_Stu?q="+query)
    return render(request, template, context)

def authMCQList(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = MCQLoginForm(request.POST)
        if (MCQUser.objects.filter(username=username).exists()):
            query = username[-3:] 
            user=MCQUser.objects.filter(username=username)
            if (user.filter(password=password).exists()):
                if form.is_valid(): 
                        obj = MCQ_Post.objects.filter(school=query).values().order_by('title')
                        obj_class = Student.objects.order_by().values('clas').distinct()
                        context = {
                                "object_clist" : obj_class,
                                "object_list" : obj,
                                "query":query
                            }
                        template = "allMCQ_QuizTopic2.html" 
                        return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                return HttpResponseRedirect("/Taskhome/authallMCQ?q=")
        else:
            messages.info(request, 'Username not exist!!!')
            return HttpResponseRedirect("/Taskhome/authallMCQ?q=")
    else: 
        form = MCQLoginForm()   
    return render(request, "userloginMCQAuth.html", {"form": form})

def clasSearchTopic2(request, clas=None):
    query = request.GET.get("q", None)
    obj = MCQ_Post.objects.filter(school=query,clas=clas).values().order_by('title')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allMCQ_QuizTopic2.html"    
    return render(request, template, context)


def MCQ_TopicList2(request):
    query = request.GET.get("q", None)
    obj = MCQ_Post.objects.filter(school=query).values().order_by('title')
    obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "object_clist" : obj_class,
            "object_list" : obj,
            "query":query
        }
    template = "allMCQ_QuizTopic2.html"    
    return render(request, template, context)

def create_MCQCourseview2(request):
    query = request.GET.get("q", None)
    form = MCQCourseForm(request.POST)
    template = "addMCQ_Topic2.html"
    context = {
            "form": form,
            "query":query
            }
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/Taskhome/allMTopic?q="+query)
    else: 
        form = MCQCourseForm()   
    return render(request, template, context)

def update_MCQCourseview2(request, title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    template = "updateMCQTopic2.html"
    form = MCQCourseForm(request.POST or None, instance=obj)
    context = {
            "form": form,
            "query":query
            }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated post!")
        return HttpResponseRedirect("/Taskhome/allMTopic?q="+query)
    return render(request, template, context)

def delete_MCQCourseview2(request , title=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Post, title=title)
    context = {
            "object": obj,
            "query":query
            }
    template = "deleteMCQ_Topic2.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/Taskhome/allMTopic?q="+query)
    return render(request, template, context)

def MCQ_QuizQueList2(request, title=None):
    # title = 'Quizz'
    query = request.GET.get("q", None)
    objs = MCQ_Question.objects.filter(MCQPost_id__school__contains=query)
    obj = objs.filter(MCQPost_id__title=title).values()
    # obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            "title" : title,
            "object_list" : obj,
            "query":query
        }
    template = "allMCQ_QuizQue2.html"    
    return render(request, template, context)

def create_MCQ_Queview2(request, title=None):
    query = request.GET.get("q", None)
    form = MCQ_QueForm(request.POST,request.FILES)
    template = "addMCQ_Que2.html"
    context = {
            "form": form,
            "objs": title,
            "query":query
            }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, 'Data Save Successfully!')
        return HttpResponseRedirect("/Taskhome/createMCQue"+title+"?q="+query)
    else: 
        form = MCQ_QueForm()   
    return render(request, template, context)

def detail_MCQ_Queview2(request,title=None, id=None):
    query = request.GET.get("q", None)
    qs = get_object_or_404(MCQ_Question, id=id)
    context = {
            "object" : qs,
            "objs": title,
            "query":query
            }
    template = "getQueData.html"
    return render(request, template, context)


def update_MCQ_Queview2(request, title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    template = "updateMCQ_Que2.html"
    form = MCQ_QueForm(request.POST or None,request.FILES,instance=obj)
    context = {
            "form":form,
            "obj": obj,
            "objs": title,
            "query":query
            }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        # messages.success(request, "Updated Post Successfully!")
        return HttpResponseRedirect("/Taskhome/allMQue"+title+"?q="+query)
    return render(request, template, context)

def delete_MCQ_Queview2(request,title=None, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(MCQ_Question, id=id)
    context = {
            "object": obj,
            "objs": title,
            "query":query
            }
    template = "deleteMCQ_Que2.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/Taskhome/allMQue"+title+"?q="+query)
    return render(request, template, context)
    
def loginpage(request):
    # query = request.GET.get("q", None)
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        
        query=username[-3:]
        print(query)
        if(ResultUser.objects.filter(username=username,password=password).exists()):
            post = ResultUser.objects.filter(username=username)
            if post:
                username = request.POST['username']
                request.session['username'] = username
                print("Successfully")
                return HttpResponseRedirect("/Taskhome/allMStu/?q="+query)
            else:
                print("Failed")
                return render(request, 'login1.html', {})
        else:
            messages.info(request, 'Username or Password not exist!!!')
            return render(request, 'login1.html', {})
    return render(request, 'login1.html', {})

# def logout(request):
#     try:
#         del request.session['username']
#     except:
#      pass
#     return render(request, 'login1.html', {})

def MCQ_StuList2(request):
    query = request.GET.get("q", None)
    if request.session.has_key('username'):
        print("Successfully")
        if request.method == 'POST':
            clas = request.POST.get('clas')
            # subject = request.POST.get('subject')
            form = MCQ_ResultFind(request.POST)
            print(clas)
            if form.is_valid(): 
                obj = MCQ_Result.objects.filter(userid__icontains=query,clas=clas).values().order_by('created_at')
                context = {
                        "object_list" : obj,
                        "query":query
                    }
                template = "allMCQ_AttStuList2.html"    
                return render(request, template, context)
        else: 
            form = MCQ_ResultFind()   
            return render(request, "userResult.html", {"form": form})
    else:
        return HttpResponseRedirect("/signin?q="+query)


def detail_MCQ_StuList2(request,userid=None,title=None):
    query = request.GET.get("q", None)
    if request.session.has_key('username'):
        school = userid[0:3]
        qs = get_object_or_404(Student, userid__icontains=school,userid=userid)
        pq = get_object_or_404(MCQ_Result, userid=userid,title=title)
        context = {
                "obj": pq,
                "object" : qs,
                "query":query
                }
        template = "getResUserDetails.html"
        return render(request, template, context)
    else:
        return HttpResponseRedirect("/signin?q="+query)

# def detail_MCQ_StuList3(request,userid=None,title=None):
#     query = request.GET.get("q", None)
#     school = userid[0:3]
#     qs = get_object_or_404(Student, userid__icontains=school,userid=userid)
#     # pq = get_object_or_404(MCQ_Result, userid=userid,title=title)
#     context = {
#             # "obj": pq,
#             "object" : qs,
#             "query":query
#             }
#     template = "getResUserDetails.html"
#     return render(request, template, context)

def detail_MCQ_StuTestList2(request,userid=None,title=None):
    query = request.GET.get("q", None)
    school = userid[0:3]
    queData = MCQ_Answer.objects.filter(userid=userid,title=title).values()
    # cAnsData = get_object_or_404(MCQ_Question, MCQPost_id__title__contains=title)
    context = {
            "object_list": queData,
            # "object_correct" : cAnsData,
            "query":query
            }
    template = "getStuQuesAnsData.html"
    return render(request, template, context)

def delete_MCQStu2(request, id=None,userid=None,title=None):
    query = request.GET.get("q", None)
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        form = AuthDeleteLoginForm(request.POST)
        if (AuthDeleteUser.objects.filter(name=name).exists()):
            user=AuthDeleteUser.objects.filter(name=name)
            if (user.filter(password=password).exists()):
                objResult = get_object_or_404(MCQ_Result, id=id)
                objAnswer = MCQ_Answer.objects.filter(userid=userid,title=title)
                context = {
                        "object": objResult,
                        "objectAns": objAnswer,
                        "query":query
                        }
                template = "deleteMCQ_Stu2.html"
                if request.method == 'POST':
                    objResult.delete()
                    objAnswer.delete()
                    return HttpResponseRedirect("/Taskhome/allMStu?q="+query)
            else:
                messages.info(request, 'Enter the Correct Password!')
                form = AuthDeleteLoginForm()   
                return render(request, "userlogin3.html", {"form": form})
        else:
            messages.info(request, 'Username not exist!!!')
            form = AuthDeleteLoginForm()   
            return render(request, "userlogin3.html", {"form": form})
    else: 
        form = AuthDeleteLoginForm()   
    return render(request, "userlogin3.html", {"form": form})

from django.db.models import Q
def detail_MCQStu_NoRes_List2(request):
    query = request.GET.get("q", None)
    if request.session.has_key('username'):
        user=MCQ_Result.objects.all().values_list('userid',flat=True)
        title=MCQ_Result.objects.all().values_list('title',flat=True)
        obj = MCQ_Answer.objects.filter(userid__icontains=query).exclude(Q(userid__in=user) & Q(title__in=title)).values('userid','title','clas','subject').distinct()
        context = {
                "object_list" : obj,
                "query":query
            }
        template = "allMCQ_AttStuList3.html"    
        return render(request, template, context)
    else:
        return HttpResponseRedirect("/signin?q="+query)

def delete_MCQStu3(request,userid=None,title=None):
    query = request.GET.get("q", None)
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        form = AuthDeleteLoginForm(request.POST)
        if (AuthDeleteUser.objects.filter(name=name).exists()):
            user=AuthDeleteUser.objects.filter(name=name)
            if (user.filter(password=password).exists()):
                # objResult = get_object_or_404(MCQ_Result, id=id)
                objAnswer = MCQ_Answer.objects.filter(userid=userid,title=title)
                context = {
                        # "object": objResult,
                        "objectAns": objAnswer,
                        "query":query
                        }
                template = "deleteMCQ_Stu2.html"
                if request.method == 'POST':
                    # objResult.delete()
                    objAnswer.delete()
                    return HttpResponseRedirect("/Taskhome/MCQ_NoResDetails/details?q="+query)
            else:
                messages.info(request, 'Enter the Correct Password!')
                form = AuthDeleteLoginForm()   
                return render(request, "userlogin3.html", {"form": form})
        else:
            messages.info(request, 'Username not exist!!!')
            form = AuthDeleteLoginForm()   
            return render(request, "userlogin3.html", {"form": form})
    else: 
        form = AuthDeleteLoginForm()   
    return render(request, "userlogin3.html", {"form": form})

def NewsDataList(request):
    query = request.GET.get("q", None)
    obj = News.objects.all()

    context = {
            "object_list" : obj,
            "code":query
        }
    template = "allNewsDataList.html"    
    return render(request, template, context)

def create_NewsData(request, id=None):
    query = request.GET.get("q", None)
    form = NewsDataForm(request.POST,request.FILES)
    template = "addNewsData.html"
    # context = {"form": form,"code":query,'typeList':_dict}
    _dict = {}
    # context={}
    if "search" in request.POST:
        school_code = request.POST.get("school_code")
        class_code = request.POST.get("class_code")
        data = Student.objects.filter(clas=class_code,userid__icontains=school_code).values_list('name',flat=True)
        
        for x in range(len(data)):
            _dict[data[x]] = data[x]
    
    context = {"form": form,"code":query,'typeList':_dict}

    if form.is_valid():
        if "save" in request.POST:
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, 'Data Save Successfully!')
            return HttpResponseRedirect("/home/allNewsData?q="+query)
    else: 
        form = NewsDataForm()      
    return render(request, template, context) 

def update_NewsData(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(News, id=id)
    template = "updateNews.html"
    form = NewsDataForm(request.POST or None, instance=obj)
    _dict = {}

    # context = {"form": form,"query":query}
    if "search" in request.POST:
        school_code = request.POST.get("school_code")
        class_code = request.POST.get("class_code")
        data = Student.objects.filter(clas=class_code,userid__icontains=school_code).values_list('name',flat=True)
        
        for x in range(len(data)):
            _dict[data[x]] = data[x]
    context = {"form": form,"query":query,'typeList':_dict} 
    if form.is_valid():
        if "save" in request.POST:
            obj = form.save(commit=False)
            obj.save()
            # messages.success(request, "Updated Post Successfully!")
            return HttpResponseRedirect("/home/allNewsData?q="+query)
    return render(request, template, context)

def delete_NewsData(request, id=None):
    query = request.GET.get("q", None)
    obj = get_object_or_404(News, id=id)
    context = {"object": obj,"query":query}
    template = "deleteNewsData.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/home/allNewsData?q="+query)
    return render(request, template, context)


def delete_feedview(request , id=None):

    query = request.GET.get("q", None)
    print (query)
    store = firestore.client()
    obj = store.collection(u'feedback').document(id)
    # obj = get_object_or_404(Feedback, id=id)
    context = {"object": obj,"code":query}
    template = "deleteFeed.html"
    if request.method == 'POST':
        obj.delete()
        # messages.success(request, "Post Deleted...!")
        return HttpResponseRedirect("/feedback/allFeedback?q="+query)
    return render(request, template, context)


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
def NoteData(query):
    store = firestore.client()
    datas = store.collection(u'notes')
    doc_ref = datas.where(u'school',u'==',query)
    data = []
    try:
        docs = doc_ref.get()
        for doc in docs:
            dic1={}
            dic2=doc.to_dict() 
            dic1['id'] = (doc.id)  
            dic1.update(dic2)         
            data.append(dic1)
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    return data
def NotesFire_FileList(request):
    query = request.GET.get("q", None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        query = username[-3:] 
        # print(query)
        form = NotesFireLoginForm(request.POST)
        if (NotesFirebaseFile_User.objects.filter(username=username).exists()):
            user=NotesFirebaseFile_User.objects.filter(username=username)
            if (user.filter(password=password).exists()):
                # objResult = get_object_or_404(MCQ_Result, id=id)
                data = NoteData(query)

                # print(data)
                context = {
                        "object_list" : data,
                        "query":query
                        }
                template = "allListNotesFireFile.html"
                return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                form = NotesFireLoginForm()   
                return render(request, "userloginNotesFireFile.html", {"form": form})
        else:
            messages.info(request, 'Username not exist!!!')
            form = NotesFireLoginForm()   
            return render(request, "userloginNotesFireFile.html", {"form": form})
    else: 
        form = NotesFireLoginForm()   
    return render(request, "userloginNotesFireFile.html", {"form": form})

def NotesFile_ListFire(request):
    query = request.GET.get("q", None)
    data = NoteData(query)
    # print(data)
    context = {
            "object_list" : data,
            "query":query
            }
    template = "allListNotesFireFile.html"
    return render(request, template, context)

def create_Notesview(request):
    query = request.GET.get("q", None)
    # print(query)
    template = "notesFirestoreCreate.html"
    store = firestore.client()
    form = NotesFormFirestore(request.POST,request.FILES) 
    context = {
                "form" : form,
                "query":query
                }
    if request.method == 'POST':
        if form.is_valid():
            school = request.POST.get("school")
            clas = request.POST.get("clas")
            subject = request.POST.get("subject")
            title = request.POST.get("title")
            desc = request.POST.get("description")
            pdf = request.POST.get("pdf_upload")

            data = {
                u'school': school,u'clas': clas,u'subject': subject,u'title': title,u'description': desc,u'pdf_upload': pdf,
                }
            print(data)

            objC = store.collection(u'notes').add(data)

            messages.success(request, 'Data Save Successfully!')
            return HttpResponseRedirect('/Taskhome/createNotesF?q='+query)
    
    template = "notesFirestoreCreate.html"
    return render(request, template, context)

def clasSearchNotesview(request, clas=None):
    query = request.GET.get("q", None)
    print(query,clas)
    store = firestore.client()
    datas = store.collection(u'notes')
    doc_ref = datas.where(u'school',u'==',query).where(u'clas',u'==',clas)
    docs = doc_ref.get()
    data = []
    try:
        for doc in docs:
            dic1={}
            dic2=doc.to_dict() 
            dic1['id'] = (doc.id)  
            dic1.update(dic2)         
            data.append(dic1)
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    context = {
            "object_list" : data,
            "query":query
        }
    template = "allListNotesFireFile.html"    
    return render(request, template, context)

def update_Notesview(request, id=None):
    query = request.GET.get("q", None)
    template = "updateNotesFireFile.html"
    store = firestore.client()
    objs = store.collection(u'notes').document(id)
    obj = objs.get()
    object_list=obj.to_dict()
    print(object_list)
    form = NotesFormFirestore(request.POST,request.FILES) 
    context = {
            "form" : form,
            "object_list": object_list,
            "query":query
            }
    if form.is_valid():
        school = request.POST.get("school")
        clas = request.POST.get("clas")
        subject = request.POST.get("subject")
        title = request.POST.get("title")
        desc = request.POST.get("description")
        pdf = request.POST.get("pdf_upload")

        data = {
            u'school': school,u'clas': clas,u'subject': subject,u'title': title,u'description': desc,u'pdf_upload': pdf,
            }
        print(data)
        objs.update(data)
        return HttpResponseRedirect('/Taskhome/NotesFlist/'+clas+'/search/?q='+query)
    
    template = "updateNotesFireFile.html"
    return render(request, template, context)

def delete_Notesview(request, id=None):
    query = request.GET.get("q", None)
    # template = "updateNotesFireFile.html"
    store = firestore.client()
    objs = store.collection(u'notes').document(id)
    objs.delete()
    messages.success(request, 'Data Delete Successfully!')
    return HttpResponseRedirect('/Taskhome/alllistNotesNonAuth?q='+query)

class NotesFireFileData(APIView):

    def get(self, request):
        store = firestore.client()
        doc_ref = store.collection(u'notes')
        # doc_ref = datas.where(u'school',u'==',query)
        data = []
        try:
            docs = doc_ref.get()
            for doc in docs:
                dic1={}
                dic2=doc.to_dict() 
                dic1['id'] = (doc.id)  
                dic1.update(dic2)         
                data.append(dic1)
        except google.cloud.exceptions.NotFound:
            print(u'Missing data')
        stu_list=data
        mesg=list(stu_list)
        return Response(mesg)

    def post(self, request):
        data=self.request.data
        school = data.get('school')
        clas = data.get('clas')
        print(school,clas)
        print(len(school))
        if (school is None or len(school)==0) | (clas is None or len(clas)==0):
            return Response({"Error":"Plese Enter Valid School And Class"})
        else:
            store = firestore.client()
            datas = store.collection(u'notes')
            doc_ref = datas.where(u'school',u'==',school).where(u'clas',u'==',clas)
            docs = doc_ref.get()
            data = []
            try:
                for doc in docs:
                    dic1={}
                    dic2=doc.to_dict() 
                    dic1['id'] = (doc.id)  
                    dic1.update(dic2)         
                    data.append(dic1)
            except google.cloud.exceptions.NotFound:
                print(u'Missing data')
            stu_list=data
            mesg=list(stu_list)
            return Response(mesg)


def NoteiceData(query):
    store = firestore.client()
    # doc_ref = store.collection(u'unitTest').document(id)
    datas = store.collection(u'noticeImage')
    # obj = doc_ref.get()
    # object_list=obj.to_dict()
    # print(object_list)
    doc_ref = datas.where(u'school',u'==',query)
    data = []
    try:
        docs = doc_ref.get()
        for doc in docs:
            dic1={}
            dic2=doc.to_dict() 
            dic1['id'] = (doc.id)  
            dic1.update(dic2)         
            data.append(dic1)
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    # print("NoticeImage Data",data)
    return data

# NoteiceData('DEO8084_IX_null')

def NoteiceFire_ImageList(request):
    query = request.GET.get("q", None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        query = username[-3:] 
        # print(query)
        form = NotesFireLoginForm(request.POST)
        if (NotesFirebaseFile_User.objects.filter(username=username).exists()):
            user=NotesFirebaseFile_User.objects.filter(username=username)
            if (user.filter(password=password).exists()):
                # objResult = get_object_or_404(MCQ_Result, id=id)
                data = NoticeImage.objects.filter(school=query)

                # print(data)
                context = {
                        "object_list" : data,
                        "query":query
                        }
                template = "allListNoteiceFireFile.html"
                return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                form = NotesFireLoginForm()   
                return render(request, "userloginNoteiceFireFile.html", {"form": form})
        else:
            messages.info(request, 'Username not exist!!!')
            form = NotesFireLoginForm()   
            return render(request, "userloginNoteiceFireFile.html", {"form": form})
    else: 
        form = NotesFireLoginForm()   
    return render(request, "userloginNoteiceFireFile.html", {"form": form})

def NoteiceFile_ListFire(request):
    query = request.GET.get("q", None)
    data = NoticeImage.objects.filter(school=query).values()
    # print(data)
    context = {
            "object_list" : data,
            "query":query
            }
    template = "allListNoteiceFireFile.html"
    return render(request, template, context)

def create_Noteicesview(request):
    query = request.GET.get("q", None)
    template = "noteiceFirestoreCreate.html"
    form = NoticeImageForm(request.POST,request.FILES) 
    context = {
                "form" : form,
                "query":query
                }
    if request.method == 'POST':
        if form.is_valid():
            school = request.POST.get("school")
            image = request.FILES.get("que_Image")
            classP = request.POST.get("classP")
            classU = request.POST.get("classU")
            classL = request.POST.get("classL")
            classI = request.POST.get("classI")
            classII = request.POST.get("classII")
            classIII = request.POST.get("classIII")
            classIV = request.POST.get("classIV")
            classV = request.POST.get("classV")
            classVI = request.POST.get("classVI")
            classVII = request.POST.get("classVII")
            classVIII = request.POST.get("classVIII")
            classIX = request.POST.get("classIX")
            classX = request.POST.get("classX")
            classXI = request.POST.get("classXI")
            classXII = request.POST.get("classXII")
            clas = [classP,classU,classL,classI,classII,classIII,classIV,classV,classVI,classVII,classVIII,classIX,classX,classXI,classXII]
            
            objC = NoticeImage.objects.create(school=school,clas=clas,que_Image=image)
            objC.save()

            messages.success(request, 'Data Save Successfully!')
            return HttpResponseRedirect('/Taskhome/createNoteiceF?q='+query)
    
    template = "noteiceFirestoreCreate.html"
    return render(request, template, context)

def clasSearchNoteiceview(request, clas=None):
    query = request.GET.get("q", None)
    print(query,clas)
    data = NoticeImage.objects.filter(clas__contains=clas,school=query)
    context = {
            "object_list" : data,
            "query":query
        }
    template = "allListNoteiceFireFile.html"    
    return render(request, template, context)

def update_Noteiceview(request, id=None):
    query = request.GET.get("q", None)
    datas = get_object_or_404(NoticeImage, id=id)
    template = "updateNoteiceFireFile.html"
    form = NoticeImageForm(request.POST,request.FILES) 
    context = {
            "form" : form,
            "object_list": datas,
            "query":query
            }
    if request.method == 'POST':
        if form.is_valid():
            school = request.POST.get("school")
            image = request.FILES.get("que_Image")
            classP = request.POST.get("classP")
            classU = request.POST.get("classU")
            classL = request.POST.get("classL")
            classI = request.POST.get("classI")
            classII = request.POST.get("classII")
            classIII = request.POST.get("classIII")
            classIV = request.POST.get("classIV")
            classV = request.POST.get("classV")
            classVI = request.POST.get("classVI")
            classVII = request.POST.get("classVII")
            classVIII = request.POST.get("classVIII")
            classIX = request.POST.get("classIX")
            classX = request.POST.get("classX")
            classXI = request.POST.get("classXI")
            classXII = request.POST.get("classXII")
            clas = [classP,classU,classL,classI,classII,classIII,classIV,classV,classVI,classVII,classVIII,classIX,classX,classXI,classXII]
            print(clas)
            # data = {
            #     u'school': school,u'image': image,u'classP':classP,u'classU':classU,u'classL':classL,
            #     u'classI':classI,u'classII':classII,u'classIII':classIII,u'classIV':classIV,u'classV':classV,u'classVI':classVI,
            #     u'classVII':classVII,u'classVIII':classVIII,u'classIX':classIX,u'classX':classX,u'classXI':classXI,u'classXII':classXII,
            #     }
            data = {
                u'school': school,u'image': image,u'classes':clas
                }
            print(data)
            NoticeImage.objects.filter(id=id).update(clas=clas,que_Image=image)
            messages.success(request, 'Data Updated Successfully!')
            # objs.delete()  
            return HttpResponseRedirect('/Taskhome/alllistNoteiceNonAuth?q='+query)
    
    template = "updateNoteiceFireFile.html"
    return render(request, template, context)

def delete_Noteiceview(request, id=None):
    query = request.GET.get("q", None)
    store = firestore.client()
    datas = store.collection(u'noticeImage')
    print('Deleted',id)
    objs = datas.document(id).delete()
    messages.success(request, 'Data Delete Successfully!')
    return HttpResponseRedirect('/Taskhome/alllistNoteiceNonAuth?q='+query)

class NoteiceFireFileData(APIView):

    def get(self, request):
        store = firestore.client()
        # doc_ref = store.collection(u'unitTest').document(id)
        doc_ref = store.collection(u'noticeImage')
        # obj = doc_ref.get()
        # object_list=obj.to_dict()
        # print(object_list)
        # doc_ref = datas.where(u'school',u'==',query)
        data = []
        try:
            docs = doc_ref.get()
            for doc in docs:
                dic1={}
                dic2=doc.to_dict() 
                dic1['id'] = (doc.id)  
                dic1.update(dic2)         
                data.append(dic1)
        except google.cloud.exceptions.NotFound:
            print(u'Missing data')
        print("NoticeImage Data",data)
        # return data
        stu_list=data
        mesg=list(stu_list)
        return Response(mesg)

    def post(self, request):
        data=self.request.data
        school = data.get('school')
        clas = data.get('clas')
        print(school,clas)
        print(len(school))
        if (school is None or len(school)==0) | (clas is None or len(clas)==0):
            return Response({"Error":"Plese Enter Valid School"})
        else:
            store = firestore.client()
            # doc_ref = store.collection(u'unitTest').document(id)
            datas = store.collection(u'noticeImage')
            # obj = doc_ref.get()
            # object_list=obj.to_dict()
            # print(object_list)
            doc_ref = datas.where(u'school',u'==',school).where(u'classes',u'array_contains',clas)
            data = []
            try:
                docs = doc_ref.get()
                for doc in docs:
                    dic1={}
                    dic2=doc.to_dict() 
                    dic1['id'] = (doc.id)  
                    dic1.update(dic2)         
                    data.append(dic1)
            except google.cloud.exceptions.NotFound:
                print(u'Missing data')
            print("NoticeImage Data",data)
            stu_list=data
            mesg=list(stu_list)
            return Response(mesg)

# Create a New Student
def create_Videoview(request):
    query = request.GET.get("q", None)
    form = VideoForm(request.POST,request.FILES)
    template = "createvideoF.html"
    context = {"form": form,"code":query}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Successfully Save Data...!")
        # return HttpResponseRedirect("/Taskhome/")
    else: 
        form = VideoForm()   
    return render(request, template, context)

# class videoFLive(TemplateView):
   
def list_videoF(request):
    query = request.GET.get("q", None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        query = username[-3:] 
        print(query)
        form = NotesFireLoginForm(request.POST)
        if (NotesFirebaseFile_User.objects.filter(username=username).exists()):
            user=NotesFirebaseFile_User.objects.filter(username=username)
            if (user.filter(password=password).exists()):
                # query = request.GET.get("q", None)
                objT = videoF.objects.filter(flag=True,school=query).values()
                objF = videoF.objects.filter(flag=False,school=query).values()
                print(objT,objF)
                # obj_class = Student.objects.order_by().values('clas').distinct()
                context = {
                        # "object_clist" : obj_class,
                        "object_Tlist" : objT,
                        "object_Flist" : objF,
                        "query":query
                    }
                template = "createvideoF.html"    
                return render(request, template, context)
            else:
                messages.info(request, 'Enter the Correct Password!')
                form = NotesFireLoginForm()   
                return render(request, "UserLoginclassStatus.html", {"form": form})
        else:
            messages.info(request, 'Username not exist!!!')
            form = NotesFireLoginForm()   
            return render(request, "UserLoginclassStatus.html", {"form": form})
    else: 
        form = NotesFireLoginForm()   
    return render(request, "UserLoginclassStatus.html", {"form": form}) 

def list_videoFL(request):
    query = request.GET.get("q", None)
    print(query)
    objT = videoF.objects.filter(flag=True,school=query)
    objF = videoF.objects.filter(flag=False,school=query)
    # obj_class = Student.objects.order_by().values('clas').distinct()
    context = {
            # "object_clist" : obj_class,
            "object_Tlist" : objT,
            "object_Flist" : objF,
            "query":query
        }
    template = "createvideoF.html"    
    return render(request, template, context)

# Upadate the Data
def updateF_view(request, id=None):
    query = request.GET.get("q", None)
    obj = videoF.objects.filter(id=id).update(flag=False)
    return HttpResponseRedirect("/Taskhome/listVideoo?q="+query)

def updateT_view(request, id=None):
    query = request.GET.get("q", None)
    obj = videoF.objects.filter(id=id).update(flag=True)
    return HttpResponseRedirect("/Taskhome/listVideoo?q="+query)
            
        # if (MCQ_Post.objects.filter(school=school).exists()):
        #     scode = MCQ_Post.objects.filter(school=school)
        #     if (scode.filter(clas=clas).exists()):
        #         clas_list=scode.filter(clas=clas).values()
        #         serializer=MCQ_PostSerializer(clas_list,many=True)
        #         return Response(serializer.data)
        #     else:
        #         return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 


    # obj = objs.get()
    # object_list=obj.to_dict()
    # print(object_list)
    # form = NotesFormFirestore(request.POST,request.FILES) 
    # context = {
    #         "form" : form,
    #         "object_list": object_list,
    #         "query":query
    #         }
    # if form.is_valid():
    #     objects = form.save(commit=False)
    #     # objects.save()
    #     objs.delete()
    #     return HttpResponseRedirect('/Taskhome/alllistNotesNonAuth?q='+query)
    
    # template = "updateNotesFireFile.html"
    # return render(request, template, context)
# def createFeedview(request):
#     query = request.GET.get("q", None)
#     form = FeedbackForm(request.POST,request.FILES)
#     template = "addFeedback.html"
#     context = {
#             "form" : form,
#             "code":query
#         }
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.save()
#         return HttpResponseRedirect('/home/allFeedback?q='+query)
#     else: 
#         form = FeedbackForm()   
#     return render(request, template, context)

# def stuTeachList(request):
#     query = request.GET.get("q", None)
#     print(query)
#     obj = Student.objects.filter(userid__startswith=query,category="STUDENT"
#             ).values("userid","category","name","mobileNum").order_by('-id')
#     context = {
#             "object_list" : obj,
#             "code":query
#         }
#     template = "allList.html"    
#     return render(request, template, context)
    

# def unitTest():
#     #query = request.GET.get("id", None)
#     #print(query)
#     # cred = credentials.Certificate('unitTest_Firebase.json')
#     # firebase_admin.initialize_app(cred, {'databaseURL'})
#     db = firestore.client()
#     doc_ref = db.collection(u'unitTest').limit(1)
#     # doc_ref1 = doc_ref.where(u'reg', u'==', u'DEO7759').get()
#     # print(doc_ref1)
#     data = []
#     try:
#         docs = doc_ref.get()
#         for doc in docs:
#             dic2 = {}
#             dic2=doc.to_dict()            
#             # dic1['id'] = (doc.id)
#             # dic1.update(dic2)
#             data.append(dic2)
#             # print(f'{doc.to_dict()}')
#             print(data)
#     except google.cloud.exceptions.NotFound:
#         print(u'Missing data')
#     return data

# def detail(request):
#     query = request.GET.get("q", None)
#     feedback_list = unitTest()
#     context = {
#             "object_list" : feedback_list,
#             "code":query
#             }
#     template = "unittest.html"    
#     return render(request, template, context)
    # context = {
    #         "object_list" : obj
    #     }
    # template = "unittestlist.html"
    # return render(request, template, context)

def Optional_colDetails(request):
    store = firestore.client()
    doc_ref = store.collection(u'optional_unit')
    data = []
    try:
        docs = doc_ref.get()
        for doc in docs:
            dic1={}
            dic2=doc.to_dict() 
            dic1['id'] = (doc.id)  
            dic1.update(dic2)         
            data.append(dic1)
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')

    # print(data)
    context = {
            "object_list" : data
            }
    template = "Option_UnitDB.html"
    return render(request, template, context)

def get_cloud_timedOut_data():
    store = firestore.client()
    doc_ref = store.collection(u'timedOut')
    data = []
    try:
        docs = doc_ref.get()
        for doc in docs:
            dic1={}
            dic2=doc.to_dict()            
            # dic1['id'] = (doc.id)
            # dic1.update(dic2)
            data.append(dic2)

            # print(u'Doc Data:{}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    # print(data)
    return data


def timedOutList(request):
    query = request.GET.get("q", None)
    timedOut_list = get_cloud_timedOut_data()
    context = {
            "object_list" : timedOut_list,
            "code":query
            }
    template = "alltimedOut.html"    
    return render(request, template, context) 

def timedOutDetail(request,userid=None):
    qs = get_object_or_404(Student,userid=userid)
    context = {
            "object" : qs,
            # "code":query
            }
    template = "getUserDetails.html"    
    return render(request, template, context)

def listData(query):
    data = []
    try:
        docs = query.get()
        for doc in docs:
            dic2=doc.to_dict()            
            data.append(dic2)
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    return data

# def get_cloud_unitCount_data():
#     data = []
#     store = firestore.client()
#     doc_col = store.collection(u'unitCount')
#     next_query = doc_col.order_by(u'data.reg').limit(100)
#     data.extend(listData(next_query))
#     # documents = list(doc_col.get())
#     # print("# of documents in collection: {}".format(len(documents)))
#     # next_query = doc_col.order_by(u'data.reg').start_at({u'data.reg':u'KAS'})
#     # print(datas)
#     # data2 = {}
#     # reg =[]
#     docs1 = next_query.stream()
#     last_doc = list(docs1)[-1]
#     last_pop = last_doc.to_dict()[u'data']
#     next_query = doc_col.order_by(u'data').start_after({u'data': last_pop}).limit(100)
#     data.extend(listData(next_query))
#     # print('List 1 ----------------',list1)

#     docs1 = next_query.stream()
#     last_doc = list(docs1)[-1]
#     last_pop = last_doc.to_dict()[u'data']
#     next_query = (doc_col.order_by(u'data').start_after({u'data': last_pop}).limit(100))
#     data.extend(listData(next_query))
#     # print('List 2 ----------------',list2)
#     # listF = list1 + list2
#     # print('Joined List  ----------------',data)
#     # return (data)
#     return data

# class unitcountList(ListView):
#     # model = Student
#     template_name = 'allunitTest.html'  # Default: <app_label>/<model_name>_list.html
#     context_objsect_name = 'users'  # Default: object_list
#     paginate_by = 100
#     queryset = get_cloud_unitCount_data()
    # query = request.GET.get("q", None)
    # timedOut_list = get_cloud_unitCount_data()

    # context = {
    #         "object_list" : timedOut_list,
    #         "code":query
    #         }
    # template = "allunitTest.html"    
    # return render(request, template, context) 

def NoteiceDataa():
    store = firestore.client()
    # doc_ref = store.collection(u'unitTest').document(id)
    datas = store.collection(u'unitTest')
    # obj = doc_ref.get()
    # object_list=obj.to_dict()
    # print(object_list)
    doc_ref = datas.where(u'field1.reg',u'==','KAS5638')
    data = []
    try:
        docs = doc_ref.get()
        for doc in docs:
            dic1={}
            dic2=doc.to_dict() 
            dic1['id'] = (doc.id)  
            dic1.update(dic2)         
            data.append(dic1)
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
    print("NoticeImage Data",data)
    return data







