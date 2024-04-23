from django.db import models
from users.models import User


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()  # Duration of the exam
    max_attempts = models.PositiveIntegerField()  # Maximum allowed attempts
    is_published = models.BooleanField(default=False)  # Whether the exam is visible to users
    auto_submit_time = models.DateTimeField(null=True, blank=True)  # Time for automatic submission
    carry_over = models.BooleanField(default=False)  # Whether it's a carry-over exam
    exam_name = models.CharField(max_length=200, blank=True, null=True)
    exam_code = models.CharField(max_length=20, blank=True, null=True)
    questions = models.ManyToManyField('Question', related_name='question_for_exams')  # Many-to-many relationship with questions

    def __str__(self):
        return self.title

class ExamCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
        

class Question(models.Model):
    TEXT = 'T'
    MULTIPLE_CHOICE = 'MC'
    
    QUESTION_TYPE_CHOICES = [
        (TEXT, 'Text'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions_for_exams')
    text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES, default=MULTIPLE_CHOICE)
    
    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)  # Whether this option is correct for the associated question
    
    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, related_name='exam_answers', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_option = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Answer to {self.question.text}"

    def calculate_score(self):
        """
        Calculate and update the score for this answer.
        You can implement your scoring logic here based on the chosen_option and the correct option.
        """
        # Example: If the chosen_option is correct, give full score (e.g., 1.0), otherwise 0.0
        if self.chosen_option and self.chosen_option.is_correct:
            self.score = 1.0
        else:
            self.score = 0.0

    def save(self, *args, **kwargs):
        self.calculate_score()  # Calculate the score before saving
        super(Answer, self).save(*args, **kwargs)


class ProctoringLog(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    img_data = models.ImageField(upload_to='proctoring_images/')  
    voice_db = models.TextField()
    img_log = models.TextField()
    user_movements_updown = models.TextField()
    user_movements_lr = models.TextField()
    user_movements_eyes = models.TextField()
    phone_detection = models.BooleanField(default=False)
    person_status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    event_type = models.CharField(max_length=50, default="Unknown")  
    event_data = models.TextField(default="") 

    def __str__(self):
        return f"Proctoring Log for Exam: {self.exam.title} - Student: {self.student.username} - Recorded at Time: {self.date_created}"


class EventLog(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    event_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.timestamp}"
