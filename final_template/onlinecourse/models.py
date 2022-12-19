import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings


# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_is_instructor'
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)
    role = models.CharField(max_length=10, default='instructor', editable=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_is_learner'
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200, blank=True)
    role = models.CharField(max_length=7, default='learner', editable=False)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation


# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30)
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor, related_name="instructor_courses")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment', related_name="user_courses")
    is_enrolled = False
    total_enrollment = models.IntegerField(default=0)

    def __str__(self):
        return "Name: " + self.name + ","


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons')
    content = models.TextField()

    class Meta:
        unique_together = [['course', 'order'], ['course', 'title']]

    def __str__(self):
        return f"Title: {self.title}, Course: {self.course}"

# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_enrollments')
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)
    
    class Meta:
        unique_together = ('user', 'course')


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_questions')
    content = models.TextField()
    grade = models.IntegerField(default=1)

    def __str__(self):
        return f"Question: {self.content}, Grade: {self.grade}, Course: {self.course}"

    def is_get_score(self, selected_ids):
        all_answers = self.question_choices.filter(is_correct=True).count()
        selected_correct = self.question_choices.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct and all_answers == len(selected_ids):
            return True
        else:
            return False


class Choice(models.Model):
     content = models.TextField()
     question = models.ForeignKey(Question, related_name='question_choices', on_delete=models.CASCADE)
     is_correct = models.BooleanField()
     
     def __str__(self):
         return f"Choice: {self.content} for Question: {self.question}, Correct: {self.is_correct}"


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='enrollment_submissions')
    choices = models.ManyToManyField(Choice, related_name='choice_in_submissions')
    