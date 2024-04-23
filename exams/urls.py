from django.urls import path
from . import views


urlpatterns = [
    path('exams/student/exams/', views.student_exam_list, name='student_exam_list'),
    path('exams/student/exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('exams/track_event/<int:exam_id>/', views.track_event, name='track_event'),
    path('exams/student/enter_exam_code/', views.enter_exam_code, name='enter_exam_code'),
    path('exams/exam-detail/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exams/exam-completed/', views.exam_completed, name='exam_completed'),
    path('user-exam-list/', views.user_exam_list, name='user_exam_list'),
    path('monitoring-logs/<int:student_id>/<int:exam_id>/', views.monitoring_logs, name='monitoring_logs'),

    # Admin-related URLs
    path('exams/admin/exams/create/', views.create_exam, name='create_exam'),
    path('exams/admin/exams/edit/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('exams/admin/exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('exams/admin/exam-codes/manage/', views.manage_exam_codes, name='manage_exam_codes'),
    path('exams/admin/exam-codes/create/', views.create_exam_code, name='create_exam_code'),
    path('exams/admin/exam-codes/edit/<int:exam_code_id>/', views.edit_exam_code, name='edit_exam_code'),
    path('exams/admin/exam-codes/delete/<int:exam_code_id>/', views.delete_exam_code, name='delete_exam_code'),
    path('exams/admin/exams/view-answers/<int:exam_id>/', views.view_student_answers, name='view_student_answers'),
]

