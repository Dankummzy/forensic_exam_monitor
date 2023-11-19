from django import forms
from .models import Exam, ExamCode, Answer, Question


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamCodeForm(forms.Form):
    exam_code = forms.CharField(label='Enter Exam Code', max_length=20)


# Create a form to display and handle user responses
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['chosen_option']
        widgets = {
            'chosen_option': forms.RadioSelect,
        }
