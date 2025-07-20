from django import forms
from .models import StudyLog
from .models import Snippet

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['date', 'subject', 'hours', 'comment']  # モデルのフィールド名に合わせてください


class StudyLogForm(forms.ModelForm):
    class Meta:
        model = StudyLog
        fields = ['date', 'subject', 'hours', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }
