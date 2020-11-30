from django.db import models
from django.template.defaultfilters import slugify
from simple_history.models import HistoricalRecords

# Create your models here.

class Student(models.Model):
    CATEGORY_CHOICES = (
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    CLASS_CHOICES = (
        ('PREP','PREP'),
        ('LKG','LKG'), 
        ('UKG','UKG'),
        ('I','I'), 
        ('II','II'),
        ('III','III'),
        ('IV','IV'), 
        ('V','V'), 
        ('VI','VI'), 
        ('VII','VII'), 
        ('VIII','VIII'), 
        ('IX','IX'), 
        ('X','X'), 
        ('XI','XI'), 
        ('XII','XII')
    )

    userid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    fatherName = models.CharField(max_length=255,null=True,blank=True)
    clas = models.CharField(max_length=30, choices=CLASS_CHOICES,null=True,blank=True)
    section = models.CharField(max_length=255,null=True,blank=True)
    houseName = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    mobileNum = models.IntegerField(null=True, blank=False)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    Enable = models.BooleanField(default=True)
    history = HistoricalRecords()
    # regmobNum = models.CharField(max_length=20,null=True,blank=True)
    # password = models.CharField(max_length=255,null=True,blank=True)
    # school_code = models.CharField(max_length=15,choices=SCHOOL_CHOICES)
    # school_code = models.ForeignKey(SchoolDB, on_delete=models.CASCADE)

    def __str__(self):
        # return self.userid
        return str(self.name)

class User(models.Model):
    # userId = models.IntegerField(null=True)
    # mobileNum = models.CharField(primary_key=True,max_length=20)
    mobileNum = models.CharField(max_length=20,null=True,blank=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.mobileNum)


class Video(models.Model):

    userid = models.CharField(max_length=100)
    # userid = models.ForeignKey(Student,on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    # video_link= models.FileField(upload_to='videos/', null=True, verbose_name="Video Link", max_length=1000)
    video_link = models.CharField(verbose_name="Video Link", max_length=1000)
    description = models.CharField(max_length=500)
    thumbnail_link = models.URLField(verbose_name="Image Link", max_length=1000)
    # models.FileField(upload_to='images/', null=True, verbose_name="Image Link", max_length=1000)
    played_time = models.TimeField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.userid + " : " + str(self.name)

class News(models.Model):
    CLASS_CHOICES = (
        ('ALL','ALL'),
        ('PREP','PREP'),
        ('LKG','LKG'), 
        ('UKG','UKG'),
        ('I','I'), 
        ('II','II'),
        ('III','III'),
        ('IV','IV'), 
        ('V','V'), 
        ('VI','VI'), 
        ('VII','VII'), 
        ('VIII','VIII'), 
        ('IX','IX'), 
        ('X','X'), 
        ('XI','XI'), 
        ('XII','XII')
    )
    SCHOOL_CHOICES = (
        ('ALL','ALL'),
        ('KAS','KAS'),
        ('DEO','DEO'), 
        ('AND','AND'),
        ('GKP','GKP')
    )
    # USER_CHOICES = (
    #     ('ALL','ALL'),
    #     ('CLASS','CLASS'),
    #     ('STUDENT','STUDENT') 
    # )

    school_code = models.CharField(max_length=3, choices=SCHOOL_CHOICES)
    user_code = models.CharField(max_length=100,null=True,blank=True)
    class_code = models.CharField(max_length=30, choices=CLASS_CHOICES,null=True,blank=True)
    news = models.TextField(max_length=2000,null=True,blank=True)
    expiryDate = models.DateField(null=True,blank=True)
    addDate = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    link = models.TextField(max_length=1000,null=True,blank=True)

    class Meta:
        ordering = ('addDate',)

    def __str__(self):
        return str(self.school_code) + " : " + str(self.user_code) + " : " + str(self.addDate) + " : " + str(self.expiryDate)

class Video_Post(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    video_link = models.CharField(verbose_name="Video Link", max_length=1000,null=True,blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('title',)
        # db_table=u'Video_Post'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

class Comment(models.Model):

    user_id = models.CharField(max_length=255)
    post_id = models.ForeignKey(Video_Post,related_name='Video_Post',on_delete=models.CASCADE)
    reply = models.CharField(max_length=255, null=True,blank=True)
    body = models.TextField(max_length=500,null=True,blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} ".format(str(self.user_id),str(self.post_id.title))

class Stu_Task(models.Model):
    CLASS_CHOICES = (
        ('PREP','PREP'),
        ('LKG','LKG'), 
        ('UKG','UKG'),
        ('I','I'), 
        ('II','II'),
        ('III','III'),
        ('IV','IV'), 
        ('V','V'), 
        ('VI','VI'), 
        ('VII','VII'), 
        ('VIII','VIII'), 
        ('IX','IX'), 
        ('X','X'), 
        ('XI','XI'), 
        ('XII','XII')
    )
    SUB_CHOICES = (
        ('English','English'),
        ('Hindi',   'Hindi'),
        ('Mathematics', 'Mathematics'),
        ('Rhymes',  'Rhymes'),
        ('English Literature Book1 ',   'English Literature Book1 '),
        ('English Literature Book2',    'English Literature Book2'),
        ('English Grammar', 'English Grammar'),
        ('Hindi Literature',    'Hindi Literature'),
        ('Hindi Grammar',   'Hindi Grammar'),
        ('Science',     'Science'),
        ('Computer',    'Computer' ),
        ('Social Studies',  'Social Studies'),
        ('History',     'History'),
        ('Geography',   'Geography'),
        ('Political Science',   'Political Science'),
        ('Economics',   'Economics'),
        ('Physical Education',  'Physical Education'),
        ('Computer Science',    'Computer Science'),
        ('Physics', 'Physics'),
        ('Chemistry',   'Chemistry' ),
        ('Biology', 'Biology'),
        ('Accountancy', 'Accountancy'),
        ('Business Studies',    'Business Studies'),
        ('Political Science',   'Political Science'),
        ('Psychology', 'Psychology')    
    )
    
    school_code = models.CharField(max_length=3)
    clas = models.CharField(max_length=30, choices=CLASS_CHOICES)
    subject = models.CharField(max_length=255, choices=SUB_CHOICES)
    date = models.DateField() 
    video = models.CharField(max_length=255)
    textbook = models.CharField(max_length=255)
    Notes = models.TextField(max_length=500,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return (str(self.Notes))

class Teach_Task(models.Model):
    CLASS_CHOICES = (
        ('PREP','PREP'),
        ('LKG','LKG'), 
        ('UKG','UKG'),
        ('I','I'), 
        ('II','II'),
        ('III','III'),
        ('IV','IV'), 
        ('V','V'), 
        ('VI','VI'), 
        ('VII','VII'), 
        ('VIII','VIII'), 
        ('IX','IX'), 
        ('X','X'), 
        ('XI','XI'), 
        ('XII','XII')
    )
    
    school_code = models.CharField(max_length=3)
    clas = models.CharField(max_length=30, choices=CLASS_CHOICES)
    Notes = models.TextField(max_length=500,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return (str(self.school_code))

class Feedback(models.Model):

    school_code = models.CharField(max_length=3)
    userid = models.CharField(max_length=255)
    feedback = models.TextField(max_length=500,null=True,blank=True)
    reply = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.school_code) + " : " + str(self.userid)

class FAQ_Question(models.Model):

    que_tittle = models.CharField(max_length=100)
    que_body =models.TextField(max_length=500,null=True,blank=True)
    user_id = models.CharField(max_length=100)
    clas = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    solve_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.que_tittle)

class FAQ_Answer(models.Model):

    que_id = models.ForeignKey(FAQ_Question,related_name='Question_Answer',on_delete=models.CASCADE)
    ans_title = models.CharField(max_length=100)
    ans_solution = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=100)
    img_link = models.URLField(verbose_name="Image Link1", max_length=1000,null=True,blank=True)
    img_link2 = models.URLField(verbose_name="Image Link2", max_length=1000,null=True,blank=True)
    img_link3 = models.URLField(verbose_name="Image Link3", max_length=1000,null=True,blank=True)
    video_link = models.URLField(verbose_name="Video Link", max_length=1000,null=True,blank=True)
    link = models.URLField(verbose_name="Link", max_length=1000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.ans_title)

class MCQ_Post(models.Model):

    # slug = models.SlugField(unique=True)
    CLASS_CHOICES = (
        ('PREP','PREP'),
        ('LKG','LKG'), 
        ('UKG','UKG'),
        ('I','I'), 
        ('II','II'),
        ('III','III'),
        ('IV','IV'), 
        ('V','V'), 
        ('VI','VI'), 
        ('VII','VII'), 
        ('VIII','VIII'), 
        ('IX','IX'), 
        ('X','X'), 
        ('XI','XI'), 
        ('XII','XII')
    )
    SUB_CHOICES = (
        ('English','English'),
        ('Hindi',   'Hindi'),
        ('Mathematics', 'Mathematics'),
        ('Rhymes',  'Rhymes'),
        ('English Literature Book1',   'English Literature Book1'),
        ('English Literature Book2',    'English Literature Book2'),
        ('English Grammar', 'English Grammar'),
        ('Hindi Literature',    'Hindi Literature'),
        ('Hindi Grammar',   'Hindi Grammar'),
        ('Science',     'Science'),
        ('Computer',    'Computer' ),
        ('Social Studies',  'Social Studies'),
        ('History',     'History'),
        ('Geography',   'Geography'),
        ('Political Science',   'Political Science'),
        ('Economics',   'Economics'),
        ('Physical Education',  'Physical Education'),
        ('Computer Science',    'Computer Science'),
        ('Physics', 'Physics'),
        ('Chemistry',   'Chemistry' ),
        ('Biology', 'Biology'),
        ('Accountancy', 'Accountancy'),
        ('Business Studies',    'Business Studies'),
        ('Political Science',   'Political Science'),
        ('Psychology', 'Psychology')    
    )
    
    title = models.CharField(max_length=255,primary_key = True)
    school = models.CharField(max_length=100)
    clas = models.CharField(max_length=30, choices=CLASS_CHOICES)
    subject = models.CharField(max_length=255, choices=SUB_CHOICES)
    description = models.TextField(max_length=500,null=True,blank=True)
    date = models.DateField()
    time = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

class MCQ_Question(models.Model):

    MCQPost_id = models.ForeignKey(MCQ_Post,related_name='Quiz_Topic', on_delete=models.CASCADE)
    que_title = models.TextField(max_length=500)
    flag = models.BooleanField(default=False)
    que_Image = models.ImageField(upload_to='images/',max_length=1000,default="images/Blank")
    choice_1 = models.CharField(max_length=255)
    choice_2 = models.CharField(max_length=255)
    choice_3 = models.CharField(max_length=255)
    choice_4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.que_title)

class MCQ_Answer(models.Model):

    userid = models.CharField(max_length=255)
    clas = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    question = models.TextField(max_length=500)
    que_Image = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userid + "-----: Title : " + str(self.title) + "-----: Question : " + str(self.question) + "-----: Answer : " + str(self.answer)

class MCQ_Result(models.Model): 

    userid = models.CharField(max_length=255)
    clas = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    result = models.IntegerField()
    total = models.IntegerField()
    correct = models.IntegerField()
    wrong = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userid + " : " + str(self.result)

class NoteiceFire(models.Model):
    
    school = models.CharField(max_length=100)
    clas = models.CharField(max_length=30)
    imageLink = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

class videoF(models.Model):
    
    clas = models.CharField(max_length=100)
    school = models.CharField(max_length=3)
    flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.clas + " : " + str(self.flag) + " : " + str(self.school)

class NoticeImage(models.Model):

    school = models.CharField(max_length=3)
    clas = models.CharField(max_length=255,null=True,blank=True)
    que_Image = models.ImageField(upload_to='images/NoticeImage/',max_length=1000,default="images/Blank")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.clas)