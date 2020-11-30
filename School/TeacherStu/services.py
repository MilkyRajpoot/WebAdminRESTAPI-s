from django.http import JsonResponse, HttpResponse
from .models import Student, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from rest_framework import status 
from . serializers import stuSerializer

# Get Same object Data After Login 
# def LoginDataSuccessResponse(object, status):
#     stu_list=Teachstu.objects.filter(mobileNum=object).values()
#     serializer=techSerializer(stu_list,many=True)
#     return Response(serializer.data)

# Method to print Messgae
def MesgResponse(objects,mesg,status):
    return JsonResponse({
        "results":mesg,
        "status":status
        },safe=False)

# Get Same object Data After Login 
def LoginDataSuccessResponse(object, status):
    enable=Student.objects.filter(Enable="True")
    stu_list=enable.filter(mobileNum=object).values()
    serializer=stuSerializer(stu_list,many=True)
    return Response(serializer.data)

# Method that return data that have same objects 
def SuccessResponse(objects, status):
    # serializer=commentSerializer(objects,many=True)
    # return Response(serializer.data)
    return JsonResponse({
        "results":objects,
        "status":status
        },safe=False)


# Method for User Login
def UserLogin(request):
        mobileNum = request.data.get('mobileNum')
        dbmobile = User.objects.filter(mobileNum=mobileNum)
        if (User.objects.filter(mobileNum=mobileNum).exists()):
            password = request.data.get('password')
            if (dbmobile.filter(password=password).exists()):
                return LoginDataSuccessResponse(mobileNum,status=200)
            else:
                return MesgResponse(mobileNum,mesg="Please Enter Correct Password.",status=200)          
        else:
            return MesgResponse(mobileNum,mesg="User Account Not Exist.",status=204)
