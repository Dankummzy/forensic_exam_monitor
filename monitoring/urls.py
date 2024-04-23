# monitoring/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('monitor/<int:exam_id>/<int:user_id>/', views.monitor_exam, name='monitor_exam'),
    path('view-logs/', views.MonitoringLogsView.as_view(), name='view_logs'),
    path('log-copy-event/', views.log_copy_event, name='log_copy_event'),
    path('log-paste-event/', views.log_paste_event, name='log_paste_event'),
    path('log-page-minimization/', views.log_page_minimization, name='log_page_minimization'),
    path('log-multiple-face-detection/', views.log_multiple_face_detection, name='log_multiple_face_detection'),
    path('log-face-deviation/', views.log_face_deviation, name='log_face_deviation'),
    path('log-monitoring-data/', views.log_monitoring_data, name='log_monitoring_data'),
    path('dashboard/', views.dashboard, name='dashboard'),  # New URL for the dashboard
]
