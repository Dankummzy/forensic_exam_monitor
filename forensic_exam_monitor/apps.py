# forensic_exam_monitor/apps.py

from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in, user_logged_out
import logging

logger = logging.getLogger(__name__)

def handle_login(sender, request, user, **kwargs):
    # Handle user login event here
    logger.info(f'User {user.username} logged in during the exam.')

def handle_logout(sender, request, user, **kwargs):
    # Handle user logout event here
    logger.info(f'User {user.username} logged out during the exam.')

class ForensicExamMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forensic_exam_monitor'  

    def ready(self):
        # Register signal handlers when the app is ready
        user_logged_in.connect(handle_login)
        user_logged_out.connect(handle_logout)
