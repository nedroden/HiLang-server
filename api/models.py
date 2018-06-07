from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    distributor = models.PositiveSmallIntegerField(default=0)

    #def __str__(self):
    #     return self.email

    def __repr__(self):
        return {
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "distributer": self.distributor,
        }

class Token(models.Model):
    token = models.CharField(max_length=60);
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    attempt = models.IntegerField(default=0);

    def __str__(self):
        return self.token

    def __repr__(self):
        return {"token": self.token}

class Language(models.Model):
    name = models.CharField(max_length=20)
    flag = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "name": self.name,
            "flag": self.flag,
        }


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.BigIntegerField(default=0)
    image = models.CharField(max_length=200, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    public = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.description,
            "user": self.user,
            "lang": self.language,
            "subs": self.subscribers,
            "img":  self.image,
            "pub":  self.public,
        }


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.user, self.course)

    def __repr__(self):
        return {
            "user": self.user,
            "course": self.course,
        }


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.user, self.course)

    def __repr__(self):
        return {
            "user": self.user,
            "course": self.course,
        }


class ExerciseType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.description,
        }


class Exercise(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)

    def __str__(self):
        return '{} in {}'.format(self.name, self.course)

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
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __repr__(self):
        return {
            "native": self.native,
            "translation": self.translation,
            "exercise": self.exercise,
        }


class SentenceStructureQuestion(models.Model):
    native = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    correctOrder = models.CharField(max_length=20)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    description = models.TextField(null=True)

    def __repr__(self):
        return {
            "native": self.native,
            "translation": self.translation,
            "correctOrder": self.correctOrder,
            "exercise": self.exercise,
            "desc": self.description,
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
