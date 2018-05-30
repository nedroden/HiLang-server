from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Login
    path('login', views.login, name='login'),

    # Users
    path('users/',views.get_users, name='users'),
    path('user/<int:user_id>/', views.get_user, name='user'),
    path('user/<str:email>/<str:password>', views.get_user_by_cred, name='user_cred'),

    # Courses
    path('courses/',views.get_courses, name='courses'),
    path('course/language/<int:language_id>/', views.get_course_lang, name='course_lang'),
    path('course/<int:course_id>/', views.get_course, name='course'),

    # Languages
    path('languages/', views.get_languages, name='languages'),

    # Subscriptions
    path('user/<int:user_id>/subscriptions/', views.get_user_subscriptions, name='user_subscriptions'),
    path('course/<int:course_id>/subscriptions/', views.get_course_subscriptions, name='course_subscriptions')
]

# integratie google, online woordenboek iets in die richting?
# Google translat uitspraak
