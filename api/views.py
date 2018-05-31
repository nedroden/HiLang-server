import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

from api.models import *

def get_json_response(serialize):
    return HttpResponse(serialize, content_type='application/json')

def index(request):
    return HttpResponse("Dit is een API")

# Login
def login(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        return get_json_response(serializers.serialize('json', User.objects.filter(email=data['email'], password=data['password'])))

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

def get_course(request, course_id):
    return get_json_response(serializers.serialize('json', Course.objects.filter(id=course_id)))

def get_course_lang(request, language_id):
    return get_json_response(serializers.serialize('json', Course.objects.filter(language=language_id)))

def create_course(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(pk=data['user'])
        course = Course(name=data['name'], user=user)
        course.save()
        return get_json_response(serializers.serialize('json', [course]))

# Languages
def get_languages(request):
    return get_json_response(serializers.serialize('json', Language.objects.all()))

# Subscriptions
def get_user_subscriptions(request, user_id):
    return HttpResponse(serializers.serialize('json', Subscription.objects.filter(user=user_id)))

def get_course_subscriptions(request, course_id):
    return get_json_response(serialize.serialize('json', Subscription.objects.filter(course=course_id)))
