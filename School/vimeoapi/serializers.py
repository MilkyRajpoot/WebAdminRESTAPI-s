from rest_framework import serializers
from rest_framework import exceptions, response
from rest_framework.validators import UniqueValidator
from . import models
from rest_framework.response import Response
import random
import string
import json
        
class VideoSer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('retdata')
    def retdata(self,dat):
        dat = dat.data
        # jtopy=json.dumps(dat)
        dat = json.loads(dat)
        return dat

    class Meta:
        fields = ('id','title','data',)
        model = models.Vimeo