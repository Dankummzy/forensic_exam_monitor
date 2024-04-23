# main.py in monitoring app

import multiprocessing
import monitoring.proctoring.eye_tracker as eye_tracker
import monitoring.proctoring.face_detector as face_detector
import monitoring.proctoring.face_landmarks as face_landmarks
import monitoring.proctoring.head_pose_estimation as head_pose_estimation
import monitoring.proctoring.mouth_opening_detector as mouth_opening_detector
import time
import channels.layers
from asgiref.testing import ApplicationCommunicator


import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_proctoring_module(module, channel_layer):
    module.run(channel_layer)

if __name__ == '__main__':
    channel_layer = channels.layers.get_channel_layer()

    # Create processes for each Python file
    eye_process = multiprocessing.Process(target=run_proctoring_module, args=(eye_tracker, channel_layer))
    face_detector_process = multiprocessing.Process(target=run_proctoring_module, args=(face_detector, channel_layer))
    face_landmarks_process = multiprocessing.Process(target=run_proctoring_module, args=(face_landmarks, channel_layer))
    head_pose_process = multiprocessing.Process(target=run_proctoring_module, args=(head_pose_estimation, channel_layer))
    mouth_opening_process = multiprocessing.Process(target=run_proctoring_module, args=(mouth_opening_detector, channel_layer))

    # Start the processes
    eye_process.start()
    face_detector_process.start()
    face_landmarks_process.start()
    head_pose_process.start()
    mouth_opening_process.start()

    # Wait for user input to stop the processes
    input("Press enter to stop all processes...")

    # Terminate the processes
    eye_process.terminate()
    face_detector_process.terminate()
    face_landmarks_process.terminate()
    head_pose_process.terminate()
    mouth_opening_process.terminate()

    # Wait for all processes to complete
    eye_process.join()
    face_detector_process.join()
    face_landmarks_process.join()
    head_pose_process.join()
    mouth_opening_process.join()
