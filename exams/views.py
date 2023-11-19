from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ExamForm, ExamCodeForm, AnswerForm
from .models import Exam, ExamCode, Answer, Question, Option


def enter_exam_code(request):
    if request.method == 'POST':
        form = ExamCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                exam_code = ExamCode.objects.get(code=code)
                # Associate the exam with the user, you may use request.user here
                request.user.exam_code = exam_code
                request.user.save()
                return redirect('exam_page')
            except ExamCode.DoesNotExist:
                form.add_error('code', 'Invalid exam code')
    else:
        form = ExamCodeForm()
    return render(request, 'exams/enter_exam_code.html', {'form': form})


# View to display available exams to students
@login_required
def student_exam_list(request):
    exams = Exam.objects.filter(is_published=True)
    return render(request, 'exams/student_exam_list.html', {'exams': exams})


@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Question.objects.filter(exam=exam)
    if request.method == 'POST':
        for question in questions:
            option_id = request.POST.get(f'question_{question.id}')
            if option_id:
                option = Option.objects.get(id=option_id)
                Answer.objects.create(user=request.user, exam=exam, question=question, chosen_option=option)
        return redirect('exam_completed')  # Redirect to a page indicating the exam is completed
    return render(request, 'exams/take_exam.html', {'exam': exam, 'questions': questions})


def exam_completed(request):
    # Your logic for handling exam completion and rendering the completion page
    return render(request, 'exams/exam_completed.html')


# View to create a new exam
@staff_member_required
def create_exam(request):
    # Implement the logic for creating a new exam
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = ExamForm()
    return render(request, 'exams/create_exam.html', {'form': form})


# View to edit an existing exam
@staff_member_required
def edit_exam(request, exam_id):
    # Implement the logic for editing an exam
    exam = get_object_or_404(Exam, pk=exam_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            exam = form.save()
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exams/edit_exam.html', {'form': form, 'exam': exam})


# View to delete an existing exam
@staff_member_required
def delete_exam(request, exam_id):
    # Implement the logic for deleting an exam
    exam = get_object_or_404(Exam, pk=exam_id)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam_list')
    return render(request, 'exams/delete_exam.html', {'exam': exam})


@staff_member_required
def manage_exam_codes(request):
    exam_codes = ExamCode.objects.all()
    return render(request, 'exams/manage_exam_codes.html', {'exam_codes': exam_codes})


@staff_member_required
def create_exam_code(request):
    # Implement the logic for creating a new exam code
    if request.method == 'POST':
        form = ExamCodeForm(request.POST)
        if form.is_valid():
            exam_code = form.save()
            return redirect('manage_exam_codes')
    else:
        form = ExamCodeForm()
    return render(request, 'exams/create_exam_code.html', {'form': form})


@staff_member_required
def edit_exam_code(request, exam_code_id):
    # Implement the logic for editing an exam code
    exam_code = get_object_or_404(ExamCode, pk=exam_code_id)
    if request.method == 'POST':
        form = ExamCodeForm(request.POST, instance=exam_code)
        if form.is_valid():
            exam_code = form.save()
            return redirect('manage_exam_codes')
    else:
        form = ExamCodeForm(instance=exam_code)
    return render(request, 'exams/edit_exam_code.html', {'form': form, 'exam_code': exam_code})

@staff_member_required
def delete_exam_code(request, exam_code_id):
    # Implement the logic for deleting an exam code
    exam_code = get_object_or_404(ExamCode, pk=exam_code_id)
    if request.method == 'POST':
        exam_code.delete()
        return redirect('manage_exam_codes')
    return render(request, 'exams/delete_exam_code.html', {'exam_code': exam_code})


# View to view student answers and give scores
@staff_member_required
def view_student_answers(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    student_answers = Answer.objects.filter(exam=exam)

    if request.method == 'POST':
        # Implement logic for scoring student answers and saving scores using AnswerForm
        form = AnswerForm(request.POST)
        if form.is_valid():
            # Process and save scores here
            for answer in student_answers:
                chosen_option = form.cleaned_data[f'chosen_option_{answer.id}']
                if chosen_option:
                    answer.chosen_option = chosen_option
                    answer.calculate_score()  # Calculate and update the score
                    answer.save()

            # Redirect to a confirmation or summary page
            return redirect('exam_completed')  # Replace 'exam_completed' with the appropriate URL

    else:
        # Create a form to collect scores
        form = AnswerForm()
        for answer in student_answers:
            # Add a field for each student's chosen option to the form
            form.fields[f'chosen_option_{answer.id}'] = forms.ModelChoiceField(
                queryset=Option.objects.filter(question=answer.question),
                required=False,
                widget=forms.RadioSelect
            )

    return render(request, 'exams/view_student_answers.html', {'exam': exam, 'student_answers': student_answers, 'form': form})


def calculate_total_score(user, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    user_answers = Answer.objects.filter(user=user, exam=exam)
    
    total_score = sum(answer.score for answer in user_answers)
    
    return total_score


def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    user = request.user  # Assuming you have user authentication in place
    total_score = calculate_total_score(user, exam_id)  # Implement this function
    return render(request, 'exams/exam_detail.html', {'exam': exam, 'total_score': total_score})
