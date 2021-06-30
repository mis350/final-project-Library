from django import forms
from .models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class RatingForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude = ['student', 'book']
