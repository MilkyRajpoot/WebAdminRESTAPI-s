from django.db import models

# Create your models here.
class Users(models.Model):

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)+" ------- "+str(self.password)

class FeedbackUser(models.Model):

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)+" ------- "+str(self.password)

class AuthDeleteUser(models.Model):

    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)+" ------- "+str(self.password)

class MCQUser(models.Model):

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.username)+" ------- "+str(self.password)

class NotesFirebaseFile_User(models.Model):

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.username)+" ------- "+str(self.password)

class UnitTest(models.Model):
    objects = models.Manager()
    # unique_id = models.CharField(max_length=32, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    clas = models.CharField(max_length=10, null=True, blank=True)
    reg = models.CharField(max_length=20, null=True, blank=True)
    questions = models.TextField(null=True, blank=True)
    ansText = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.title)+" ------- "+str(self.questions)

    def _str_(self):
        template = '{0.title} {0.subject} {0.clas} {0.reg} {0.questions} {0.ansText}'
        return template.format(self)


class UnitCount(models.Model):
    objects = models.Manager()
    reg = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    counts = models.CharField(max_length=10, null=True, blank=True)
    time = models.DateTimeField(blank=True, null=True)

    def _str_(self):
        template = '{0.reg} {0.title} {0.subject} {0.count} {0.time}'
        return template.format(self)


class Feedback(models.Model):
    objects = models.Manager()
    date = models.DateField(blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)

    def _str_(self):
        template = '{0.date} {0.msg} {0.school} {0.user}'
        return template.format(self)


class OptionalUnit(models.Model):
    objects = models.Manager()
    date = models.DateField(blank=True, null=True)
    reg = models.CharField(max_length=20, null=True, blank=True)
    topic = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        template = '{0.date} {0.reg} {0.topic}'
        return template.format(self)


class TimedOut(models.Model):
    objects = models.Manager()
    q_count = models.CharField(max_length=20, blank=True, null=True)
    reg = models.CharField(max_length=20, blank=True, null=True)

    def _str_(self):
        template = '{0.q_count} {0.reg}'
        return template.format(self)

class ResultUser(models.Model):

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.username)+" ------- "+str(self.password)

