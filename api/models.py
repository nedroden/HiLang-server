from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    email = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=25)
    password = models.CharField(max_length=60)
    distributor = models.PositiveSmallIntegerField(default=0)
    salt = models.CharField(max_length=50, null=True)
    attempt = models.IntegerField(default=0)

    def __str__(self):
        return self.email

    def __repr__(self):
        return {
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "distributer": self.distributor,
            "salt": self.salt,
            "attempt": self.attempt
        }


class Token(models.Model):
    token = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " : " + self.token

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
    native_lang = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, related_name='native')
    trans_lang = models.ForeignKey(Language, null=True, on_delete=models.CASCADE, related_name='translation')
    public = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.description,
            "user": self.user,
            "lang": self.native_lang,
            "subs": self.subscribers,
            "img": self.image,
            "pub": self.public,
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


# All types of exercises: Flashcards etc.
class LessonType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return {
            "name": self.name,
            "desc": self.description,
        }


class Lesson(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True)
    grammar = models.TextField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def delete(self, user_id):
        user = User.objects.get(pk=user_id)

        if self.course.user == user.id:
            super().delete()

    def __str__(self):
        return '{} in {}'.format(self.name, self.course)

    def __repr__(self):
        return {
            "name": self.name,
            "cat": self.category,
            "desc": self.description,
            "course": self.course,
            "lessontype": self.lessonType,
        }

class LessonCompleted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=3, decimal_places=1)

class WordListQuestion(models.Model):
    native = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE)
    sentenceStructure = models.BooleanField(default=False)

    def __repr__(self):
        return {
            "native": self.native,
            "translation": self.translation,
            "lesson": self.lesson,
        }
