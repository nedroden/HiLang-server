from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    distributor = models.PositiveSmallIntegerField(default=0)
    def __repr__(self):
        return {
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "distributer": self.distributor,
        }

class Language(models.Model):
    name = models.CharField(max_length=20)
    def __repr__(self):
        return {
            "name": self.name,
        }

class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.description,
            "user": self.user,
            "lang": self.language,
        }

class LessonType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.description,
        }

class Lesson(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.ForeignKey(LessonType, on_delete=models.CASCADE)
    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.description,
            "course": self.course,
            "type": self.type,
        }

class WordListQuestion(models.Model):
    native = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    def __repr__(self):
        return {
            "native": self.native,
            "translation": self.translation,
            "exercise": self.lesson,
        }

class SentenceStructureQuestion(models.Model):
    native = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    correctOrder = models.CharField(max_length=20)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    def __repr__(self):
        return {
            "native": self.native,
            "translation": self.translation,
            "correctOrder": self.correctOrder,
            "exercise": self.lesson,
        }

class SentenceStructureOption(models.Model):
    value = models.CharField(max_length=100)
    tag = models.IntegerField()
    question = models.ForeignKey(SentenceStructureQuestion, on_delete=models.CASCADE)
    def __repr__(self):
        return {
            "value": self.value,
            "tag": self.tag,
            "question": self.question,
        }
