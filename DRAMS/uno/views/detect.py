from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators import gzip
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.decorators.csrf import csrf_exempt
from uno.models import City, Location
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from uno.defaults import COVID, FIRE
import random

from .predictdisaster import PredictDisaster
from collections import deque
import threading
import time
import os
import cv2
import numpy as np


fps = 24
outputFrame = {}
t = {}

# initialize the predictions queue
size = 120
Q = deque(maxlen=size)

nov = [0, 0]
count_covid = [0, 0]

sev = 0
count_fire = 0


def predict_frame(vid):
    # grab global references to the video stream, output frame, and lock variables
    global outputFrame

    frame = outputFrame['vid'+str(vid)]

    pd = PredictDisaster()
    # loop over frames from the video file stream
    while True:

        if frame is None:
            continue

        frame_preds = pd.predict(frame)

        if frame_preds is not None:
            Q.append(frame_preds)
            # perform prediction averaging over the current
            results = np.array(Q).mean(axis=0)
            i = np.argmax(results)
            label = i
            print(str(vid) + ": " + str(label))
            node = Location.objects.get(cctv=str(vid))
            node.disaster_status = str(1-label)
            node.save()


def generate(vs, vid, instance):
    # grab global references to the output frame and lock variables
    global outputFrame, nov, count_covid, COVID, sev, count_fire, FIRE

    # loop over frames from the video file stream
    while True:
        # read the next frame from the file
        grabbed, frame = vs.read()
        time.sleep(1 / (fps-random.randint(0, 14)))

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            outputFrame['vid'+str(vid)] = None
            break

        outputFrame['vid'+str(vid)] = frame.copy()

        if "covid" in instance:
            cov = COVID[str(vid)]
            ind = count_covid[vid-1]
            nov[vid-1] = cov[ind]
            count_covid[vid-1] = count_covid[vid-1] + 1
        elif "fire" in instance:
            if vid == 2:
                sev = FIRE[count_fire]
                count_fire = count_fire + 1

        # encode the frame in JPEG format
        flag, encodedImage = cv2.imencode(".jpg", frame)

        # ensure the frame was successfully encoded
        if not flag:
            continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encodedImage.tobytes() + b'\r\n\r\n')


@gzip.gzip_page
def video_feed(request, vid, instance):
    try:
        # initialize the video stream
        videofile = os.path.sep.join([os.getcwd(), staticfiles_storage.url('vids/'+instance+str(vid)+'.mp4')])
        vs = cv2.VideoCapture(videofile)

        grabbed, frame = vs.read()
        if grabbed:
            outputFrame['vid' + str(vid)] = frame.copy()

        # try:
        #     if vid == 3:
        #         t['vid' + str(vid)] = threading.Thread(target=predict_frame, args=(vid,))
        #         t['vid' + str(vid)].daemon = True
        #         t['vid' + str(vid)].start()
        # except KeyError as e:
        #     print(e)

        return StreamingHttpResponse(generate(vs, vid, instance), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("***********")
        return None


def detect(request, instance):
    global count_fire, count_covid
    count_fire = 0
    count_covid = [0, 0]
    cities = City.objects.all()
    if len(cities) > 0:
        cn = []
        for city in cities:
            cn.append({"id": city.id, "name": city.name})
    else:
        cn = None

    return render(request, instance+'/detect.html', {'cities': cn, 'instance': instance})


@csrf_exempt
def get_coordinates(request):
    cid = request.POST.get("cid")
    city = City.objects.get(id=int(cid))
    coord = city.coordinates.split(",")

    locs = Location.objects.filter(city=city)
    nodes = []
    for loc in locs:
        nodes.append({
            'name': loc.geography,
            'coordinates': loc.coordinates.split(','),
            'cctvurl': loc.cctv
        })
    data = {
        "lat": float(coord[0]),
        "lng": float(coord[1]),
        "tot": city.total_nodes,
        "live": city.live_nodes,
        "nodes": nodes
    }
    return JsonResponse(data)


@csrf_exempt
def check_video_status(request):
    cid = request.POST.get("cid")
    city = City.objects.get(id=int(cid))
    locs = Location.objects.filter(city=city)
    nodes = []
    for loc in locs:
        nodes.append({
            'cctvurl': loc.cctv,
            'status': loc.flood_status
        })
    data = {
        "nodes": nodes
    }
    return JsonResponse(data)


@csrf_exempt
def check_covid_status(request):
    global nov
    data = {}
    c = 1
    for n in nov:
        data[str(c)] = str(n)
        c = c + 1

    return JsonResponse(data)


@csrf_exempt
def check_fire_status(request):
    global sev
    data = {
        "sev": str(sev)
    }
    return JsonResponse(data)
