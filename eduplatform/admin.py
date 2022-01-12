from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Subjects)
admin.site.register(Levels)
admin.site.register(QuestionTypes)
admin.site.register(Question)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(MultipleChoiceResponses)
admin.site.register(NumericResponseQuestion)