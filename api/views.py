from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
import json

from api import models


def get_json_response(serialize):
    return HttpResponse(serialize, content_type='application/json')


def index(request):
    return HttpResponse("Dit is een API")


# Login
def login(request):
    if(request.method == 'POST'):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        return HttpResponse(username + '' + password)


# Users
def get_users(request):
    return get_json_response(serializers.serialize('json', models.User.objects.all()))


def get_user(request, user_id):
    return HttpResponse(serializers.serialize('json', models.User.objects.get(id=user_id).subscription_set().all()))

def get_user_by_cred(request, email, password):
    return HttpResponse(serializers.serialize('json', models.User.objects.filter(email=email, password=password)))


# Courses
def get_courses(request):
    return get_json_response(serializers.serialize('json', models.Course.objects.all()))


def get_course(request, course_id):
    return get_json_response(serializers.serialize('json', models.Course.objects.filter(id=course_id)))


def get_course_lang(request, language_id):
    return get_json_response(serializers.serialize('json', models.Course.objects.filter(language=language_id)))


# Languages
def get_languages(request):
    return get_json_response(serializers.serialize('json', models.Language.objects.all()))


def get_lang_details(request, language_id):
    return get_json_response(serializers.serialize('json', models.Language.objects.filter(id=language_id)))

# Subscriptions
def get_user_subscriptions(request, user_id):
    subscriptionData = serializers.serialize('json', models.Subscription.objects.filter(user=models.User.objects.get(pk=user_id)))
    data = json.loads(subscriptionData)
    returnData = []
    for sub in data:
        course_id = sub['fields']['course']
        courseData = models.Course.objects.get(pk=course_id)
        returnData.append(courseData)
    return get_json_response(serializers.serialize('json', returnData))


def get_course_subscriptions(request, course_id):
    return get_json_response(serializers.serialize('json', models.Subscription.objects.filter(course=course_id)))

