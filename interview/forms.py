from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'answer_text']
        labels = {
            'text': 'Question',
            'answer_text': 'Answer',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
            'answer_text': forms.Textarea(attrs={'rows': 2}),
        }
