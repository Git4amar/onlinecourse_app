from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Lesson, Instructor, Learner, Question, Choice


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_time', 'role']


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation', 'role']


# Inlines
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 5

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):
    model =  Question
    extra = 5


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['content', 'course']
    list_filter = ['course']
    
    
@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'content', 'is_correct']
    list_filter = ['question', 'is_correct']