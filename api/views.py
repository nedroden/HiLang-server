import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
import json
import string
import random
from django.db import IntegrityError
from api.models import *

def generate_token():
    alphabet = string.ascii_letters + string.digits
    while True:
        return ''.join(random.SystemRandom().choice(alphabet) for i in range(60))

def get_json_response(serialize):
    return HttpResponse(serialize, content_type='application/json')


def index(request):
    return HttpResponse("Dit is een API")


# Login
def login(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(email=data['email'], password=data['password'])
        token = Token(token=generate_token(), user=User.objects.get(pk=1))
        token.save()
        return JsonResponse({'user': {'email': user.email,
                                      'name': user.name,
                                      'distributor': user.distributor,},
                             'token': token.token}, safe=False)
        # token = Token(token=generate_token(), user=user)
        # token.save()
        # #returnData = [user, repr(token)]
        # returnData = {'user': user,
        #               'token': token}
        # return get_json_response(serializers.serialize('json', json.dumps(returnData)))
        #return get_json_response(serializers.serialize('json', [user]))

# Users
def get_users(request):
    return get_json_response(serializers.serialize('json', User.objects.all()))


def get_user(request, user_id):
    return get_json_response(serializers.serialize('json', User.objects.filter(id=user_id)))


def create_user(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        user = User(email=data['email'], name=data['name'], password=data['password'], distributor=0)
        try:
            user.save()
            return get_json_response(serializers.serialize('json', [user]))
        except IntegrityError as e:
            return get_json_response(serializers.serialize('json', []))


# Courses
def get_courses(request):
    return get_json_response(serializers.serialize('json', Course.objects.all()))


def get_course(request, course_id, user_id):
    courseData = Course.objects.get(id=course_id)
    authorData = User.objects.get(pk=user_id)
    favoriteData = Favorite.objects.filter(user=authorData,course=Course.objects.get(pk=course_id))
    if not favoriteData:
        favorite = False
    else:
        favorite = True

    returnData = {
        'id': courseData.id,
        'name': courseData.name,
        'author': authorData.name,
        'authorId': courseData.user.pk,
        'description': courseData.description,
        'image': courseData.image,
        'favorite': favorite
    }
    return JsonResponse(returnData)


def get_public_courses(request):
    return get_json_response(serializers.serialize('json', Course.objects.filter(public=1)))


def get_course_lang(request, language_id):
    return get_json_response(serializers.serialize('json', Course.objects.filter(language=language_id)))


def create_course(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(pk=data['user'])
        course = Course(name=data['name'], user=user)
        course.save()
        return get_json_response(serializers.serialize('json', [course]))


def get_user_courses(request, user_id):
    courseData = Course.objects.filter(user=User.objects.get(pk=user_id))
    return get_json_response(serializers.serialize('json', courseData))


def edit_course_desc(request, course_id):
    course = Course.objects.get(pk=course_id)
    data = json.loads(request.body.decode('utf-8'))
    course.description = data['desc']
    course.save()
    return HttpResponse(request)


# Lessons
def get_lesson(request, id):
    lesson = list(Lesson.objects.filter(pk=id).values())
    lesson[0]['vocabulary'] = list(WordListQuestion.objects.filter(lesson=id).values())

    return HttpResponse(json.dumps(lesson), content_type='application/json')


def delete_lesson(request, id):
    if request.method == 'DELETE':
        lesson = Lesson.objects.get(pk=id)
        lesson.delete(4)
        return HttpResponse()


def get_course_lessons(request, course_id):
    lessonData = Lesson.objects.filter(course_id=course_id)
    return get_json_response(serializers.serialize('json', lessonData))


def get_lesson_det(request, id):
    lessonData = Lesson.objects.get(pk=id)
    returnData = {
        "id": lessonData.id,
        "name": lessonData.name,
        "cat": lessonData.category,
        "desc": lessonData.description,
        "native": lessonData.native_lang_id,
        "translation": lessonData.trans_lang_id
    }
    return JsonResponse(returnData)


def edit_lesson_desc(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    data = json.loads(request.body.decode('utf-8'))
    lesson.description = data['desc']
    lesson.save()
    return HttpResponse(request)


# Languages
def get_languages(request):
    return get_json_response(serializers.serialize('json', Language.objects.all()))


def get_lang_details(request, language_id):
    return get_json_response(serializers.serialize('json', Language.objects.filter(id=language_id)))


# Subscriptions
def get_user_subscriptions(request, user_id):
    subscriptionData = serializers.serialize('json', Subscription.objects.filter(user=User.objects.get(pk=user_id)))
    data = json.loads(subscriptionData)
    returnData = []
    for sub in data:
        course_id = sub['fields']['course']
        courseData = Course.objects.get(pk=course_id)
        returnData.append(courseData)
    return get_json_response(serializers.serialize('json', returnData))


def get_course_subscriptions(request, course_id):
    return get_json_response(serializers.serialize('json', Subscription.objects.filter(course=course_id)))


# Favorite
def add_favorite(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        Favorite.objects.create(user=User.objects.get(pk=data['user']), course=Course.objects.get(pk=data['course']))
    return get_json_response(request)


def del_favorite(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        entry = Favorite.objects.filter(user=User.objects.get(pk=data['user']), course=Course.objects.get(pk=data['course']))
        entry.delete()
    return get_json_response(request)


def get_user_favorites(request, user_id):
    favoriteData = serializers.serialize('json', Favorite.objects.filter(user=User.objects.get(pk=user_id)))
    data = json.loads(favoriteData)
    returnData = []
    for fav in data:
        course_id = fav['fields']['course']
        courseData = Course.objects.get(pk=course_id)
        returnData.append(courseData)
    return get_json_response(serializers.serialize('json', returnData))
