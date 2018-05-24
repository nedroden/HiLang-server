import json
from pprint import pprint

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from api import models


def index(request):
    return HttpResponse("Dit is een API")


def get_courses(request):
    response = models.Course.objects.all()
    return HttpResponse(serializers.serialize('json', response))

def get_course(request):
    response = models.Course.objects.filter(id=1)
    return HttpResponse(serializers.serialize('json', response))
