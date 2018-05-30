from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login

from api import models


def index(request):
    return HttpResponse("Dit is een API")


# Login
def login(request):
    if(request.method == 'POST'):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        return HttpResponse(username + '' + password)
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request,user)
        #     return HttpResponse(request)
        # else:
        #     return HttpResponse(serializers.serialize('json', models.User.objects.all()))


# Users
def get_users(request):
    return HttpResponse(serializers.serialize('json', models.User.objects.all()))


def get_user(request, user_id):
    return HttpResponse(serializers.serialize('json', models.User.objects.filter(id=user_id)))


# Courses
def get_courses(request):
    return HttpResponse(serializers.serialize('json', models.Course.objects.all()))


def get_course(request, course_id):
    return HttpResponse(serializers.serialize('json', models.Course.objects.filter(id=course_id)))


def get_course_lang(request, language_id):
    return HttpResponse(serializers.serialize('json', models.Course.objects.filter(language=language_id)))


# Languages
def get_languages(request):
    return HttpResponse(serializers.serialize('json', models.Language.objects.all()))


# Subscriptions
def get_user_subscriptions(request, user_id):
    return HttpResponse(serializers.serialize('json', models.Subscription.objects.filter(user=user_id)))


def get_course_subscriptions(request, course_id):
    return HttpResponse(serializers.serialize('json', models.Subscription.objects.filter(course=course_id)))

