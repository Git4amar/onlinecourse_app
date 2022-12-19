from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    path('', views.course_list_view, name='index'),
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('course/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('course/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll'),
    path('course/<int:course_id>/submit/', views.submit, name='exam_submission'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='submission_result'),
    path('usercourse/', views.user_courses, name='user_courses'),
    path('course/create', views.create_course, name='create_course'),
    path('course/delete/<int:course_id>', views.delete_course, name='delete_course'),
    path('course/lesson/add/<int:course_id>', views.add_lesson, name='add_lesson'),
    path('course/<int:course_id>/lesson/delete/<int:lesson_id>', views.delete_lesson, name='delete_lesson'),
 ]
