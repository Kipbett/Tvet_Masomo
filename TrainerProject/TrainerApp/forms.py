from django import forms

from .models import Course, CustomUser, Document, Unit


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