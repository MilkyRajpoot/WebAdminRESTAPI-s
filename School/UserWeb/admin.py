from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Users)
admin.site.register(FeedbackUser)
admin.site.register(AuthDeleteUser)
admin.site.register(MCQUser)
admin.site.register(UnitTest)
admin.site.register(UnitCount)
admin.site.register(Feedback)
admin.site.register(OptionalUnit)
admin.site.register(TimedOut)
admin.site.register(ResultUser)
admin.site.register(NotesFirebaseFile_User)