from django import forms
from django.contrib.auth import get_user_model

from final_project.main.models import Courses

UserModel = get_user_model()


# CREATE COURSE FORM
class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        exclude = ('participants', 'coach',)


# CONTACT FORM
class ContactForm(forms.Form):
    SUBJECT_MAX_LENGTH = 50
    recipient = forms.EmailField()
    subject = forms.CharField(
        max_length=SUBJECT_MAX_LENGTH,
    )
    message = forms.CharField(widget=forms.Textarea)
