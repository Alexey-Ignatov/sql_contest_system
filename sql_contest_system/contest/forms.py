from django import forms
from .models import Task_submission

class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Task_submission
        fields = ('solution',)