from django.shortcuts import render
from django.http import HttpResponse
from. import models
from django.db.models import Q
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import serializers
from datetime import datetime
from rest_framework import viewsets
from . import models

# Create your views here.
def myjob():
    stat = models.VimeoStatus.objects.all()
    p = 1
    while True:
        url = 'https://api.vimeo.com/users/112186186/videos/?per_page=100&page='+str(p)
        payload = {
        }
        headers = {
            "Authorization": f"Bearer 70b8a941d1f7a9950d7c09d3abf322ba",
            'Content-Type': 'Application/json',
            'Accept': 'application/vnd.vimeo.*+json;version=3.4',
            }
        response = requests.request("GET", url, headers=headers, data = payload)

        data = json.loads(response.text)
        if p == 1:
            models.Vimeo.objects.all().delete()
            if len(stat) == 0:
                stat = models.VimeoStatus()
                stat.status = True
                stat.count = data['total']
                stat.save()
            else:
                if int(stat[0].count) == int(data['total']):
                    stat[0].status = False
                    stat[0].save()
                else:
                    stat[0].status = True
                    stat[0].count = data['total']
        print(data['paging']['next'])
        for i in data['data']:
            dt = models.Vimeo()
            name = i['name']
            dt.title = name
            dt.college = name[:4]
            dt.sub = name[5:]
            dt.data = json.dumps(i)
            dt.save()
        if data['paging']['next'] is None:
            break
        else:
            p = p + 1
    return True
def job(request):
    stat = models.VimeoStatus.objects.all()
    p = 1
    while True:
        url = 'https://api.vimeo.com/users/112186186/videos/?per_page=100&page='+str(p)
        payload = {
        }
        headers = {
            "Authorization": f"Bearer 70b8a941d1f7a9950d7c09d3abf322ba",
            'Content-Type': 'Application/json',
            'Accept': 'application/vnd.vimeo.*+json;version=3.4',
            }
        response = requests.request("GET", url, headers=headers, data = payload)

        data = json.loads(response.text)
        if p == 1:
            models.Vimeo.objects.all().delete()
            if len(stat) == 0:
                stat = models.VimeoStatus()
                stat.status = True
                stat.count = data['total']
                stat.save()
            else:
                if int(stat[0].count) == int(data['total']):
                    stat[0].status = False
                    stat[0].save()
                else:
                    stat[0].status = True
                    stat[0].count = data['total']
        print(data['paging']['next'])
        if data is None:
            return HttpResponse(True)
        for i in data['data']:
            dt = models.Vimeo()
            name = i['name']
            dt.title = name
            dt.college = name[:4]
            dt.sub = name[5:]
            dt.data = json.dumps(i)
            dt.save()
        if data['paging']['next'] is None:
            break
        else:
            p = p + 1
    return HttpResponse(True)


class Videos(viewsets.ModelViewSet):
    queryset = models.Vimeo.objects.all()
    serializer_class = serializers.VideoSer
    http_method_names = ['get', 'list']
    def list(self, request):
        queryset = models.Vimeo.objects.all()
        school = request.GET.get('school', None)
        sclass = request.GET.get('class', None)
        lesson = request.GET.get('lesson', None)
        subject = request.GET.get('subject', None)
        part = request.GET.get('part', None)
        if school:
            queryset = queryset.filter(Q(college__contains=school))
        if sclass:
            if len(sclass) == 2:
                sclass = str(sclass) + 'L'

            queryset = queryset.filter(Q(sub__contains=sclass))
        if lesson:
            queryset = queryset.filter(Q(sub__contains=lesson))
        if subject:
            queryset = queryset.filter(Q(sub__contains=subject))
        if part:
             queryset = queryset.filter(Q(sub__contains=part))
        serializer = serializers.VideoSer(queryset, many=True)
        return Response(data=serializer.data)

class Status(APIView):
    def get(self, request):
        data = models.VimeoStatus.objects.all()[0]
        mycount = request.GET.get('count', None)
        update_required = False
        if data.status == True:
            update_required = True
        elif mycount:
            if int(mycount) != int(data.count):
                update_required = True
        return Response({'update_required':update_required})