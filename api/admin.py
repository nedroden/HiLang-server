from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Language)
admin.site.register(Course)
admin.site.register(LessonType)
admin.site.register(Lesson)
admin.site.register(WordListQuestion)
admin.site.register(SentenceStructureQuestion)
admin.site.register(SentenceStructureOption)
