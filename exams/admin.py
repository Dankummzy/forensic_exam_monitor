from django.contrib import admin
from .models import Exam, ExamCode, Question, Option, Answer, ProctoringLog, EventLog
from django import forms

# Inline for adding options to questions
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Modify this value to specify the number of options to display

# Inline for adding questions to exams, and each question can have options
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    inlines = [OptionInline]  # Include the OptionInline within QuestionInline

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'description', 'start_time', 'end_time', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')

    fieldsets = [
        (None, {'fields': ['title', 'description']}),
        ('Exam Details', {'fields': ['start_time', 'end_time', 'duration', 'max_attempts', 'is_published']}),
    ]

# Define the CustomQuestionForm
class CustomQuestionForm(forms.ModelForm):
    exam_title = forms.CharField(
        max_length=200,
        required=False,
        help_text="You can either select an existing exam or create a new one.",
    )

    class Meta:
        model = Question
        fields = '__all__'

    def save(self, commit=True):
        exam_title = self.cleaned_data.get('exam_title')
        if exam_title:
            exam, created = Exam.objects.get_or_create(title=exam_title)
            self.instance.exam = exam
        return super().save(commit)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = CustomQuestionForm

# Register the ExamCode model
admin.site.register(ExamCode)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('text', 'question__text')

    fieldsets = [
        (None, {'fields': ['question']}),
        ('Option Details', {'fields': ['text', 'is_correct']}),
    ]

    actions = ['make_correct_option', 'make_incorrect_option']

    def make_correct_option(self, request, queryset):
        queryset.update(is_correct=True)

    make_correct_option.short_description = "Mark selected options as correct"

    def make_incorrect_option(self, request, queryset):
        queryset.update(is_correct=False)

    make_incorrect_option.short_description = "Mark selected options as incorrect"

# Register the Answer model
admin.site.register(Answer)
admin.site.register(EventLog)
admin.site.register(ProctoringLog)

