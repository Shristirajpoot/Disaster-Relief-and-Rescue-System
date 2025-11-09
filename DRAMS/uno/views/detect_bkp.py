from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
from django.contrib.staticfiles.storage import staticfiles_storage

from .predictdisaster import PredictDisaster
from collections import deque
import threading
import time
import os
import cv2


fps = 24
outputFrame = None

lock = threading.Lock()

# initialize the predictions queue
size = 120
Q = deque(maxlen=size)

# initialize the video stream
videofile = os.path.sep.join([os.getcwd(),staticfiles_storage.url('vids/floods_101_nat_geo.mp4')])
vs = cv2.VideoCapture(videofile)


def predict_frame():
    # grab global references to the video stream, output frame, and lock variables
    global vs, outputFrame, lock

    pd = PredictDisaster()
    j = 1
    # loop over frames from the video file stream
    while True:
        print(j)
        j = j + 1
        # read the next frame from the file
        grabbed, frame = vs.read()
        time.sleep(1/fps)

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break

        # frame_preds = pd.predict(frame)
        #
        # if frame_preds is not None:
        #     Q.append(frame_preds)
        #     # perform prediction averaging over the current
        #     results = np.array(Q).mean(axis=0)
        #     i = np.argmax(results)
        #     label = i
        #
        #     # draw the activity on the output frame
        #     text = "activity: {}".format(label)
        #     cv2.putText(frame, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
        #                 1.25, (0, 255, 0), 5)

        # acquire the lock, set the output frame
        with lock:
            outputFrame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            flag, encodedImage = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encodedImage.tobytes() + b'\r\n\r\n')


@gzip.gzip_page
def video_feed(request):
    # start a thread that will perform motion detection
    t = threading.Thread(target=predict_frame)
    t.daemon = True
    # t.start()
    return None
    try:
        return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("***********")
        print(e)
        return None
