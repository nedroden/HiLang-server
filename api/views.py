import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login

from api import models


def get_json_response(serialize):
    return HttpResponse(serialize, content_type='application/json')


def index(request):
    return HttpResponse("Dit is een API")


# Login
def login(request):
    if(request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        return get_json_response(serializers.serialize('json', models.User.objects.filter(email=data['email'], password=data['password'])))

# Users
def get_users(request):
    return get_json_response(serializers.serialize('json', models.User.objects.all()))



def get_user(request, user_id):
    return get_json_response(serializers.serialize('json', models.User.objects.filter(id=user_id)))

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



# Subscriptions
def get_user_subscriptions(request, user_id):
    return HttpResponse(serializers.serialize('json', models.Subscription.objects.filter(user=user_id)))


def get_course_subscriptions(request, course_id):
    return get_json_response(serialize.serialize('json', models.Subscription.objects.filter(course=course_id)))

# def login(request):
#     return get_json_response(serializers.serialize('json', models.Subscription.objects.filter(user=user_id)))

    # return get_json_response(serialize.serialize({
    #     'login' : (models.User.get(email=request.POST['email'], password=request.POST['password']) != None)
    # }))
