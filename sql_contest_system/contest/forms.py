
# -*- coding: utf-8 -*-


from django import forms
from .models import Task_submission

class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Task_submission
        fields = ('solution',)




class AddUsersForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
        table = forms.CharField(widget=forms.Textarea, label=u'Таблица')

