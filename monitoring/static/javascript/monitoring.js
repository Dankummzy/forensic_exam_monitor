<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Face Detection with OpenCV.js</title>
  <script async src="https://docs.opencv.org/master/opencv.js" onload="onOpenCvReady();" type="text/javascript"></script>
</head>
<body>
  <h1>Face Detection with OpenCV.js</h1>
  <video id="videoInput" width="640" height="480" autoplay></video>
  <canvas id="canvasOutput" width="640" height="480"></canvas>

  <script>
    let video = document.getElementById('videoInput');
    let canvasOutput = document.getElementById('canvasOutput');
    let context = canvasOutput.getContext('2d');
    let faceCascade;

    function onOpenCvReady() {
      // Load the face detection cascade
      faceCascade = new cv.CascadeClassifier();
      faceCascade.load('haarcascade_frontalface_default.xml');

      // Start the video stream
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
          video.srcObject = stream;
        })
        .catch((error) => {
          console.error('Error accessing the camera:', error);
        });

      // Call the processVideo function once the video is playing
      video.addEventListener('playing', processVideo);
    }

    function processVideo() {
      let cap = new cv.VideoCapture(video);
      let frame = new cv.Mat(video.height, video.width, cv.CV_8UC4);
      let gray = new cv.Mat();

      function detectAndDraw() {
        cap.read(frame);
        cv.cvtColor(frame, gray, cv.COLOR_RGBA2GRAY);
        let faces = new cv.RectVector();
        let facesSize = new cv.Size(0, 0);

        // Detect faces
        faceCascade.detectMultiScale(gray, faces, 1.1, 3, 0, facesSize, facesSize);

        // Draw rectangles around the faces
        for (let i = 0; i < faces.size(); ++i) {
          let face = faces.get(i);
          let point1 = new cv.Point(face.x, face.y);
          let point2 = new cv.Point(face.x + face.width, face.y + face.height);
          cv.rectangle(frame, point1, point2, [255, 0, 0, 255]);
        }

        // Display the result on the canvas
        cv.imshow(canvasOutput, frame);
        requestAnimationFrame(detectAndDraw);
      }

      detectAndDraw();
    }
  </script>
</body>
</html>
