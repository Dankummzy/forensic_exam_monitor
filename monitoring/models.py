from django.db import models
from users.models import User
from exams.models import Exam

class Monitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    face_deviation = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)  # Add this line to include a timestamp field
    logins = models.IntegerField(default=0)  # Add logins field
    logouts = models.IntegerField(default=0)  # Add logouts field
    copy_paste_attempt = models.BooleanField(default=False)
    page_minimized = models.BooleanField(default=False)
    user_inactivity_detected = models.BooleanField(default=False)
    multiple_face_detected = models.BooleanField(default=False)

    def __str__(self):
        return f"Monitoring Session for {self.user.username} - {self.exam.title}"