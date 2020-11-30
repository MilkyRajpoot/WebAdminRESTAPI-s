from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,ParseError
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from .models import *
from django.shortcuts import render #Default
from django.http import *
from django.shortcuts import get_object_or_404 #get object(error) when object not exist
from rest_framework.views import APIView #API data
from rest_framework.response import Response #Successful 200 response
from rest_framework import status #send back status 
from . import services
from datetime import date as date1
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import json
import pdb
import datetime
import pytz
from django.db.models import Q
from . serializers import *
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class stulist(APIView):

    def get(self, request):
    	enable=Student.objects.filter(Enable="True")
    	stu_list=enable.all()
    	serializer=stuSerializer(stu_list,many=True)
    	return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        mobileNum = data.get('mobileNum')
        # if (Student.objects.filter(mobileNum=mobileNum).exists()):
        if (User.objects.filter(mobileNum=mobileNum).exists()):
            return services.UserLogin(request)
        else:
            password = data.get('password',None)
            paswd = len(str(password))
            print(paswd)
            # print(paswd)
            # import pdb
            # pdb.set_trace()

            if password is None or len(password)==0:
                return services.MesgResponse(mobileNum,mesg="Please Enter Password.",status=204) 
            
            else:
                # return services.MesgResponse(mobileNum,mesg=" Password.",status=204) 
                saveQuerySet = User.objects.create(mobileNum=mobileNum,password=password)
                saveQuerySet.save()
                return services.LoginDataSuccessResponse(mobileNum,status=200) 
        # else:
            # return services.MesgResponse(mobileNum,mesg='Enter Valid Mobile Number...',status=204)

@api_view(['POST',])
def checkMobileNum(request):
	mobileNum = request.data.get('mobileNum',None)
	enable=Student.objects.filter(Enable="True")
	if (enable.filter(mobileNum=mobileNum).exists()):
		if (enable.filter(mobileNum=mobileNum).exists()):
			return services.MesgResponse(mobileNum,mesg='Mobile Number is Valid...',status=status.HTTP_201_CREATED)
		else:
			return services.MesgResponse(mobileNum,mesg='Mobile Number is Invalid...',status=status.HTTP_400_BAD_REQUEST)    
	else:
		return services.MesgResponse(mobileNum,mesg='User is Blocked from School',status=status.HTTP_400_BAD_REQUEST)

class stuTaskList(APIView):

    def get(self, request):
        stuTask_list=Stu_Task.objects.all()
        serializer=stuTaskSerializer(stuTask_list,many=True)
        return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        school_code = data.get('school_code')
        clas = data.get('clas')
        date = data.get('date')
        if (Stu_Task.objects.filter(school_code=school_code).exists()):
        	scode = Stu_Task.objects.filter(school_code=school_code)
        	if (scode.filter(clas=clas).exists()):
        		stu_list=scode.filter(clas=clas).values()
        		if (stu_list.filter(date=date).exists()):
        			dvalue=stu_list.filter(date=date).values()
        			# dvalue.filter(date=date).values()
	        		serializer=stuTaskSerializer(dvalue,many=True)
	        		return Response(serializer.data)
	        	else:
	        		return services.MesgResponse(clas,mesg="Date Not Exist",status=status.HTTP_400_BAD_REQUEST)
        	else:
        		return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
        else:
        	return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 

class notesList(APIView):

    def get(self, request):
        note_list=Teach_Task.objects.all()
        serializer=noteSerializer(note_list,many=True)
        return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        school_code = data.get('school_code')
        clas = data.get('clas')
        if (Teach_Task.objects.filter(school_code=school_code).exists()):
        	scode = Teach_Task.objects.filter(school_code=school_code)
        	if (scode.filter(clas=clas).exists()):
        		stu_list=scode.filter(clas=clas).values()
        		serializer=noteSerializer(stu_list,many=True)
        		return Response(serializer.data)
        	else:
        		return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
        else:
        	return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 

class feedBackList(APIView):

    def get(self, request):
        feed_list=Feedback.objects.all()
        serializer=feedbackSerializer(feed_list,many=True)
        return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        school_code = data.get('school_code')
        userid = data.get('userid')
        if (Feedback.objects.filter(school_code=school_code).exists()):
        	scode = Feedback.objects.filter(school_code=school_code)
        	if (scode.filter(userid=userid).exists()):
        		stu_list=scode.filter(userid=userid).values()
        		serializer=feedbackSerializer(stu_list,many=True)
        		return Response(serializer.data)
        	else:
        		return services.MesgResponse(userid,mesg="User-Id Not Exist",status=status.HTTP_400_BAD_REQUEST)
        else:
        	return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
def forgetPass(request):

	mobileNum = request.data.get('mobileNum')
	password = request.data.get('password')
	if (User.objects.filter(mobileNum=mobileNum).exists()):
		paswd = len(str(password))
		print(paswd)
		if password is None or len(password)==0:
			return services.MesgResponse(mobileNum,mesg="Please Enter Password.",status=status.HTTP_400_BAD_REQUEST) 
		else:
			saveQuerySet = User.objects.filter(mobileNum=mobileNum).update(password=password)
		return services.MesgResponse(mobileNum,mesg="Password Successfully Changed.",status=status.HTTP_201_CREATED)
		

class FileView(APIView):
	parser_classes = (MultiPartParser, FormParser)

	def get(self, request):
		stu_list=Video.objects.all()
		serializer=videoSerializer(stu_list,many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
	 	file_serializer = videoSerializer(data=request.data)
	 	if file_serializer.is_valid():
	 		file_serializer.save()
	 		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
	 	else:
	 		return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsView(APIView):

	def get(self, request):
		news_list=News.objects.all()
		serializer=newsSerializer(news_list,many=True)
		return Response(serializer.data)

	def post(self, request):
		data=self.request.data
		user_code = data.get('user_code')
		date = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
		print(date)
		ucode = user_code[0:3]
		# tcode = user_code[-3:]
		if (Student.objects.filter(userid=user_code).exists()):
			reqName = Student.objects.filter(userid=user_code).values_list('name',flat=True)[0]
			reqDate = News.objects.exclude(expiryDate__lt=date).values('expiryDate')
			# print(reqDate)
			if (reqDate.filter(user_code=reqName).exists()):
				reqCls = Student.objects.filter(userid=user_code).values_list('clas',flat=True)[0]
				stuCls = reqDate.filter(class_code=reqCls)
				stuName = reqDate.filter(user_code=reqName)
				stuSchool = reqDate.filter(school_code=ucode)
				news_list= (stuName.filter(school_code=ucode).values() | stuCls.filter(school_code="ALL").values() | stuSchool.filter(class_code='ALL').values() | News.objects.filter(school_code='ALL',class_code='ALL').values())
				serializer=newsSerializer(news_list,many=True)
				return Response(serializer.data)
			else:
				reqCls = Student.objects.filter(userid=user_code).values_list('clas',flat=True)[0]
				stuUserCode = reqDate.filter(school_code=ucode,class_code=reqCls)
				stuCls = reqDate.filter(class_code=reqCls)
				stuSchool = reqDate.filter(school_code=ucode)
				news_list= (stuUserCode.filter(user_code="ALL").values() | stuCls.filter(school_code="ALL").values() | stuSchool.filter(class_code='ALL').values() | News.objects.filter(school_code='ALL',class_code='ALL').values())
				serializer=newsSerializer(news_list,many=True)
				return Response(serializer.data)
		else:
			return services.MesgResponse(user_code, mesg='User-Code not Exist...!!!', status=status.HTTP_400_BAD_REQUEST)

class VideoPostUploadView(APIView):

	def post(self, request):
		file_serializer = videoPostSerializer(data=self.request.data)
		if file_serializer.is_valid():
			file_serializer.save()
			return Response(file_serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):

	def get(self, request):
		que_list=Comment.objects.all()
		serializer=commentSerializer(que_list,many=True)
		return Response(serializer.data)

	# def get(self, request, slug):
	# 	post = get_object_or_404(Video_Post, slug=slug)
	# 	comments = Comment.objects.filter(post_id=post).order_by('-id').values()
	# 	video = Video_Post.objects.filter(slug__iexact =slug).values() 
	# 	serializer1 = videoPostSerializer(video,many=True)
	# 	serializer = commentSerializer(comments,many=True) 
	# 	Serializer_list = [serializer1.data, serializer.data]
	# 	return Response(Serializer_list)
		# data = [video, comments]
		# return Response(data)

	# def post(self, request, slug):
	# 	try:
	# 		postid = Video_Post.objects.get(slug=slug)
	# 	except:
	# 		return Response(status=status.HTTP_404_NOT_FOUND)
	# 	if request.method == 'POST':
	# 		serializer = commentSerializer(instance=postid,data=request.data)
	# 		print (request.data)
	# 		if serializer.is_valid():
	# 			serializer.save()
	# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
	# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionView(APIView):

	def get(self, request):
		que_list=FAQ_Question.objects.all()
		serializer=questionSerializer(que_list,many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
	 	file_serializer = questionSerializer(data=request.data)
	 	if file_serializer.is_valid():
	 		file_serializer.save()
	 		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
	 	else:
	 		return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerView(APIView):
	
	def get(self, request, id):
		post = get_object_or_404(FAQ_Question, id=id)
		print(post)
		ans_Data = FAQ_Answer.objects.filter(que_id=post).order_by('-id').values()
		que_Data = FAQ_Question.objects.filter(id = id).values() 
		serializer1 = questionSerializer(que_Data,many=True)
		serializer = answerSerializer(ans_Data,many=True) 
		Serializer_list = [serializer1.data, serializer.data]
		return Response(Serializer_list)

class MCQ_PostTopicView(APIView):
	
	def get(self, request):
		MCQ_Data = MCQ_Post.objects.all()
		MCQue_Data = MCQ_Question.objects.all() 
		serializer1 = MCQ_QueSerializer(MCQue_Data,many=True)
		# serializer = MCQ_PostSerializer(MCQ_Data,many=True) 
		Serializer_list = serializer1.data
		return Response(Serializer_list)

	def post(self, request):
		data=self.request.data
		school = data.get('school')
		clas = data.get('clas')
		userid = data.get('userid')
		if (MCQ_Post.objects.filter(school=school).exists()):
			scode = MCQ_Post.objects.filter(school=school)
			if (scode.filter(clas=clas).exists()):
				clas_list=scode.filter(clas=clas).values()
				serializer=MCQ_PostSerializer(clas_list,many=True)
				return Response(serializer.data)
			else:
				return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
		else:
			return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
def MCQ_QueView(request):
	data=request.data
	title = data.get('title')
	school = data.get('school')
	clas = data.get('clas')
	if (MCQ_Question.objects.filter(MCQPost_id__school__contains=school).exists()):
		scode = MCQ_Question.objects.filter(MCQPost_id__school__contains=school)
		if (scode.filter(MCQPost_id__clas=clas).exists()):
			clas_list=scode.filter(MCQPost_id__clas=clas).values()
			if (clas_list.filter(MCQPost_id__title=title).exists()):
				sublist = clas_list.filter(MCQPost_id__title=title).values()
				serializer = list(sublist)
				checktitle=title[-7:-4:]
				print(checktitle)
				if (checktitle == 'DES'):

					questions_list = []
					# options_list = []
					# asnwers_list = []
					flag_list = []
					url_list = []

					if len(serializer)>0:
						for elm in serializer:
							que_title = elm["que_title"]
							# choice_1 = elm["choice_1"]
							# choice_2 = elm["choice_2"]
							# choice_3 = elm["choice_3"]
							# choice_4 = elm["choice_4"]
							# correct_answer = elm["correct_answer"]
							flag = elm["flag"]
							que_Image = elm["que_Image"]
							# print(flag_list,url_list)

							questions_list.append(elm["que_title"])
							# options_list.append([elm["choice_1"],elm['choice_2'],elm['choice_3'],elm['choice_4']])
							# asnwers_list.append(elm["correct_answer"])
							flag_list.append(elm["flag"])
							url_list.append(elm["que_Image"])

					data = {}
					data["questions_list"] = questions_list 
					# data["options_list"] = options_list 
					# data["asnwers_list"] = asnwers_list
					data["flag_list"] = flag_list
					data["url_list"] = url_list
					# print(data)
					return Response(data)				
				elif (checktitle == 'MCQ'):
					questions_list = []
					options_list = []
					asnwers_list = []
					flag_list = []
					url_list = []

					if len(serializer)>0:
						for elm in serializer:
							que_title = elm["que_title"]
							choice_1 = elm["choice_1"]
							choice_2 = elm["choice_2"]
							choice_3 = elm["choice_3"]
							choice_4 = elm["choice_4"]
							correct_answer = elm["correct_answer"]
							flag = elm["flag"]
							que_Image = elm["que_Image"]
							# print(flag_list,url_list)

							questions_list.append(elm["que_title"])
							options_list.append([elm["choice_1"],elm['choice_2'],elm['choice_3'],elm['choice_4']])
							asnwers_list.append(elm["correct_answer"])
							flag_list.append(elm["flag"])
							url_list.append(elm["que_Image"])

					data = {}
					data["questions_list"] = questions_list 
					data["options_list"] = options_list 
					data["asnwers_list"] = asnwers_list
					data["flag_list"] = flag_list
					data["url_list"] = url_list
					# print(data)
					return Response(data)
				else:
					return services.MesgResponse(title,mesg="Title is not Descriptive/MCQ",status=status.HTTP_400_BAD_REQUEST)
			else:
				return services.MesgResponse(title,mesg="Subject Not Exist",status=status.HTTP_400_BAD_REQUEST)
		else:
			return services.MesgResponse(clas,mesg="Class Not Exist",status=status.HTTP_400_BAD_REQUEST)
	else:
		return services.MesgResponse(school,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 


def Apidata(res):
	ansData_list = []
	Question_answer = []
	if (len(res)>0):
		userid = "userid"
		title = "title"
		subject = "subject"

		for elm in res:
			question = elm["question"]
			answer = elm["answer"]

			Question_answer.append({
                "question":question,
                "answer":answer
            })

		ansData_list.append({
			"userid":userid,
			"title":title, 
			"subject":subject,
			"Question_answer":Question_answer
			})

	data = {}
	data = ansData_list
	return data


class MCQ_AnswerData(APIView):

	def get(self, request):
		ans_list=MCQ_Answer.objects.all()
		serializer=MCQ_AnswerSerializer(ans_list,many=True)
		return Response(serializer.data)

	def post(self, request):
		data=request.data
		print(data)
		ans_serializer = MCQ_AnswerSerializer(data=request.data,many=True)
		if ans_serializer.is_valid():
			ans_serializer.save()
			res = ans_serializer.data
			return Response(res, status=status.HTTP_201_CREATED)
		else:
			return Response(ans_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	 	

@api_view(['POST'])
def MCQ_FansView(request):
	data=request.data
	userid = data.get('userid')
	title = data.get('title')
	subject = data.get('subject')
	question = data.get('question')
	answer = data.get('answer')
	clas = data.get('clas')
	que_Image = data.get('que_Image')


	if (MCQ_Post.objects.filter(subject=subject,title=title).exists()):
		if (MCQ_Answer.objects.filter(userid=userid,subject=subject,title=title).exists()):
			que_ans = MCQ_Answer.objects.filter(userid=userid,subject=subject,title=title).values()
			serializer=MCQ_AnswerSerializer(que_ans,many=True)
			res = serializer.data
			result , wrong_ans = 0,0 
			ansData_list = []
			Question_answer = []
			tQues = (len(res))
			if (len(res)>0):
				for elm in res:
					question = elm["question"]
					answer = elm["answer"]
					que_Image = elm["que_Image"]
					if (MCQ_Question.objects.filter(que_title=question,correct_answer=answer,que_Image=que_Image).exists()):
						result += 1
					else:
						result += 0
				wrong_ans = tQues-result
				cor_ans = tQues - wrong_ans

			if (MCQ_Result.objects.filter(userid=userid,title=title).exists()):
				# print(MCQ_Result.objects.filter(userid=userid,title=title).values())
				return services.MesgResponse(userid,mesg="Student already attend the Quiz,Result Exist with this User-Id!!!",status=status.HTTP_400_BAD_REQUEST)
			else :
				return services.MesgResponse(userid,mesg="Student not attend the Quiz,Result Not-Exist with this User-Id!!!",status=status.HTTP_201_CREATED)
		else:
			return JsonResponse({
					"success":False,
					"User-Id, Subject, Title": (userid, subject,title),
					"Data":"Data Not Exist of that User-Id, Title and Subject",
					},status=status.HTTP_400_BAD_REQUEST) 
	else: 
		return JsonResponse({
					"success":False,
					"Data":"Data Not Exist of that Title and Subject",
					},status=status.HTTP_400_BAD_REQUEST)


class MCQ_ResultData(APIView):

	def get(self, request):
		res_list=MCQ_Result.objects.all()
		serializer=MCQ_ResultSerializer(res_list,many=True)
		return Response(serializer.data)

	def post(self, request):
		data=self.request.data
		school = data.get('school')
		clas = data.get('clas')
		userid = data.get('userid')
		date = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

		sec=Student.objects.filter(userid=userid).values_list('section', flat=True)[0]
		section=sec.replace(" ", "")
		sci_Sub = ['Biology','Chemistry','Mathematics','Physics']
		comm_Sub = ['Accountancy','Business Studies']
		hum_Sub = ['Political Science','History']
		commanSubOfCommHum = ['Economics']
		print(section)

		if (MCQ_Answer.objects.filter(userid=userid).exists()):
			utitle=MCQ_Answer.objects.filter(userid=userid).values_list('title', flat=True)
			rtitle=MCQ_Result.objects.filter(userid=userid).values_list('title', flat=True)
			if (MCQ_Post.objects.filter(school=school).exists()):
				scode = MCQ_Post.objects.filter(school=school)
				if (scode.filter(clas=clas,date=date).exists()):
					rcodeExclude = scode.filter(clas=clas,date=date).exclude(title__in=rtitle)
					scodExclude = rcodeExclude.filter(clas=clas,date=date).exclude(title__in=utitle)
					if (clas == 'XII'):
						if (section == 'S'):
							clas_list = scodExclude.filter(clas=clas,date=date).exclude(subject__in=(commanSubOfCommHum+comm_Sub+hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						elif (section == 'C'):
							clas_list = scodExclude.filter(clas=clas,date=date).exclude(subject__in=(sci_Sub+hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						elif (section == 'H'):
							clas_list = scodExclude.filter(clas=clas,date=date).exclude(subject__in=(comm_Sub+sci_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						else:
							return services.MesgResponse(clas,mesg="Class 12th Section must be from C or H or S",status=status.HTTP_201_CREATED)
					elif (clas == 'XI'):
						if (section == 'S'):
							clas_list = scodExclude.filter(clas=clas, date=date).exclude(
								subject__in=(commanSubOfCommHum + comm_Sub + hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list, many=True)
							return Response(serializer.data)
						elif (section == 'C'):
							clas_list = scodExclude.filter(clas=clas, date=date).exclude(
								subject__in=(sci_Sub + hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list, many=True)
							return Response(serializer.data)
						elif (section == 'H'):
							clas_list = scodExclude.filter(clas=clas, date=date).exclude(
								subject__in=(comm_Sub + sci_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list, many=True)
							return Response(serializer.data)
						else:
							return services.MesgResponse(clas, mesg="Class 11th Section must be from C or H or S",
								status=status.HTTP_201_CREATED)
					else:
 						clas_list=scodExclude.filter(clas=clas,date=date).values()
 						serializer=MCQ_PostSerializer(clas_list,many=True)
 						return Response(serializer.data)
				else:
					return services.MesgResponse(clas,mesg="Class or Date Not Exist",status=status.HTTP_400_BAD_REQUEST)
			else:
				return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST)
		elif (MCQ_Result.objects.filter(userid=userid).exists()):
			utitle=MCQ_Result.objects.filter(userid=userid).values_list('title', flat=True)
			if (MCQ_Post.objects.filter(school=school).exists()):
				scode = MCQ_Post.objects.filter(school=school)
				if (scode.filter(clas=clas,date=date).exists()):
					scodExclude = scode.filter(clas=clas,date=date).exclude(title__in=utitle)
					if (clas == 'XII'):
						if (section == 'S'):
							clas_list = scodExclude.filter(clas=clas,date=date).exclude(subject__in=(commanSubOfCommHum+comm_Sub+hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						elif (section == 'C'):
							clas_list = scodExclude.filter(clas=clas,date=date).exclude(subject__in=(sci_Sub+hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						elif (section == 'H'):
							clas_list = scodExclude.filter(clas=clas,date=date).exclude(subject__in=(comm_Sub+sci_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						else:
							return services.MesgResponse(clas,mesg="Class 12th Section must be from C or H or S",status=status.HTTP_201_CREATED)

					else:
 						clas_list=scodExclude.filter(clas=clas,date=date).values()
 						serializer=MCQ_PostSerializer(clas_list,many=True)
 						return Response(serializer.data)
				else:
					return services.MesgResponse(clas,mesg="Class or Date Not Exist",status=status.HTTP_400_BAD_REQUEST)
			else:
				return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST)
		
		else:
			if (MCQ_Post.objects.filter(school=school).exists()):
				scode = MCQ_Post.objects.filter(school=school)
				if (scode.filter(clas=clas,date=date).exists()):
					if (clas == 'XII'):
						if (section == 'S'):
							clas_list = scode.filter(clas=clas,date=date).exclude(subject__in=(commanSubOfCommHum+comm_Sub+hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						elif (section == 'C'):
							clas_list = scode.filter(clas=clas,date=date).exclude(subject__in=(sci_Sub+hum_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						elif (section == 'H'):
							clas_list = scode.filter(clas=clas,date=date).exclude(subject__in=(comm_Sub+sci_Sub)).values()
							serializer = MCQ_PostSerializer(clas_list,many=True)
							return Response(serializer.data)
						else:
							return services.MesgResponse(clas,mesg="Section must be from C or H or S",status=status.HTTP_201_CREATED)
					else:
 						clas_list=scode.filter(clas=clas,date=date).values()
 						serializer=MCQ_PostSerializer(clas_list,many=True)
 						return Response(serializer.data)
				else:
					return services.MesgResponse(clas,mesg="Class or Date Not Exist",status=status.HTTP_400_BAD_REQUEST)
			else:
				return services.MesgResponse(school_code,mesg="School Not Exist",status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST',])
def MCQ_stuResult(request):
    userid = request.data.get('userid',None)
    if (userid is None or len(userid)==0):    
    	return services.MesgResponse(userid,mesg="Please Enter Valid User-Id.",status=204) 
    elif (MCQ_Result.objects.filter(userid=userid).exists()):
    	res_list= MCQ_Result.objects.filter(userid=userid).values()
    	serializer=MCQ_ResultSerializer(res_list,many=True)
    	return Response(serializer.data)
    else:
    	return services.MesgResponse(userid,mesg='User-Id is Invalid...',status=status.HTTP_400_BAD_REQUEST)    


@api_view(['POST',])
def MCQ_stuResultDetails(request):
    userid = request.data.get('userid',None)
    title = request.data.get('title',None)
    mesg = []
    if ((userid is None or len(userid)==0) | (title is None or len(title)==0)):    
    	return services.MesgResponse(userid,mesg="Please Enter User-Id and Title.",status=204) 
    elif (MCQ_Answer.objects.filter(userid=userid,title=title).exists()):
    	ans_list= MCQ_Answer.objects.filter(userid=userid,title=title).values('title','clas','subject','question','que_Image','answer')
    	post_list= MCQ_Question.objects.filter(MCQPost_id__title=title).values('que_title','que_Image','correct_answer')
    	res_list= MCQ_Result.objects.filter(userid=userid,title=title).values('result','total','correct','wrong')
    	mesg1=list(ans_list)
    	mesg2=list(post_list)
    	mesg3=list(res_list)
    	Student_Data_list = []
    	Actual_QueAnswer_List = []
    	Result_list = []
    	if len(mesg1)>0:
    		for elm in mesg1:
    			title = elm["title"]
    			clas = elm["clas"]
    			subject = elm["subject"]
    			question = elm["question"]
    			que_Image = elm["que_Image"]
    			answer = elm["answer"]
    			Student_Data_list.append({
    				"title":title,
    				"clas":clas,
    				"subject":subject,
    				"Question_AnswerData":[{
		                "question":question,
		                "que_Image":que_Image,
		                "answer":answer
		                }]
    				})
    	if len(mesg2)>0:
    		for elm in mesg2:
    			que_title = elm["que_title"]
    			correct_answer = elm["correct_answer"]
    			que_Image = elm["que_Image"]
    			Actual_QueAnswer_List.append({
    				"que_title":que_title,
    				"correct_answer":correct_answer,
    				"que_Image":que_Image
    				})
    	if len(mesg3)>0:
    		for elm in mesg3:
    			result = elm["result"]
    			total = elm["total"]
    			correct = elm["correct"]
    			wrong = elm["wrong"]
    			Result_list.append({
    				"result":result,
    				"total":total,
    				"correct,":correct,
    				"wrong":wrong
    				})
    	data = {}
    	data["Student_Data_list"] = Student_Data_list 
    	data["Actual_QueAnswer_List"] = Actual_QueAnswer_List
    	data["Result_list"] = Result_list
    	return Response(data)
    else:
    	return services.MesgResponse(userid,mesg='User-Id is Invalid...',status=status.HTTP_400_BAD_REQUEST)    
		


class videoPostDetailsData(APIView):
	def get(self, request):
		video_list=Video_Post.objects.all()
		serializer=videoPostSerializer(video_list,many=True)
		return Response(serializer.data)


@api_view(['POST'])
def videoPostDetails(request, slug):
	
	comItems = {}
	comItemList = []
	try:
		postid = Video_Post.objects.get(slug=slug)
	except:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	post_id = request.data.get('post_id', postid)
	user_id = request.data.get('user_id', None)
	body = request.data.get('body', None)
	comment_id = request.data.get('comment_id', None)
	
	if comment_id is not None:
		# get comment_id and update the reply attribute.
		reply = (request.data.get('reply', None))
		# here you can pass update qs to by using comment_id and postId with userId as well to store reply in db.
		
		updtaeReplyQs = Comment.objects.filter(id=comment_id).update(reply=reply)
		return services.MesgResponse(updtaeReplyQs,mesg='...',status=status.HTTP_201_CREATED)


	saveQuerySet = Comment.objects.create(post_id=post_id,user_id =user_id,body = body)
	saveQuerySet.save()
	return getSuccessresponse(saveQuerySet)


def getSuccessresponse(QuerySet):
	return JsonResponse({
			"post_id":str(QuerySet.post_id),
			"user_id": str(QuerySet.user_id),
			"comment_id": str(QuerySet.id),
			"reply": str(QuerySet.reply),
			"comment": QuerySet.body},
			safe=False)	
	

@api_view(['GET',])
def videoPostDetail(request, slug):
	post = get_object_or_404(Video_Post, slug=slug)
	comments = Comment.objects.filter(post_id=post).order_by('-id').values()
	video = Video_Post.objects.filter(slug__iexact =slug).values() 
	serializer1 = videoPostSerializer(video,many=True)
	serializer = commentSerializer(comments,many=True) 
	Serializer_list = [serializer1.data, serializer.data]
	return Response(Serializer_list)

@api_view(['POST',])
def stuListSchool(request):
    school_code = request.data.get('school_code',None)
    # school_code = Student.objects.filter(userid__icontains=school_code)
    if (Student.objects.filter(userid__icontains=school_code).exists()):
    	stu_list= Student.objects.filter(userid__icontains=school_code).values()
    	serializer=stuSerializer(stu_list,many=True)
    	return Response(serializer.data)
    else:
        return services.MesgResponse(school_code,mesg='School Code is Invalid...',status=status.HTTP_400_BAD_REQUEST)    


@api_view(['POST',])
def addNews(request):
	 	file_serializer = newsSerializer(data=request.data)
	 	if file_serializer.is_valid():
	 		file_serializer.save()
	 		return Response(file_serializer.data, status=status.HTTP_201_CREATED)
	 	else:
	 		return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def userData(request):
    stu_list=User.objects.all()
    serializer=userSerializer(stu_list,many=True)
    return Response(serializer.data)


@api_view(['POST',])
def getUserData(request):
	userid = request.data.get('userid',None)
	if (Video.objects.filter(userid=userid).exists()):
		stu_list=Video.objects.filter(userid=userid).values()
		mesg=list(stu_list)
		return Response(mesg)
	else:
		return services.MesgResponse(userid,mesg="Mobile Number Not Exist",status=204)

@api_view(['POST',])
def addShipmentAPIView(request):
    stuItems = {}
    stuItemList = []
    userid = request.data.get('userid', None)
    name = request.data.get('name', None)
    fatherName = request.data.get('fatherName', None)
    clas = request.data.get('clas', None)
    mobileNum = request.data.get('mobileNum ',None)
    category = request.data.get('category',None)
    saveQuerySet = Student.objects.create(userid=userid,name =name,fatherName = fatherName,clas = clas,mobileNum =mobileNum,category =category)
    saveQuerySet.save()
    stuItemList.append({
            "userid":saveQuerySet.userid,
            "name": saveQuerySet.name,
            "fatherName": saveQuerySet.fatherName,
            "clas": saveQuerySet.clas,
            "mobileNum": saveQuerySet.mobileNum,
            "category": saveQuerySet.category,
        })
    stuItems["stuItems"] = stuItemList
    return services.SuccessResponse(stuItems, status=200)	

class VideoFormData(APIView):
	
	def get(self, request):
		videoF_list=videoF.objects.all()
		serializer=VideoFSerializer(videoF_list,many=True)
		return Response(serializer.data)

	def post(self, request):
		data=self.request.data
		school = data.get('school')
		clas = data.get('clas')
		userid = data.get('userid')
		if (videoF.objects.filter(clas=clas,school=school).exists()):
			clas_list = videoF.objects.filter(clas=clas,school=school).values()
			serializer=VideoFSerializer(clas_list,many=True)
			return Response(serializer.data)
		else:
			return services.MesgResponse(clas,mesg="Class/School Not Exist",status=status.HTTP_400_BAD_REQUEST) 

class NoteiceFireFileData(APIView):

    def get(self, request):
        noticeImage_list=NoticeImage.objects.all()
        serializer=noticeImageSerializer(noticeImage_list,many=True)
        return Response(serializer.data)

    def post(self, request):
        data=self.request.data
        school = data.get('school')
        clas = data.get('clas')
        print(school,clas)
        print(len(school))
        if (school is None or len(school)==0) | (clas is None or len(clas)==0):
            return Response({"Error":"Plese Enter Valid School"})
        elif (NoticeImage.objects.filter(clas__contains=clas,school=school).exists()):
        	data_list = NoticeImage.objects.filter(clas__contains=clas,school=school).values()
        	# serializer=noticeImageSerializer(data_list,many=True)
        	serializer = list(data_list)
        	return Response(serializer)
        else:
        	return services.MesgResponse(clas,mesg="Class/School Not Exist",status=status.HTTP_400_BAD_REQUEST) 


