// proctoring_constants.js

const PROCTORING_ALERTS = {
  EYE_TRACKER: "eye_tracker",
  FACE_DETECTOR: "face_detector",
  FACE_LANDMARKS: "face_landmarks",
  HEAD_POSE: "head_pose_estimation",
  MOUTH_OPENING: "mouth_opening_detector",
  // Add more alerts as needed
};

// Export the constants for use in other scripts
if (typeof module !== "undefined" && module.exports) {
  module.exports = PROCTORING_ALERTS;
}
