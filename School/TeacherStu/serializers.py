from rest_framework import serializers
from . models import *

class stuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'       
        # fields = ('userid', 'name', 'fatherName', 'clas', 'section', 'houseName', 'address', 'mobileNum', 'category')

class videoSerializer(serializers.ModelSerializer):

  class Meta():
    model = Video
    fields = '__all__'

class userSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = User
        fields = '__all__'

class newsSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = News
        fields = '__all__'

class videoPostSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = Video_Post
        fields = '__all__'
  
class commentSerializer(serializers.ModelSerializer):
    post_id = videoPostSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','user_id', 'post_id', 'body','reply', 'createDate', 'updateDate')

class stuTaskSerializer(serializers.ModelSerializer):

  class Meta():
    model = Stu_Task
    fields = '__all__' 

class noteSerializer(serializers.ModelSerializer):

  class Meta():
    model = Teach_Task
    fields = '__all__' 

class feedbackSerializer(serializers.ModelSerializer):

  class Meta():
    model = Feedback
    fields = '__all__' 

class questionSerializer(serializers.ModelSerializer):
    que_tittle = serializers.CharField(max_length=100)
    que_body =serializers.CharField(max_length=500,allow_blank=True, allow_null=True)
    user_id = serializers.CharField(max_length=100)
    clas = serializers.CharField(max_length=100)
    school = serializers.CharField(max_length=100)
    solve_status = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
    class Meta:
        model = FAQ_Question
        fields = '__all__'
        # serializer = questionSerializer(FAQ_Question)
        # serializer.data

class answerSerializer(serializers.ModelSerializer):

    que_id = questionSerializer(read_only=True)
    
    class Meta:
        model = FAQ_Answer
        fields = ('que_id','ans_title', 'ans_solution', 'teacher_id','img_link' ,'img_link2' ,'img_link2' ,'video_link','link', 'created_at', 'updated_at')
        # fields = '__all__'

class MCQ_PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MCQ_Post
        fields = '__all__' 

class MCQ_QueSerializer(serializers.ModelSerializer):

    MCQPost_id = MCQ_PostSerializer(read_only=True)
    class Meta:
        model = MCQ_Question
        fields = ('id','que_title','flag', 'que_Image', 'choice_1', 'choice_2','choice_3' ,'choice_4' ,'correct_answer' ,'created_at', 'updated_at','MCQPost_id')
        # fields = '__all__'

class MCQ_AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MCQ_Answer
        fields = '__all__' 

class MCQ_ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MCQ_Result
        fields = '__all__'  

class VideoFSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = videoF
        fields = '__all__'       

class noticeImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NoticeImage
        fields = '__all__'        