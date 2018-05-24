from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses',views.get_courses, name='courses'),
    path('course', views.get_course,name='course'),
]
