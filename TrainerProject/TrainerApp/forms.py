from django import forms

from .models import Course, CustomUser, Department, Document, Unit

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = (
            'profile_picture',
            'username',
            'first_name',
            'last_name',
            'department',
            'email',
            'phone_number',
            'password'
        )
        
class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_name', 'course_code', 'cycle', 'course_level', 'course_image', )
        
class AddUnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('unit_name', 'unit_code', 'module', 'competency')
        
class AddDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document_name', 'document_file', 'document_type')
        
class SelectionForm(forms.Form):
    
    trainer_name = forms.CharField(max_length=100)
    phone_number = forms.IntegerField()
    trainer_number = forms.CharField(max_length=50)
    name_of_institution = forms.CharField(max_length=200)
    date_of_preparation = forms.DateField()
    number_of_learners = forms.IntegerField()
    course_class = forms.CharField(max_length=50)
    number_weeks = forms.IntegerField()
    number_of_sessions_per_week = forms.IntegerField()
    hours_per_session = forms.IntegerField()
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={'id': 'id_department'})
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        empty_label="Select Course",
        widget=forms.Select(attrs={'id': 'id_course'})
    )
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.none(),
        empty_label="Select Unit",
        widget=forms.Select(attrs={'id': 'id_unit'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3 col-sm-12'
        
        # self.helper.layout(
        #     Row(
        #         Column('trainer_name', css_class='form-group col-md-6 col-sm-12'),
        #         Column('trainer_name', css_class='form-group col-md-6 col-sm-12')
        #     ),
        #     Row(
        #         Column('trainer_number', css_class='form-group col-md-6 col-sm-12'),
        #         Column('name_of_institution', css_class='form-group col-md-6 col-sm-12')
        #     ),
        #     Row(
        #         Column('date_of_preparation', css_class='form-group col-md-6 col-sm-12'),
        #         Column('number_of_learners', css_class='form-group col-md-6 col-sm-12')
        #     ),
        #     Row(
        #         Column('course_class', css_class='form-group col-md-6 col-sm-12'),
        #         Column('number_weeks', css_class='form-group col-md-6 col-sm-12')
        #     ),
        #     Row(
        #         Column('number_of_sessions_per_week', css_class='form-group col-md-6 col-sm-12'),
        #         Column('hours_per_session', css_class='form-group col-md-6 col-sm-12')  
        #     ),
        #     Row(
        #         Column('department', css_class='form-group col-md-4 col-sm-12'),
        #         Column('course', css_class='form-group col-md-4 col-sm-12'),
        #         Column('unit', css_class='form-group col-md-4 col-sm-12')
        #     ),
        #     Submit('submit', 'Submit', css_class='btn btn-primary')
        # )
        
        # Handle server-side queryset filtering for form validation (if form is submitted)
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['course'].queryset = Course.objects.filter(department=department_id).order_by('course_name')
            except (ValueError, TypeError):
                pass
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['unit'].queryset = Unit.objects.filter(course=course_id).order_by('unit_name')
            except (ValueError, TypeError):
                pass

class MpesaForm(forms.Form):
    mpesa_number = forms.IntegerField(label="Enter your Mpesa Number", widget=forms.NumberInput(attrs={'placeholder': '254700XXXXXX'}))