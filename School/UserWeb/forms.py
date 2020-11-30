from django import forms  
from . models import *
from django.core.exceptions import ValidationError
from TeacherStu.models import *

class StuForm(forms.ModelForm):  

    # Enable = forms.BooleanField(widget=forms.CheckboxInput, default=False)

    class Meta:
        model = Student
        fields = '__all__'

        labels = {
            'userid': ('User-Id'),
            'name':('Name'),
            'fatherName':("Father Name"),
            'clas':('Choose Class'),
            'section':('Section'),
            'houseName':('HouseName'),
            'address':('Address'),
            'mobileNum':('Mobile Number'),
            'category':("Choose Category"),
        }

        widgets = {
            'userid': forms.TextInput(attrs={'placeholder': 'Enter User-Id','class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Name'}),
            'fatherName': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Father Name'}),
            'clas': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'section': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Section'}),
            'houseName': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter House Name'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Home Address'}),
            'mobileNum': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Mobile Number'}),
            'category': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
        }

class StuTaskForm(forms.ModelForm):  

    class Meta:
        model = Stu_Task
        fields = '__all__'

        labels = {
            'school_code': ('School-Code'),
            'clas':('Class'),
            'subject':("Subject"),
            'date':('Choose Date'),
            'video':('Video'),
            'textbook':('TextBook'),
            'Notes':('Notes'),
        }

        widgets = {
            'school_code': forms.TextInput(attrs={'placeholder': 'Enter School-Code','class':'form-control'}),
            'clas': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'subject': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'video': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Video Description'}),
            'textbook': forms.TextInput(attrs={'class':'form-control','placeholder': 'TextBook'}),
            'Notes': forms.Textarea(attrs={'cols':10,'rows':5,'placeholder': 'Note','class':'form-control'}),
        }

class TeachForm(forms.ModelForm):  

    class Meta:
        model = Teach_Task
        fields = '__all__'

        labels = {
            'school_code': ('School-Code'),
            'clas':('Class'),
            'Notes':('Notes'),
        }

        widgets = {
            'school_code': forms.TextInput(attrs={'placeholder': 'Enter School-Code','class':'form-control'}),
            'clas': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'Notes': forms.Textarea(attrs={'cols':10,'rows':5,'placeholder': 'Note','class':'form-control'}),
        } 

class FeedbackForm(forms.ModelForm):  

    class Meta:
        model = Feedback
        fields = '__all__'

        labels = {
            'school_code': ('School-Code'),
            'userid':('User-Id'),
            'feedback':('Feedback'),
            'reply':('Reply'),
        }

        widgets = {
            'school_code': forms.TextInput(attrs={'placeholder': 'Enter School-Code','class':'form-control'}),
            'userid': forms.TextInput(attrs={'placeholder': 'Enter User-Id','class':'form-control'}),
            'feedback': forms.Textarea(attrs={'cols':10,'rows':5,'placeholder': 'Enter Your Feedback','class':'form-control'}),
            'reply': forms.TextInput(attrs={'placeholder': 'Reply','class':'form-control'}),
        }


class UserForm(forms.ModelForm):  

    class Meta:
        model = User
        fields = '__all__'

        labels = {
            'mobileNum': ('Mobile Number'),
            'password':('Password'),
        }
        
        attrs = {
        "type": "password"
    }        

        widgets = {
            'mobileNum': forms.TextInput(attrs={'placeholder': 'Enter Mobile Number','class':'form-control'}),
            'password': forms.PasswordInput(attrs={"type": "password", 'class':'form-control'}),
            #'password': forms.PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
        }

class UsersLoginForm(forms.ModelForm):  

    class Meta:
        model = Users
        fields = ['name','password']

        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input-text with-border', 'placeholder': 'Enter Password'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter User Name'}),
        }
        labels = {
            'name': ('User Name'),
            'password':('Password'),
            }

class FeedUsersLoginForm(forms.ModelForm):  

    class Meta:
        model = FeedbackUser
        fields = ['name','password']

        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input-text with-border', 'placeholder': 'Enter Password'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter User Name'}),
        }
        labels = {
            'name': ('User Name'),
            'password':('Password'),
            }

class MCQCourseForm(forms.ModelForm):
    # title = forms.TextInput()
    # school = forms.TextInput()
    # clas = forms.Select()
    # subject = forms.Select()
    # description = forms.Textarea() 
    # date = forms.DateInput()
    # time = forms.NumberInput()

    class Meta:
        model = MCQ_Post
        fields = ['title','school','clas','subject','description','date','time']

        labels = {
            'title': ('Enter Quiz Title'),
            'school':('School-Code'),
            'clas':('Choose Class for Quiz'),
            'subject':('Choose Subject of Quiz'),
            'description':('Enter Description about Quiz'),
            'date':('Select Date of Quiz'),
            'time':('Choose Quiz Time'),
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Quiz Title','class':'form-control'}),
            'school': forms.TextInput(attrs={'placeholder': 'Enter School-Code','class':'form-control'}),
            'clas': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'subject': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'description': forms.Textarea(attrs={'cols':10,'rows':5,'placeholder': 'Enter Description about Quiz','class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'time': forms.NumberInput(attrs={'min': '1','max':'60','class': 'form-control', 'id': 'blah'}),        
            }

    def clean_title(self):
        title = self.cleaned_data['title']
        if " " in title or '@' in title or ',' in title or '|' in title or '%' in title or '$' in title or '^' in title or '&' in title or '()' in title or '#' in title:
            raise forms.ValidationError('Title should not contain any Space( ) an Special Characters.')
        return title  



class MCQ_QueForm(forms.ModelForm):  

    MCQPost_id = forms.ModelChoiceField(queryset=MCQ_Post.objects.all(),required=False,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = MCQ_Question
        fields = '__all__'

        labels = {
            'MCQPost_id': ('Choose Quiz Title'),
            'que_title':('Question'),
            'flag':('flag'),
            'que_Image':('Upload Question Image'),
            'choice_1':('Option Choice 1'),
            'choice_2':('Option Choice 2'),
            'choice_3':('Option Choice 3'),
            'choice_4':('Option Choice 4'),
            'correct_answer':('Correct Answer'),
        }
        # fields = ('id','que_title', 'choice_1', 'choice_2','choice_3' ,'choice_4' ,'correct_answer' ,'created_at', 'updated_at','MCQPost_id')
        widgets = {
            'que_title': forms.TextInput(attrs={'placeholder': 'Enter Question','class':'form-control'}),
            'choice_1': forms.TextInput(attrs={'placeholder': 'Enter First Choice ','class':'form-control'}),
            'choice_2': forms.TextInput(attrs={'placeholder': 'Enter  Second Choice','class':'form-control'}),
            'choice_3': forms.TextInput(attrs={'placeholder': 'Enter Third Choice','class':'form-control'}),
            'choice_4': forms.TextInput(attrs={'placeholder': 'Enter Fourth Choice','class':'form-control'}),
            'correct_answer': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Correct Answer'}),
           }

    # def clean_que_Image(self):
    #     que_Image = self.cleaned_data.get('que_Image', False)
    #     if que_Image:
    #         if que_Image.size > 4*1024*1024:
    #             raise ValidationError("Image size too large ( > 4mb )")
    #         return que_Image
    #     else:
    #         raise ValidationError("Couldn't read uploaded que_Image")


    def clean_correct_answer(self):
        correct_answer = self.cleaned_data['correct_answer']
        if correct_answer==None or len(correct_answer) == 0:
            raise ValidationError("Answer cannot be empty")
        return correct_answer

class MCQ_AttStuList(forms.ModelForm):  

    class Meta:
        model = MCQ_Result
        fields = '__all__'

        labels = {
            'userid': ('Student User-Id'),
            'title':('Title'),
        }
        # fields = ('id','que_title', 'choice_1', 'choice_2','choice_3' ,'choice_4' ,'correct_answer' ,'created_at', 'updated_at','MCQPost_id')
        widgets = {
            'userid': forms.TextInput(attrs={'placeholder': 'Student User-Id','class':'form-control'}),
            'title': forms.TextInput(attrs={'placeholder': 'Test Title','class':'form-control'}),
           }

class NewsDataForm(forms.ModelForm):  
    # user_code = forms.ModelChoiceField(queryset=Student.objects.filter(clas='V'),required=False,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = News
        fields = '__all__'

        labels = {
            'school_code': ('School-Code'),
            'user_code':('User-Id'),
            'class_code':('Enter the Class'),
            'news':('News Data'),
            'expiryDate':('Expiry Date of News'),
            'link':('Any Link'),
        }
        widgets = {
            'school_code': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'user_code': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'class_code': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            'news': forms.Textarea(attrs={'cols':10,'rows':5,'placeholder': 'Enter anout News','class':'form-control'}),
            'expiryDate': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'link': forms.Textarea(attrs={'cols':10,'rows':5, 'placeholder': 'Any Link','class':'form-control'}),
           }

class AuthDeleteLoginForm(forms.ModelForm):  

    class Meta:
        model = AuthDeleteUser
        fields = ['name','password']

        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input-text with-border', 'placeholder': 'Enter Password'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter User Name'}),
        }
        labels = {
            'name': ('User Name'),
            'password':('Password'),
            }

class ResultuserLoginForm(forms.ModelForm):  

    class Meta:
        model = ResultUser
        fields = ['username','password']

        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input-text with-border', 'placeholder': 'Enter Password'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter User-Name'}),
        }
        labels = {
            'username': ('User-Name'),
            'password':('Password'),
            }

class MCQLoginForm(forms.ModelForm):  

    class Meta:
        model = MCQUser
        fields = ['username','password']

        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input-text with-border', 'placeholder': 'Enter Password'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter User-Name'}),
        }
        labels = {
            'username': ('User-Name'),
            'password':('Password'),
            }

class MCQ_ResultFind(forms.ModelForm):  

    class Meta:
        model = MCQ_Post
        fields = ['clas']

        # labels = {
        #     'userid': ('Student User-Id'),
        #     'title':('Title'),
        # }
        # fields = ('id','que_title', 'choice_1', 'choice_2','choice_3' ,'choice_4' ,'correct_answer' ,'created_at', 'updated_at','MCQPost_id')
        widgets = {
            'clas': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
            # 'subject': forms.Select(attrs={'id':'choicewa','class':'form-control'}),
           }

class NotesFormFirestore(forms.Form):

    school = forms.CharField()
    clas = forms.CharField()
    subject = forms.CharField()
    title = forms.CharField()
    pdf_upload = forms.CharField()

class NotesFireLoginForm(forms.ModelForm):  

    class Meta:
        model = NotesFirebaseFile_User
        fields = ['username','password']

        password = forms.CharField(widget=forms.PasswordInput)
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'input-text with-border', 'placeholder': 'Enter Password'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter User-Name'}),
        }
        labels = {
            'username': ('User-Name'),
            'password':('Password'),
            }

class NoteiceFormFirestore(forms.Form):

    school = forms.CharField()
    clas = forms.CharField()
    image_upload = forms.CharField()

class VideoForm(forms.ModelForm):  

    class Meta:
        model = videoF
        fields = '__all__'

        labels = {
            'clas': ('Class'),
            'flag':('Enable'),
            }

class NoticeImageForm(forms.ModelForm):  

    class Meta:
        model = NoticeImage
        fields = '__all__'

    


