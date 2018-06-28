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
            if userToken.token == token:
                if user.attempt > 0:
                    user.attempt = 0
                    user.save()
                return True
    except ObjectDoesNotExist:
        return False
    update_attempt(user)
    return False


def update_attempt(user):
    user.attempt += 1
    if user.attempt >= 5:
        destroy_user_tokens(user.pk)
    else:
        user.save()


def parse_params(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if validate_token(data['user_id'], data['token']):
            return data['params']
    return None


def check_token(request):
    if request.method == 'POST':
        if request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
                return JsonResponse({'approved': validate_token(data['user_id'], data['token'])}, safe=False)
            except KeyError:
                pass
    return JsonResponse({'approved': False}, safe=False)


def destroy_token(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = None
        try:
            user = User.objects.get(pk=data['user_id'])
            Token.objects.get(token=data['token'], user=user).delete()
        except (ObjectDoesNotExist, KeyError):
            if user is not None:
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
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        try:
            user = User.objects.get(email=data['email'])
            hashed = bcrypt.hashpw(data['password'].encode(), user.salt.encode())
            if hashed == user.password.encode():
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
    if (data is None):
        return HttpResponseForbidden()
    return get_json_response(serializers.serialize('json', User.objects.all()))


def get_user(request, user_id):
    data = parse_params(request)
    if (data is None):
        return HttpResponseForbidden()

    try:
        user = User.objects.get(pk=user_id)
        return JsonResponse({'id': user.pk,
                             'name': user.name,
                             'email': user.email,
                             'distributor': user.distributor,
                             'created_at': user.created_at}, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({}, safe=False)


def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        try:
            User.objects.get(email=data['email'])
            return JsonResponse({'error': 'E-mail is already in user'})
        except ObjectDoesNotExist:
            try:
                salt = bcrypt.gensalt(14)
                user = User(email=data['email'],
                            name=data['name'],
                            password=bcrypt.hashpw(data['password'].encode(), salt).decode(),
                            distributor=0,
                            salt=salt.decode())
                user.save()
                return JsonResponse(create_session(user), safe=False)
            except IntegrityError as e:
                pass
    return JsonResponse({}, safe=False)


# Courses
def get_popular_courses(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    if 'lang' in data:
        HttpResponse('test');
    else:
        courses = Course.objects.order_by('-subscribers')[:10]
    return get_json_response(serializers.serialize('json', courses))

def get_newest_courses(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    if 'lang' in data:
        HttpResponse('test');
    else:
        courses = Course.objects.order_by('-created_at')[:10]
    return get_json_response(serializers.serialize('json', courses))

def get_course(request, course_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    try:
        courseData = Course.objects.get(id=course_id)
        authorData = User.objects.get(pk=courseData.user.pk)
        print(courseData);
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
            'author': {'name': authorData.name, 'bio': authorData.bio},
            'authorId': courseData.user.pk,
            'description': courseData.description,
            'image': courseData.image,
            'native_lang': courseData.native_lang.pk,
            'trans_lang': courseData.trans_lang.pk,
            'favorite': favorite,
            'subscription': subscription,
            'created_at': courseData.created_at.strftime("%d %b %Y"),
        }
        return JsonResponse(returnData)
    except Exception as e:
        return HttpResponse('false')

def get_public_courses(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    return get_json_response(serializers.serialize('json', Course.objects.filter(public=1)))


def get_course_lang(request, language_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    return get_json_response(serializers.serialize('json', Course.objects.filter(language=language_id)))


def create_course(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    user = User.objects.get(pk=data['user'])
    course = Course(name=data['name'], user=user, trans_lang=Language.objects.get(pk=data['trans_lang']), native_lang=Language.objects.get(pk=data['native_lang']), public=0)
    course.save()
    return get_json_response(serializers.serialize('json', [course]))


def get_user_courses(request, user_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    courseData = Course.objects.filter(user=User.objects.get(pk=user_id))
    return get_json_response(serializers.serialize('json', courseData))

def delete_course(request, course_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    try:
        user = User.objects.get(pk=json.loads(request.body.decode('utf-8'))['user_id'])
        course = Course.objects.filter(pk=course_id, user=user)
        course.delete()
        return HttpResponse("true")
    except ObjectDoesNotExist:
        return HttpResponse("false")

def edit_course_desc(request, course_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    course = Course.objects.get(pk=course_id)
    course.description = data['desc']
    course.save()
    return HttpResponse(request)

def update_course(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    try:
        course = Course.objects.get(pk=data['id'])
        course.name = data['name']
        course.description = data['description']
        course.image = data['image']
        course.native_lang = Language.objects.get(pk=data['native_lang'])
        course.trans_lang = Language.objects.get(pk=data['target_lang'])
        course.save()
    except ObjectDoesNotExist:
        return HttpResponse('false');
    return HttpResponse('true');


def edit_course_lang(request, course_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    course = Course.objects.get(pk=course_id)
    course.trans_lang = Language.objects.get(pk=data['lang_id'])
    course.save()
    return HttpResponse(request)



def search_courses(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    list1 = Course.objects.filter(name__icontains=data['name'])
    list2 = Course.objects.filter(description__icontains=data['name'])
    courseData = list1 | list2
    returnData = []
    for course in courseData:
        author = course.user
        unique = True
        for returnCourse in returnData:
            if course.pk == returnCourse['id']:
                unique = False
        if unique:
            returnData.append({
                'id'          : course.pk,
                'name'        : course.name,
                'description' : course.description,
                'image'       : course.image,
                'subscribers' : course.subscribers,
                'author'      : author.name,
                'trans_lang'  : course.trans_lang.pk,
                'native_lang' : course.native_lang.pk
            })
    return JsonResponse(returnData, safe=False)


# Lessons
def get_lesson_types(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    return get_json_response(serializers.serialize('json', LessonType.objects.all()))


def create_lesson(request, course_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    try:
        # Is this course yours???
        course = Course.objects.get(pk=course_id)
    except ObjectDoesNotExist:
        return get_json_response(serializers.serialize('json', []))

    created = False
    print(data);
    if 'lesson_id' in data:
        created = True
    if (not created):
        lesson = Lesson.objects.create(name=data['title'],
                                       category=data['category'],
                                       description=data['description'],
                                       grammar=data['grammar'],
                                       course=course)
    else:
        lesson = Lesson.objects.get(pk=data['lesson_id'])
        lesson.name = data['title']
        lesson.category = data['category']
        lesson.description = data['description']
        lesson.grammar = data['grammar']
        lesson.save()
        listData = WordListQuestion.objects.filter(lesson=lesson)
        listData.delete()

    upload_questions(data['questions'], lesson)
    return get_json_response(serializers.serialize('json', [lesson]))

def upload_questions(questions, lesson):
    for question in questions:
        entry = WordListQuestion(native=question['native'],
                                 translation=question['translation'],
                                 lesson=lesson,
                                 sentenceStructure=question['sentence'])
        entry.save()

def get_lesson(request, id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    try:
        lesson = Lesson.objects.get(pk=id)
        lesson_vocabulary = list(WordListQuestion.objects.filter(lesson=id).values())

        json_data = {
            'id': lesson.id,
            'name': lesson.name,
            'category': lesson.category,
            'description': lesson.description,
            'grammar': lesson.grammar,
            'course_id': lesson.course_id,
            'vocabulary': lesson_vocabulary
        }
        return JsonResponse(json_data)
    except ObjectDoesNotExist:
        return JsonResponse({}, safe=False)


def get_completed_lessons(request, user_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    completedData = LessonCompleted.objects.filter(user_id=user_id)
    returnData = []
    for lesson in completedData:
        returnData.append({
            'id': lesson.id,
            'lesson_id': lesson.lesson_id,
            'grade': lesson.grade
        })
    return JsonResponse(returnData, safe=False)


def delete_lesson(request, id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    try:
        user = User.objects.get(pk=json.loads(request.body.decode('utf-8'))['user_id'])
        lesson = Lesson.objects.filter(pk=id, course__user=user)
        lesson.delete()
        return HttpResponse("true")
    except ObjectDoesNotExist:
        return HttpResponse("false")


def get_course_lessons(request, course_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    lessonData = Lesson.objects.filter(course_id=course_id)
    return get_json_response(serializers.serialize('json', lessonData))

def get_sentence_questions(request, lesson_id):
    data = parse_params(request)
    if (data ==None):
        return HttpResponseForbidden()

    questions = []
    try:
        lesson = Lesson.objects.get(pk=lesson_id)
        questions = WordListQuestion.objects.filter(lesson=lesson, sentenceStructure=1)
    except ObjectDoesNotExist:
        pass
    return get_json_response(serializers.serialize('json', questions))


def get_lesson_det(request, id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    try:
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
    except ObjectDoesNotExist:
        return HttpResponse("false")


def edit_lesson_desc(request, lesson_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    lesson = Lesson.objects.get(pk=lesson_id)
    data = json.loads(request.body.decode('utf-8'))
    lesson.description = data['desc']
    lesson.save()
    return HttpResponse(request)


def set_lesson_completed(request, user_id, lesson_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    if data['grade'] >= 5.5:
        LessonCompleted.objects.create(user=User.objects.get(pk=user_id),
                                       lesson=Lesson.objects.get(pk=lesson_id),
                                       grade=data['grade'])
    return get_json_response(request)

# Languages
def get_languages(request):
    return get_json_response(serializers.serialize('json', Language.objects.all()))


def get_lang_details(request, language_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    return get_json_response(serializers.serialize('json', Language.objects.filter(id=language_id)))


def get_lang_course(request, course_id):
    data = parse_params(request)
    if data is None:
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
    if data is None:
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
    if data is None:
        return HttpResponseForbidden()

    return get_json_response(serializers.serialize('json', Subscription.objects.filter(course=course_id)))


def subscribe(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    Subscription.objects.create(user=User.objects.get(pk=data['user']),
                                course=Course.objects.get(pk=data['course']))
    course = Course.objects.get(pk=data['course'])
    course.subscribers = course.subscribers + 1
    course.save()
    return get_json_response(request)


def unsubscribe(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()

    entry = Subscription.objects.filter(user=User.objects.get(pk=data['user']),
                                        course=Course.objects.get(pk=data['course']))
    entry.delete()
    course = Course.objects.get(pk=data['course'])
    course.subscribers = course.subscribers - 1
    course.save()
    return get_json_response(request)


# Favorite
def add_favorite(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    Favorite.objects.create(user=User.objects.get(pk=data['user']), course=Course.objects.get(pk=data['course']))
    return get_json_response(request)


def del_favorite(request):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    entry = Favorite.objects.filter(user=User.objects.get(pk=data['user']),
                                    course=Course.objects.get(pk=data['course']))
    entry.delete()
    return get_json_response(request)


def get_user_favorites(request, user_id):
    data = parse_params(request)
    if data is None:
        return HttpResponseForbidden()
    favoriteData = serializers.serialize('json', Favorite.objects.filter(user=User.objects.get(pk=user_id)))
    data = json.loads(favoriteData)
    returnData = []
    for fav in data:
        course_id = fav['fields']['course']
        courseData = Course.objects.get(pk=course_id)
        returnData.append(courseData)
    return get_json_response(serializers.serialize('json', returnData))
