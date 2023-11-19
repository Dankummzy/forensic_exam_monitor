from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from exams.models import Exam
from .models import Monitor
import face_recognition

import cv2
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.views.generic.list import ListView


@login_required
def dashboard(request):
    return render(request, 'monitoring/dashboard.html')


class MonitoringLogsView(ListView):
    model = Monitor
    template_name = 'monitor_list.html'
    context_object_name = 'logs'


# Helper function to check user login status (customize based on your authentication system)
def check_login_status(user):
    return user.is_authenticated

# Helper function to detect user inactivity (customize based on your inactivity detection)
def check_user_inactivity(user_inactivity_timer, user_inactivity_threshold):
    if user_inactivity_timer >= user_inactivity_threshold:
        return True
    return False

# Helper function to log user inactivity event
def log_user_inactivity(monitor_session):
    monitor_session.user_inactivity_detected = True

# Helper function to log login/logout event
def login_logout(monitor_session, user_logged_in):
    if user_logged_in:
        monitor_session.logins += 1
    else:
        monitor_session.logouts += 1

@csrf_exempt
def log_login_logout(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    monitor_session = Monitor.objects.latest('start_time')
    
    user_logged_in = check_login_status(request.user)
    
    login_logout(monitor_session, user_logged_in)
    
    monitor_session.save()
    
    return JsonResponse({"message": "Login/Logout event logged."})

@csrf_exempt
def log_copy_event(request):
    if request.method == 'POST' and request.POST.get('event') == 'copy':
        monitor_session = Monitor.objects.latest('start_time')
        monitor_session.copy_paste_attempt = True
        monitor_session.save()
        return JsonResponse({"message": "Copy event logged."})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def log_paste_event(request):
    if request.method == 'POST' and request.POST.get('event') == 'paste':
        monitor_session = Monitor.objects.latest('start_time')
        monitor_session.copy_paste_attempt = True
        monitor_session.save()
        return JsonResponse({"message": "Paste event logged."})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def log_page_minimization(request):
    if request.method == 'POST':
        monitor_session = Monitor.objects.latest('start_time')
        monitor_session.page_minimized = True
        monitor_session.save()
        return JsonResponse({"message": "Page minimization event logged."})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def log_face_deviation(request):
    if request.method == 'POST':
        monitor_session = Monitor.objects.latest('start_time')
        monitor_session.face_deviation = True
        monitor_session.save()
        return JsonResponse({"message": "Face deviation event logged."})
    return HttpResponseBadRequest("Invalid request")


@csrf_exempt
def log_multiple_face_detection(request):
    if request.method == 'POST':
        monitor_session = Monitor.objects.latest('start_time')
        monitor_session.multiple_face_detected = True
        monitor_session.save()
        return JsonResponse({"message": "Multiple face detection event logged."})
    return HttpResponseBadRequest("Invalid request")

@csrf_exempt
def log_monitoring_data(request):
    if request.method == 'POST':
        monitor_session = Monitor.objects.latest('start_time')
        multiple_face_detected = request.POST.get('multipleFaceDetected', 'false')
        facial_deviations = request.POST.get('facialDeviations', 'false')
        monitor_session.multiple_face_detected = multiple_face_detected == 'true'
        monitor_session.face_deviation = facial_deviations == 'true'
        monitor_session.save()
        return JsonResponse({"message": "Monitoring data logged."})
    return HttpResponseBadRequest("Invalid request")

@login_required
def monitor_exam(request, exam_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    exam = get_object_or_404(Exam, pk=exam_id)

    monitor_session = Monitor(user=user, exam=exam)
    monitor_session.save()

    cap = cv2.VideoCapture(0)

    is_logged_in = True
    last_login_state = is_logged_in

    while True:
        ret, frame = cap.read()

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)

        multiple_face_detected = False
        if len(face_locations) > 1:
            multiple_face_detected = True

        monitor_session.multiple_face_detected = multiple_face_detected

        deviation_detected = False

        if face_locations:
            for face_location in face_locations:
                top, right, bottom, left = face_location
                frame_height, frame_width, _ = frame.shape
                expected_x = frame_width // 2
                expected_y = frame_height // 2
                deviation_x = abs(expected_x - (left + right) // 2)
                deviation_y = abs(expected_y - (top + bottom) // 2)
                deviation_threshold = 50

                if deviation_x > deviation_threshold or deviation_y > deviation_threshold:
                    deviation_detected = True
                    break

        if deviation_detected:
            monitor_session.face_deviation = True

        if document.hidden:  # Customize this based on your requirements
            monitor_session.page_minimized = True

        current_login_state = check_login_status(request.user)

        if current_login_state != last_login_state:
            is_logged_in = current_login_state
            log_login_logout(monitor_session, is_logged_in)

        last_login_state = current_login_state

        if check_user_inactivity(monitor_session.user_inactivity_timer, monitor_session.user_inactivity_threshold):
            log_user_inactivity(monitor_session)

        if current_login_state:
            monitor_session.user_inactivity_timer = 0
        else:
            monitor_session.user_inactivity_timer += 1

        condition_to_end_monitoring = False

        if condition_to_end_monitoring:
            break

    cap.release()
    cv2.destroyAllWindows()

    monitor_session.end_time = timezone.now()
    monitor_session.save()

    return render(request, 'monitoring/monitor_exam.html', {'exam_id': exam_id, 'user_id': user_id})


