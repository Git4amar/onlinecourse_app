import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Course, Enrollment, Choice, Submission, Instructor, Learner
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.utils import IntegrityError
from django.db.models import Max
from .forms import CourseForm, LessonForm, LearnerForm, InstructorForm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.


def registration_request(request):
    
    if request.method == 'GET':
        # define form for learner
        learner_form = LearnerForm()

        # define form for instructor
        instructor_form = InstructorForm()
        instructor_form.helper.attrs = {'style' : 'display: none;'}
        
        context = {
            'user_is':  'default',
            'learner_form': learner_form,
            'instructor_form': instructor_form
        }
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':

        bound_instructor_form = None
        bound_learner_form = None

        try:
            request.POST['occupation']
        except KeyError:
            bound_instructor_form = InstructorForm(request.POST)
            learner_form = LearnerForm()
            learner_form.helper.attrs = {'style' : 'display: none;'}
        else:
            bound_learner_form = LearnerForm(request.POST)
            instructor_form = InstructorForm()
            instructor_form.helper.attrs = {'style' : 'display: none;'}

        if bound_instructor_form and bound_instructor_form.is_valid():
            new_user = bound_instructor_form.save(commit=False)
            new_user.set_password(new_user.password)
            #new_user.save()
            #new_instructor = Instructor(user = new_user, full_time = bound_instructor_form.cleaned_data['fulltime'])
            #new_instructor.save()
            #login(request, new_user)
            #messages.success(request, f"Welcome {new_user.first_name}!, You've successfully registered")
            messages.info(request, f"Request received to register {new_user.username} as Instructor. \
                However, registration as Instructor is disabled for this project demo in order to keep database clean. \
                    Please register as Learner to continue demo")
            #return redirect("onlinecourse:user_courses")
            
        elif bound_learner_form and bound_learner_form.is_valid():
            new_user = bound_learner_form.save(commit=False)
            new_user.set_password(new_user.password)
            new_user.save()
            new_learner = Learner(user = new_user, occupation = request.POST['occupation'])
            new_learner.save()
            login(request, new_user)
            messages.success(request, f"Welcome {new_user.first_name}!, You've successfully registered")
            return redirect("onlinecourse:user_courses")
        
        context = {
            'user_is': 'learner' if bound_learner_form else 'instructor',
            'learner_form': bound_learner_form if bound_learner_form else learner_form,
            'instructor_form': bound_instructor_form if bound_instructor_form else instructor_form
        }
            
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
        
        #username = request.POST['username']
        #password = request.POST['psw']
        #first_name = request.POST['firstname']
        #last_name = request.POST['lastname']
        #user_exist = False
        #try:
        #    User.objects.get(username=username)
        #    user_exist = True
        #except:
        #    logger.error("New user")
        #if not user_exist:
        #    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
        #                                    password=password)
        #    login(request, user)
        #    messages.success(request, f"Welcome {user.first_name}!, You've successfully registered")
        #    return redirect("onlinecourse:user_courses")
        #else:
        #    messages.error(request, 'User already exists.')
        #    return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {user.first_name}!')
            return redirect('onlinecourse:user_courses')
        else:
            messages.error(request, 'Invalid username / password')
            return redirect('onlinecourse:index')
    else:
        return redirect('onlinecourse:index')


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def course_list_view(request):
    context = {}
    user = get_user(request)
    if not user.is_authenticated:
        context['course_list'] = Course.objects.order_by('-total_enrollment')[:10]
    else:
        try:
            context['user_profile'] = user.user_is_instructor.get()
        except Instructor.DoesNotExist:
            context['user_profile'] = user.user_is_learner.get()
                    
        context['course_list'] = Course.objects.exclude(users=user).order_by('-total_enrollment')[:10]
        
    return render(request, 'onlinecourse/course_list_bootstrap.html', context)


def course_details(request, course_id):
    course = Course.objects.get(pk=course_id)
    context = {}
    context["course"] = course

    if get_user(request).is_authenticated:
        
        try:
            if Enrollment.objects.get(user=get_user(request), course=course):
                context["user_is_enrolled"] = True
        except Enrollment.DoesNotExist:
            messages.warning(request, 'You can only access your courses i.e enrolled or created')
            return redirect('onlinecourse:index')
        else:
            try:
                instructor = request.user.user_is_instructor.get()
                if instructor in course.instructors.all():
                    context["user_is_instructor"] = True
                    context['lesson_form'] =  LessonForm()
                    context['lesson_form'].helper.form_action = reverse('onlinecourse:add_lesson', kwargs={'course_id': course.pk})
                    context['lesson_form'].helper.attrs = {'data-course-id': course.pk}
            except Instructor.DoesNotExist:
                context["user_is_instructor"] = False
            finally:
                return render(request, 'onlinecourse/course_detail_bootstrap.html', context)

    else:
        messages.warning(request, 'Not Logged in. Please login or sign up to access course details')
        return redirect('onlinecourse:index')


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = get_user(request)

    if user.is_authenticated:
        if not Enrollment.objects.filter(user=user, course=course).count() > 0:
            # Create an enrollment
            Enrollment.objects.create(user=user, course=course, mode='honor')
            course.total_enrollment = course.course_enrollments.all().count()
            course.save()
            messages.success(request, f"Congratulation {user.first_name}! You're successfully enrolled in {course.name}.")
        
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))
    else:
        messages.warning(request, 'Not Logged in. Please login or sign up to enroll a course')
        return redirect('onlinecourse:index')


@login_required
def submit(request, course_id):
    course = Course.objects.get(pk=course_id)
    user = get_user(request)
    if request.method == "POST":
        user_course_enrollment = user.user_enrollments.get(course=course)
        user_submission = Submission.objects.create(enrollment=user_course_enrollment)
        for key in request.POST:
            if "choice" in key:
                user_submission.choices.add(Choice.objects.get(pk=request.POST[key]))
        user_submission.save()
        return HttpResponseRedirect(reverse(viewname='onlinecourse:submission_result', kwargs={'course_id': course_id, 'submission_id': user_submission.pk}))
    else:
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


@login_required
def show_exam_result(request, course_id, submission_id):
    context = {}
    context['usr_fn'] = get_user(request).first_name
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    context['course'] = course
    context['submission'] =  submission
    course_questions = course.course_questions.all()
    submission_grade = 0
    max_grade = 0
    context['grade_earned'] = {}
    for question in course_questions:
        max_grade += question.grade
        user_selected_choices = submission.choices.filter(question=question)
        selected_ids = []

        for choice in user_selected_choices:
            selected_ids.append(choice.pk)

        if question.is_get_score(selected_ids):
            submission_grade += question.grade
            context['grade_earned'][question.pk] =  question.grade
        else:
            context['grade_earned'][question.pk] =  0
    
    context['grade'] = round((submission_grade / max_grade) * 100)
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


@login_required
def user_courses(request):
    context = {}
    user = get_user(request)

    try:
        context['user_profile'] = user.user_is_instructor.get()
    except Instructor.DoesNotExist:
        context['user_profile'] = user.user_is_learner.get()
        
    if context['user_profile'].role == 'learner':
        context['user_course_list'] = user.user_courses.all().order_by('name')
    else:
        context['user_course_list'] = context['user_profile'].instructor_courses.all().order_by('name')
        
    return render(request, 'onlinecourse/user_course_list.html', context)


@login_required
def unenroll_course(request, course_id):
    if request.method == "POST":
        course_to_unenroll = Course.objects.get(pk=course_id)
        user = request.user
        try:
            enrollment_to_delete = user.user_enrollments.get(course=course_to_unenroll)
        except Enrollment.DoesNotExist:
            messages.error(request, 'Invalid Request')
        else:
            enrollment_to_delete.delete()
            course_to_unenroll.total_enrollment = course_to_unenroll.course_enrollments.all().count()
            course_to_unenroll.save()
            messages.success(request, f"You've successfully unenrolled from {course_to_unenroll.name}")
    else:
        messages.error(request, 'Invalid Request')
    return redirect('onlinecourse:user_courses')


@login_required
def create_course(request):
    if request.method == "GET":
        course_create_form = CourseForm()
        # limit the form choices for multiple instructors to exclude user for empty form instance
        course_create_form.fields['instructors'].queryset = Instructor.objects.exclude(user = request.user)
    else:
        course_create_form = CourseForm(request.POST, request.FILES)
        # limit the form choices for multiple instructors to exclude user for bound form instance
        course_create_form.fields['instructors'].queryset = Instructor.objects.exclude(user = request.user)
        if course_create_form.is_valid():
            new_course = course_create_form.save(commit=False)
            new_course.name = new_course.name.title()
            new_course.save()
            course_create_form.save_m2m()
            new_course.instructors.add(Instructor.objects.get(user = request.user))
            for instructor in new_course.instructors.all():
                print(instructor)
                instructor_enrollment = Enrollment(user = instructor.user, course = new_course)
                instructor_enrollment.save()
            new_course.total_enrollment = new_course.course_enrollments.all().count()
            new_course.save()
            messages.success(request, f'Course {new_course.name} successfully created')
            return redirect('onlinecourse:course_details', course_id = new_course.pk)
    
    return render(request, 'onlinecourse/create_course.html', {
        'form': course_create_form
    })


@login_required
def delete_course(request, course_id):
    # route for POST method
    if request.method == "POST":
        try:
            instructor = Instructor.objects.get(user = request.user)
        except Instructor.DoesNotExist:
            messages.warning(request, 'Invalid request. Not allowed')
        else:
            try:
                course_to_delete = instructor.instructor_courses.get(pk = course_id)
            except Course.DoesNotExist:
                messages.warning(request, 'Invalid request. Not allowed')
            else:
                course_to_delete.delete()
                messages.success(request, f'Course {course_to_delete.name} successfully deleted')
    # route for GET method
    else:
        messages.warning(request, 'Invalid request method. Not allowed')
    # redirect user back to user courses
    return redirect('onlinecourse:user_courses')


@login_required
def add_lesson(request, course_id):
    lesson_in_course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        lesson_form = LessonForm(json.loads(request.body))

        if lesson_form.is_valid():
            new_lesson = lesson_form.save(commit= False)
            new_lesson.course = lesson_in_course
            new_lesson.title = lesson_form.cleaned_data['title'].casefold()
            try:
                new_lesson.save()
            except IntegrityError as error:

                for issue in error.args:
                    
                    if 'order' in issue:
                        course_lessons = Course.objects.get(pk = course_id).course_lessons.all()
                        new_lesson.order = course_lessons.aggregate(Max('order'))['order__max'] + 1

                    if 'title' in issue:
                        error = json.dumps({'title': [f'Lesson titled {new_lesson.title} already exists. Title should be unique within a course.']})
                        return JsonResponse({'errors': error}, status=409)    
                       
                new_lesson.save()
                messages.success(request, f'Lesson {new_lesson.title.capitalize()} successfully added')
                return JsonResponse({'message': f'Lesson {new_lesson.title} successfully added'}, status=200)
                
            else:
                messages.success(request, f'Lesson {new_lesson.title} successfully added')
                return JsonResponse({'message': f'Lesson {new_lesson.title} successfully added'}, status=200)
        else:
            return JsonResponse({'errors': json.dumps(lesson_form.errors)}, status=409)

    else:
        messages.error(request, 'Invalid Method. Not Allowed')
        return redirect('onlinecourse:course_details', course_id = lesson_in_course.pk)


@login_required
def delete_lesson(request, course_id, lesson_id):
    if request.method == "POST":
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        lesson_in_course = instructor.instructor_courses.get(pk = course_id)
        lesson_to_delete = lesson_in_course.course_lessons.get(pk = lesson_id)
        lesson_to_delete.delete()
        for lesson in lesson_in_course.course_lessons.filter(order__gt = lesson_to_delete.order):
            lesson.order -= 1
            lesson.save()
        messages.success(request, f'Lesson: {lesson_to_delete.title.capitalize()} deleted successfully')
    else:
        messages.error(request, 'Invalid Method. Not Allowed')
    return redirect('onlinecourse:course_details', course_id = lesson_in_course.pk)