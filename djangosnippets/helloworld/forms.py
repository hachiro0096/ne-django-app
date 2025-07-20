from django import forms
from .models import StudyLog

class StudyLogForm(forms.ModelForm):
    class Meta:
        model = StudyLog
        fields = ['date', 'subject', 'hours', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }
