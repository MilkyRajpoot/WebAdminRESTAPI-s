import json
from vimeoapi import models
import requests

def job():
    stat = models.VimeoStatus.objects.all()
    p = 1
    while True:
        url = 'https://api.vimeo.com/users/112186186/videos/?per_page=100&page='+str(p)
        payload = {
        }
        headers = {
            "Authorization": f"Bearer 70b8a941d1f7a9950d7c09d3abf322ba",
            'Content-Type':	'Application/json',
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

job()
