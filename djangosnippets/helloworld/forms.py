from django import forms
from .models import StudyLog

class StudyLogForm(forms.ModelForm):
    class Meta:
        model = StudyLog
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': '今日の学習内容を記入'})
        }
