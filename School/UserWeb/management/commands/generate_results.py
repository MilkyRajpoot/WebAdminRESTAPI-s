from django.core.management.base import BaseCommand
from UserWeb.models import *
from django.db.models import Count


class Command(BaseCommand):
    def handle(self, *args, **options):
        unit_count = UnitCount.objects.all().order_by('title')
        unit_test = UnitTest.objects.all().order_by('title')
        questions = StudentMcqQuestions.objects.all().order_by('mcq_post_id')
        student_details = StudentDetails.objects.all()
        student_ids = unit_test.values('reg').distinct()
        subjects = unit_count.values('title', 'subject').distinct()

        for i in student_ids:
            d = {}
            student = student_details.filter(userid=i['reg']).values()
            if student:
                for sub in subjects:
                    correct_ans, wrong_ans = 0, 0
                    unit_test = UnitTest.objects.filter(reg=i['reg'], subject=sub['subject']).values()
                    length = unit_test.values('questions').distinct().count()
                    ques_and_ans = unit_test.values('questions', 'ansText', 'title').distinct()
                    for j in range(length):
                        if questions.filter(que_title=ques_and_ans[j]['questions'],
                                            correct_answer=ques_and_ans[j]['ansText']).exists():
                            correct_ans += 1
                        else:
                            wrong_ans += 1
                        d[i['reg']] = {'subject': sub['subject'], 'correct_ans': correct_ans, 'wrong_ans': wrong_ans,
                                       'quiz_title': ques_and_ans[j]['title'], 'total_marks': 20,
                                       'clas': student[0]['clas'], 'name': student[0]['name'],
                                       'father_name': student[0]['fatherName'], 'mob_no': student[0]['mobileNum'],
                                       'category': student[0]['category'], 'Enable': student[0]['Enable']}

            mcq_post = StudentMcqQuestions.objects.values('mcq_post_id').annotate(Count('mcq_post_id'))
            for key, val in d.items():
                try:
                    if not McqResults.objects.filter(stu_id=key, quiz_title=val['quiz_title'], clas=val['clas'],
                                                     subject=val['subject'], result=val['correct_ans'],
                                                     correct_ans=val['correct_ans'],
                                                     wrong_ans=val['wrong_ans']).exists():

                        total_questions = mcq_post.filter(
                            mcq_post_id=val['quiz_title']).values('mcq_post_id__count')[0]['mcq_post_id__count']

                        f = McqResults(stu_id=key, quiz_title=val['quiz_title'], clas=val['clas'], subject=val['subject'],
                                       result=val['correct_ans'], total_questions=total_questions,
                                       correct_ans=val['correct_ans'], wrong_ans=val['wrong_ans'], name=val['name'],
                                       father_name=val['father_name'], mob_no=val['mob_no'],
                                       category=val['category'], Enable=val['Enable'])
                        print(f)
                        f.save()
                except IndexError:
                    pass
