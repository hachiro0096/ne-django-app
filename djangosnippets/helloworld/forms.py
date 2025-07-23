from django import forms
from .models import StudyLog
from .models import Snippet
from .models import Question, Answer
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['icon', 'nickname', 'show_badges']
        widgets = {
            'show_badges': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']


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
