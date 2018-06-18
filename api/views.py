import json
import bcrypt
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
import json
import string
import random
import pprint
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from api.models import *


def index(request):
    return HttpResponse("Dit is een API")


def generate_token():
    alphabet = string.ascii_letters + string.digits
    while True:
        return ''.join(random.SystemRandom().choice(alphabet) for i in range(60))


def validate_token(userId, token):
    try:
        user = User.objects.get(pk=userId)
        userTokens = Token.objects.filter(user=user)
        for userToken in userTokens:
            if (userToken.token == token):
                if (user.attempt > 0):
                    user.attempt = 0
                    user.save()
                return True
    except ObjectDoesNotExist:
        return False
    update_attempt(user)
    return False


def update_attempt(user):
    user.attempt += 1
    if (user.attempt >= 5):
        destroy_user_tokens(user.pk)
    else:
        user.save()


def parse_params(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        if (validate_token(data['user_id'], data['token'])):
            return data['params']
    return None


def check_token(request):
    if (request.method == 'POST'):
        if (request.body):
            try:
                data = json.loads(request.body.decode('utf-8'))
                return JsonResponse({'approved': validate_token(data['user_id'], data['token'])}, safe=False)
            except KeyError:
                pass
    return JsonResponse({'approved': False}, safe=False)


def destroy_token(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        user = None
        try:
            user = User.objects.get(pk=data['user_id'])
            Token.objects.get(token=data['token'], user=user).delete()
        except (ObjectDoesNotExist, KeyError):
            if user != None:
                update_attempt(user)
    return HttpResponse('Tokens destroyed')


def destroy_user_tokens(user_id):
    user = User.objects.get(pk=user_id)
    user.attempt = 0
    user.save()
    Token.objects.filter(user=user).delete()


def get_json_response(serialize):
    return HttpResponse(serialize, content_type='application/json')


# Login
def login(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        try:
            user = User.objects.get(email=data['email'])
            hashed = bcrypt.hashpw(data['password'].encode(), user.salt.encode())
            print(hashed)
            print(user.password.encode())
            if (hashed == user.password.encode()):
                return JsonResponse(create_session(user), safe=False)
        except ObjectDoesNotExist:
            pass
    return JsonResponse({}, safe=False)


def create_session(user):
    token = Token(token=generate_token(), user=user)
    token.save()
    response = {
                'user_id': user.pk,
                'token': token.token
                }
    return response


# Users
def get_users(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    return get_json_response(serializers.serialize('json', User.objects.all()))


def get_user(request, user_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    return get_json_response(serializers.serialize('json', User.objects.filter(id=user_id)))


def create_user(request):
    if (request.method == 'POST'):
        data = json.loads(request.body.decode('utf-8'))
        try:
            User.objects.get(email=data['email'])
            return JsonResponse({'error': 'E-mail is already in user'})
        except ObjectDoesNotExist:
            try:
                salt = bcrypt.gensalt(14).decode()
                user = User(email=data['email'],
                            name=data['name'],
                            password=bcrypt.hashpw(data['password'].encode(), salt),
                            distributor=0,
                            salt=salt)
                user.save()
                return JsonResponse(create_session(user), safe=False)
            except IntegrityError as e:
                pass
    return JsonResponse({}, safe=False)


# Courses
def get_courses(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    return get_json_response(serializers.serialize('json', Course.objects.all()))


def get_course(request, course_id, user_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    courseData = Course.objects.get(id=course_id)
    authorData = User.objects.get(pk=user_id)
    favoriteData = Favorite.objects.filter(user=authorData, course=Course.objects.get(pk=course_id))
    subscriptionData = Subscription.objects.filter(user=authorData, course=Course.objects.get(pk=course_id))
    if not favoriteData:
        favorite = False
    else:
        favorite = True

    if not subscriptionData:
        subscription = False
    else:
        subscription = True

    returnData = {
        'id': courseData.id,
        'name': courseData.name,
        'author': authorData.name,
        'authorId': courseData.user.pk,
        'description': courseData.description,
        'image': courseData.image,
        'favorite': favorite,
        'subscription': subscription
    }
    return JsonResponse(returnData)


def get_public_courses(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    return get_json_response(serializers.serialize('json', Course.objects.filter(public=1)))


def get_course_lang(request, language_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    return get_json_response(serializers.serialize('json', Course.objects.filter(language=language_id)))


def create_course(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    user = User.objects.get(pk=data['user'])
    course = Course(name=data['name'], user=user)
    course.save()
    return get_json_response(serializers.serialize('json', [course]))


def get_user_courses(request, user_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    courseData = Course.objects.filter(user=User.objects.get(pk=user_id))
    return get_json_response(serializers.serialize('json', courseData))


def edit_course_desc(request, course_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    course = Course.objects.get(pk=course_id)
    course.description = data['desc']
    course.save()
    return HttpResponse(request)


def search_courses(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    list1 = Course.objects.filter(name__icontains=data['name'], public=1)
    list2 = Course.objects.filter(description__icontains=data['name'], public=1)
    courseData = list1 | list2
    returnData = []
    for course in courseData:
        author = course.user
        unique = True
        for returnCourse in returnData:
            if course.id == returnCourse['id']:
                unique = False
        if unique:
            returnData.append(
                {
                    "id": course.id,
                    "name": course.name,
                    "description": course.description,
                    "image": course.image,
                    "subscribers": course.subscribers,
                    "author": author.name
                }
            )
    return JsonResponse(returnData, safe=False)


# Lessons
def get_lesson_types(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden();
    return get_json_response(serializers.serialize('json', LessonType.objects.all()))


def create_lesson(request, course_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden();
        
    try:
        course = Course.objects.get(pk=course_id)
        lessonType = LessonType.objects.get(pk=data['lessonType'])
    except ObjectDoesNotExist:
        return get_json_response(serializers.serialize('json', []))

    if Lesson.objects.get(pk=data['id']) == None:
        lesson = Lesson(name=data['title'],
                        category=data['category'],
                        description=data['description'],
                        grammar=data['grammar'],
                        course=course,
                        lessonType=lessonType)
        lesson.save()
        for question, answer in data['words'].items():
            entry = WordListQuestion(native=question, translation=answer, lesson=lesson)
            entry.save()
    else:
        lesson = Lesson.objects.get(pk=data['id'])
        lesson.name = data['title']
        lesson.category = data['category']
        lesson.description = data['description']
        lesson.grammar = data['grammar']
        lesson.save()
        listData = WordListQuestion.objects.filter(lesson=lesson)
        listData.delete()
        for question, answer in data['words'].items():
            entry = WordListQuestion(native=question, translation=answer, lesson=lesson)
            entry.save()
    return get_json_response(serializers.serialize('json', [lesson]))


def get_lesson(request, id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    lesson = list(Lesson.objects.filter(pk=id).values())
    lesson[0]['vocabulary'] = list(WordListQuestion.objects.filter(lesson=id).values())

    return HttpResponse(json.dumps(lesson), content_type='application/json')


def delete_lesson(request, id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    if request.method == 'DELETE':
        lesson = Lesson.objects.get(pk=id)
        lesson.delete(id)
        return HttpResponse()


def get_course_lessons(request, course_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    lessonData = Lesson.objects.filter(course_id=course_id)
    return get_json_response(serializers.serialize('json', lessonData))


def get_lesson_det(request, id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    lessonData = Lesson.objects.get(pk=id)
    courseData = Course.objects.get(pk=lessonData.course_id)
    nativeData = Language.objects.get(pk=courseData.native_lang.id)
    transData = Language.objects.get(pk=courseData.trans_lang.id)
    returnData = {
        "id": lessonData.id,
        "name": lessonData.name,
        "cat": lessonData.category,
        "desc": lessonData.description,
        "grammar": lessonData.grammar,
        "native": nativeData.name,
        "trans": transData.name
    }
    return JsonResponse(returnData)


def edit_lesson_desc(request, lesson_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    lesson = Lesson.objects.get(pk=lesson_id)
    data = json.loads(request.body.decode('utf-8'))
    lesson.description = data['desc']
    lesson.save()
    return HttpResponse(request)


# Languages
def get_languages(request):
    return get_json_response(serializers.serialize('json', Language.objects.all()))


def get_lang_details(request, language_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    return get_json_response(serializers.serialize('json', Language.objects.filter(id=language_id)))

def get_lang_course(request, course_id):
    data = parse_params(request)
    if data == None:
        return HttpResponseForbidden()

    courseData = Course.objects.get(pk=course_id)
    nativeData = Language.objects.get(pk=courseData.native_lang.id)
    transData = Language.objects.get(pk=courseData.trans_lang.id)
    returnData = {
        "native": nativeData.name,
        "trans": transData.name
    }
    return JsonResponse(returnData)

# Subscriptions
def get_user_subscriptions(request, user_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    subscriptionData = serializers.serialize('json', Subscription.objects.filter(user=User.objects.get(pk=user_id)))
    data = json.loads(subscriptionData)
    returnData = []
    for sub in data:
        course_id = sub['fields']['course']
        courseData = Course.objects.get(pk=course_id)
        returnData.append(courseData)
    return get_json_response(serializers.serialize('json', returnData))


def get_course_subscriptions(request, course_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    return get_json_response(serializers.serialize('json', Subscription.objects.filter(course=course_id)))


def subscribe(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    Subscription.objects.create(user=User.objects.get(pk=data['user']),
                                course=Course.objects.get(pk=data['course']))
    return get_json_response(request)


def unsubscribe(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()

    entry = Subscription.objects.filter(user=User.objects.get(pk=data['user']),
                                        course=Course.objects.get(pk=data['course']))
    entry.delete()
    return get_json_response(request)


# Favorite
def add_favorite(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    Favorite.objects.create(user=User.objects.get(pk=data['user']), course=Course.objects.get(pk=data['course']))
    return get_json_response(request)


def del_favorite(request):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    entry = Favorite.objects.filter(user=User.objects.get(pk=data['user']),
                                    course=Course.objects.get(pk=data['course']))
    entry.delete()
    return get_json_response(request)


def get_user_favorites(request, user_id):
    data = parse_params(request)
    if (data == None):
        return HttpResponseForbidden()
    favoriteData = serializers.serialize('json', Favorite.objects.filter(user=User.objects.get(pk=user_id)))
    data = json.loads(favoriteData)
    returnData = []
    for fav in data:
        course_id = fav['fields']['course']
        courseData = Course.objects.get(pk=course_id)
        returnData.append(courseData)
    return get_json_response(serializers.serialize('json', returnData))
