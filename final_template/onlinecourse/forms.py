"""Forms for Online Course Application"""
from django import forms
from .models import Course, Lesson, Learner
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField


class UserForm(forms.ModelForm):

     # define model for form
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Crispy form helper
        self.helper = FormHelper()
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'onlinecourse:registration'

    first_name = forms.CharField(
        label = 'First Name',
        required = True,
    )

    last_name = forms.CharField(
        label = 'Last Name',
        required = True,
        
    )

    password = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput()
    )


class LearnerForm(UserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_id = 'add_learner_form'
        self.helper.form_class = 'shadow p-3 my-1 bg-body rounded form-horizontal border border-2'
        self.fields['occupation'] = forms.ChoiceField(
            label = 'Occupation',
            choices = Learner.OCCUPATION_CHOICES,
            required = True,
        )
        
        # Crispy form layout
        self.helper.layout = Layout(
            FloatingField(
                'username',
                'first_name',
                'last_name',
                'password',
            ),
            Field('occupation', id = 'option-for-learner'),
            StrictButton('Sign Up', type='submit', css_class='btn btn-primary w-100')
        )


class InstructorForm(UserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.form_id = 'add_instructor_form'
        self.helper.form_class = 'shadow p-3 my-1 bg-body rounded form-horizontal border border-2'
        self.fields['fulltime'] = forms.BooleanField(
                label = 'Full-Time',
                widget = forms.CheckboxInput(),
                required = False
            )
        # Crispy form layout
        self.helper.layout = Layout(
                FloatingField(
                    'username',
                    'first_name',
                    'last_name',
                    'password',
                ),
                Field('fulltime', id = 'option-for-instructor', checked = 'checked'),
                StrictButton('Sign Up', type='submit', css_class='btn btn-primary w-100')
            )


class LessonForm(forms.ModelForm):

    # define model for form
    class Meta:
        model = Lesson
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Crispy form helper
        self.helper = FormHelper()
        self.helper.form_id = 'add_lesson_form'
        self.helper.form_class = 'shadow p-3 my-1 bg-body rounded form-horizontal collapse border border-2'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'POST'

        # Crispy form layout
        self.helper.layout = Layout(
            FloatingField(
                'title',
            ),
            Field('content'),
            StrictButton('Add', type='submit', css_class='btn btn-success w-100')
        )

    # field validations and customization
    title = forms.CharField(
        label = 'Lesson Title',
        validators = [
            RegexValidator(r'^[\w?-]{1}(\s?[,\.\w?-]+){0,197}$',
            message='Name must be between 1 and 200 characters. \
                    Only number, letter, hyphen, comma, period, underscore and one space is allowed between characters.'
            )
        ],
    )

    order = forms.IntegerField(
        required = False
    )


class CourseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructors'] = forms.ModelMultipleChoiceField(
            queryset = None,
            label = 'Additional Instructors',
            required = False,
            widget = forms.CheckboxSelectMultiple(),
        )
        self.helper = FormHelper(self)
        self.helper.form_id = 'create_course_form'
        self.helper.form_class = 'card p-3 mb-5 form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'onlinecourse:create_course'
        
        self.helper.layout = Layout(
            FloatingField(
                'name',
            ),
            Fieldset(
                '',
                'description',
                'image',
                'instructors',
                'pub_date'
            ),
            StrictButton('Create Course', type='submit', css_class='btn btn-primary')
        )

    # VALIDATIONS
    name = forms.CharField(
        label = 'Course Name',
        max_length = 50,
        validators = [
            RegexValidator(
                r'^[\w-]{3}(\s?[\w-]+){0,47}$',
                message='Name must be between 3 and 50 characters. \
                    Only number, letter, hyphen, underscore and one space is allowed between characters.'
            )
        ],
        widget = forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    description = forms.CharField(
        label = 'Description',
        min_length = 3, max_length = 1000,
        widget = forms.Textarea(attrs={'rows': '5'})
    )

    pub_date = forms.DateField(
        label = 'Publication Date',
        widget = forms.DateInput(attrs={'type': 'date', 'class': 'w-auto'})
    )

    image = forms.ImageField(
        label = 'Image for course'
    )


    class Meta:
        model = Course
        exclude = ['is_enrolled', 'users', 'total_enrollment']
