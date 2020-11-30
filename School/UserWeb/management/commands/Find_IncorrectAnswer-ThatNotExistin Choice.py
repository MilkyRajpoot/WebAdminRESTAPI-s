from TeacherStu.models import MCQ_Question
from django.db.models import Q
y=0
for x in range(17662):
	queD = MCQ_Question.objects.all().values('MCQPost_id','que_title','correct_answer')[x]
	title=(queD['MCQPost_id'])
	que = queD['que_title']
	cans = queD['correct_answer']
	ques = MCQ_Question.objects.filter(MCQPost_id=title,que_title=que)
	if ques.filter(Q(choice_1=cans)|Q(choice_2=cans)|Q(choice_3=cans)|Q(choice_4=cans)).exists():
		y=y+1
		pass
	else:
		print('Main Title',title,'Question',que)

y=1
for x in ques:
	ca = x.correct_answer
	if ques.filter(Q(choice_1=ca)|Q(choice_2=ca)|Q(choice_3=ca)|Q(choice_4=ca)).exists():
	  y=y+1
	  pass
	else:
	  print('Main Title',x.MCQPost_id,'Question',x.que_title)

