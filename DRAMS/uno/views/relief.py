from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from uno.models import *

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from urllib.request import urlopen as urlopen

import csv
import datetime
import time
import os
from django.core.files.storage import FileSystemStorage

import googlemaps
from datetime import datetime

import geocoder
from mapbox import Geocoder, DirectionsMatrix, Directions

import requests, json
import random


MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiaGFyaWhhcmFucjE3OTkiLCJhIjoiY2szMWw4Z2hrMGE4bDNubzNrcTZsaHN5ZyJ9.8FfIJ9hkh6TPvD7u5gTgAg"
GOOGLEMAPS_KEY = "AIzaSyDeBKPe6snSckM7qYsFR_Yox7TLen6BXuE"

fs = FileSystemStorage()

gmaps = googlemaps.Client(key=GOOGLEMAPS_KEY)
geocoder = Geocoder(access_token=MAPBOX_ACCESS_TOKEN)
directionsmatrix = DirectionsMatrix(access_token=MAPBOX_ACCESS_TOKEN)
directions = Directions(access_token=MAPBOX_ACCESS_TOKEN)


def getRandomColor():
    letters = '0123456789ABCDEF'
    color = '#'
    for i in range(6):
        color += letters[random.randint(0, 15)]
    return color


def getTimeString():
    import datetime
    time = datetime.datetime.now()
    s = time.strftime("%d%m%y%H%M%S")
    return str(s)


def convertTimeStringtoSec(timeString):
    hh, mm = timeString.split(':')
    hh = int(hh)
    mm = int(mm)
    return hh * 3600 + mm * 60


def geocode(place):
    bounds = {"northeast": {"lat": 13.2350706044533, "lng": 77.835893090333},
              "southwest": {"lat": 12.6580521988705, "lng": 77.3221188537577}}

    # result = gmaps.geocode(address = place, bounds = bounds)[0]
    coordi = result["geometry"]["location"]
    return {"name": place, "coordinates": [coordi["lng"], coordi["lat"]]}


def ReadCSV(filename='default_input.csv'):
    cp = []
    response = requests.get(filename)
    # response = urllib.request.urlopen(filename)
    # csv_reader = csv.reader(response.text)

    # with open(filename) as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader = response.text.split("\r\n")
    for rows in csv_reader:
        row = rows.split(',')
        if len(row) == 1:
            cp.append(geocode(row[0]))
        elif len(row) == 2:
            cp.append({"name": "NA", "coordinates": [float(row[0]), float(row[1])]})
        else:
            name = ""
            for x in row[:-2]:
                name += (x + ", ")
            cp.append({"name": name[:-2], "coordinates": [float(row[-2]), float(row[-1])]})

    # csv_file.close()
    return cp


def get_directionmatrix(origins=[], destinations=[]):
    if len(origins) == 0:
        return {"dm": [], "tm": []}

    distance_matrix = []
    time_matrix = []
    mode = "walking"

    o = []
    for x in origins:
        o.append({"lng": x["coordinates"][0], "lat": x["coordinates"][1]})

    d = []
    for x in destinations:
        d.append({"lat": x["coordinates"][1], "lng": x["coordinates"][0]})

    if len(d) == 0:
        d = o
        mode = "driving"

    for x in o:
        # my_dist = gmaps.distance_matrix(origins = x, destinations = d, mode = mode)

        if my_dist["status"] == "OK":
            dm = my_dist["rows"][0]
            d_row = []
            t_row = []
            for y in range(len(dm["elements"])):
                ele = dm["elements"][y]
                dist = ele["distance"]["value"]
                time = ele["duration"]["value"]
                d_row.append(dist)
                t_row.append(time)
            distance_matrix.append(d_row)
            time_matrix.append(t_row)

    return {"dm": distance_matrix, "tm": time_matrix}


def getLatLng(coordinates):
    return {"lng": coordinates[0], "lat": coordinates[1]}


def findDistance(c1, c2):
    lat = c1[1] - c2[1]
    lng = c1[0] - c2[0]
    return lat ** 2 + lng ** 2


@csrf_exempt
def route_solve(request, instance):
    start_time = 0

    # Results of routes already taken from the developed algorithm
    if instance == "flood":

        busroutes = [[{'name': 'Nodal Center 2', 'coordinates': [77.6011374, 12.9710276]}, {'name': 'Nodal Center 3', 'coordinates': [77.575255, 12.961499]}, {'name': 'Nodal Center 4', 'coordinates': [77.594952, 12.992788]}], [{'name': 'Nodal Center 5', 'coordinates': [77.573816, 12.977989]}], [{'name': 'Nodal Center 6', 'coordinates': [77.615719, 12.973342]}, {'name': 'Nodal Center 7', 'coordinates': [77.592606, 12.953885]}, {'name': 'Nodal Center 8', 'coordinates': [77.5977256, 12.9400027]}, {'name': 'Nodal Center 9', 'coordinates': [77.5799882, 12.9464443]}, {'name': 'Nodal Center 10', 'coordinates': [77.5706605, 12.9483044]}, {'name': 'Nodal Center 11', 'coordinates': [77.5875185, 12.9671789]}], [{'name': 'Nodal Center 12', 'coordinates': [77.606802, 12.975458]}, {'name': 'Nodal Center 13', 'coordinates': [77.625422, 12.974936]}, {'name': 'Nodal Center 14', 'coordinates': [77.595932, 12.983535]}]]
        depot = {"name": "Hospital", "coordinates": [77.6014259, 12.9766927]}

        customerroutes = [[{"name": "C1", "coordinates": [77.581773, 12.9919749]},
                           {"name": "C2", "coordinates": [77.5797214, 12.9560634]},
                           {"name": "C3", "coordinates": [77.589264, 12.9937511]},
                           {"name": "C4", "coordinates": [77.5997376, 12.9717027]},
                           {"name": "C5", "coordinates": [77.588293, 12.99187]},
                           {"name": "C6", "coordinates": [77.5973354, 12.9969503]},
                           {"name": "C7", "coordinates": [77.6004898, 12.9675007]},
                           {"name": "C8", "coordinates": [77.5769988, 12.9588382]},
                           {"name": "C9", "coordinates": [77.6016427, 12.9679703]},
                           {"name": "C10", "coordinates": [77.576293, 12.9586076]}],
                          [{"name": "C11", "coordinates": [77.5785971, 12.9801631]},
                           {"name": "C12", "coordinates": [77.579093, 12.979153]},
                           {"name": "C13", "coordinates": [77.5789691, 12.9852608]},
                           {"name": "C14", "coordinates": [77.5754842, 12.9810472]},
                           {"name": "C15", "coordinates": [77.5794689, 12.9854272]},
                           {"name": "C16", "coordinates": [77.575989, 12.980931]},
                           {"name": "C17", "coordinates": [77.578344, 12.9846679]},
                           {"name": "C18", "coordinates": [77.5791526, 12.985408]},
                           {"name": "C19", "coordinates": [77.5751304, 12.9796817]}],
                          [{"name": "C20", "coordinates": [77.5939335, 12.9673595]},
                           {"name": "C21", "coordinates": [77.6171727, 12.970698]},
                           {"name": "C22", "coordinates": [77.5964887, 12.9445632]},
                           {"name": "C23", "coordinates": [77.5944802, 12.9479753]},
                           {"name": "C24", "coordinates": [77.583453, 12.956667]},
                           {"name": "C25", "coordinates": [77.6148476, 12.975137]},
                           {"name": "C26", "coordinates": [77.5978886, 12.9467759]},
                           {"name": "C27", "coordinates": [77.5678907, 12.9439881]},
                           {"name": "C28", "coordinates": [77.5860947, 12.9393909]},
                           {"name": "C29", "coordinates": [77.5847106, 12.9435159]}],
                          [{"name": "C30", "coordinates": [77.6302884, 12.9702455]},
                           {"name": "C31", "coordinates": [77.6063377, 12.9749292]},
                           {"name": "C32", "coordinates": [77.587675, 12.984703]},
                           {"name": "C33", "coordinates": [77.6195261, 12.9763195]},
                           {"name": "C34", "coordinates": [77.622182, 12.9732937]},
                           {"name": "C35", "coordinates": [77.5931639, 12.9885546]},
                           {"name": "C36", "coordinates": [77.5942613, 12.9835316]},
                           {"name": "C37", "coordinates": [77.5954997, 12.9860892]},
                           {"name": "C38", "coordinates": [77.6256549, 12.9750754]}]]

        depot_coordinates = getLatLng(depot["coordinates"])

        routes = []

        c_count = 1

        busstops = []

        for r_count in range(len(busroutes)):
            route = busroutes[r_count]
            waypoint_coordinates = []
            bss = []
            for bs in route:
                waypoint_coordinates.append(getLatLng(bs["coordinates"]))
                bss.append(bs)

            direction = gmaps.directions(origin=depot_coordinates, destination=depot_coordinates,
                                         waypoints=waypoint_coordinates, mode="driving")
            routes.append({"routes": direction, "bus_stops": bss})

            for bs in bss:
                busstops.append(
                    {"name": bs["name"], "coordinates": bs["coordinates"], "noc": 0, "route": r_count, "rtime": ""})

        cust_points = []

        for ind in range(len(routes)):
            customers = customerroutes[ind]
            bs = routes[ind]["bus_stops"]

            for points in customers:
                mind = 10000000000
                bs_ind = 0
                for hh in range(len(bs)):
                    dist = findDistance(points["coordinates"], bs[hh]["coordinates"])
                    if mind > dist:
                        mind = dist
                        bs_ind = hh
                for hh in range(ind):
                    bs_ind += len(busroutes[hh])

                busstops[bs_ind]["noc"] += 1

                cust_points.append(
                    {"name": points["name"], "coordinates": points["coordinates"], "route": ind, "bus_stop": bs_ind})
                c_count += 1

        par = [["vc", "10"], ["n", "4"], ["occ", "80%"], ["kpt", "60"], ["mw", "1 km"]]

        # colour = ["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e", "#e74a3b", "#858796"]
        colour = ["#0000d0", "#008e00", "#950092", "#ea7000", "#c10022", "#897500"]

        result = {"status": "OK", "routes": routes, "colours": colour[:len(busroutes)], "busstops": busstops,
                  "st": start_time, "depot": depot, "customerpoints": cust_points, "par": par}

    elif instance == "fire":

        busroutes = [[{'name': 'Nodal Center 1', 'coordinates': [77.5733669, 12.9748412]}], [{'name': 'Nodal Center 5', 'coordinates': [77.573816, 12.977989]}]]
        depot = {"name": "Fire Station", "coordinates": [77.6014259, 12.9766927]}

        depot_coordinates = getLatLng(depot["coordinates"])

        routes = []

        busstops = []

        for r_count in range(len(busroutes)):
            route = busroutes[r_count]
            waypoint_coordinates = []
            bss = []
            for bs in route:
                waypoint_coordinates.append(getLatLng(bs["coordinates"]))
                bss.append(bs)

            direction = gmaps.directions(origin=depot_coordinates, destination=depot_coordinates,
                                         waypoints=waypoint_coordinates, mode="driving")
            routes.append({"routes": direction, "bus_stops": bss})

            for bs in bss:
                busstops.append(
                    {"name": bs["name"], "coordinates": bs["coordinates"], "noc": 0, "route": r_count, "rtime": ""})

        par = [["fs", "1"], ["sev", "High"], ["hra", "1"], ["n", "2"], ["ep", "150"]]

        # colour = ["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e", "#e74a3b", "#858796"]
        colour = ["#0000d0", "#008e00", "#950092", "#ea7000", "#c10022", "#897500"]

        result = {"status": "OK", "routes": routes, "colours": colour[:len(busroutes)], "busstops": busstops,
                  "st": start_time, "depot": depot, "par": par}

    elif instance == "covid":
        # Results of routes already taken from the developed algorithm

        busroutes = [[{'name': 'Nodal Center 6', 'coordinates': [77.615719, 12.973342]}, {'name': 'Nodal Center 7', 'coordinates': [77.592606, 12.953885]}, {'name': 'Nodal Center 8', 'coordinates': [77.5977256, 12.9400027]}, {'name': 'Nodal Center 9', 'coordinates': [77.5799882, 12.9464443]}, {'name': 'Nodal Center 10', 'coordinates': [77.5706605, 12.9483044]}, {'name': 'Nodal Center 11', 'coordinates': [77.5875185, 12.9671789]}]]
        depot = {"name": "Police Station", "coordinates": [77.6014259, 12.9766927]}

        depot_coordinates = getLatLng(depot["coordinates"])

        routes = []

        busstops = []

        for r_count in range(len(busroutes)):
            route = busroutes[r_count]
            waypoint_coordinates = []
            bss = []
            for bs in route:
                waypoint_coordinates.append(getLatLng(bs["coordinates"]))
                bss.append(bs)

            direction = gmaps.directions(origin=depot_coordinates, destination=depot_coordinates,
                                         waypoints=waypoint_coordinates, mode="driving")
            routes.append({"routes": direction, "bus_stops": bss})

            for bs in bss:
                busstops.append(
                    {"name": bs["name"], "coordinates": bs["coordinates"], "noc": 0, "route": r_count, "rtime": ""})

        par = [["n", "1"], ["soc", "High"], ["hra", "1"], ["kpt", "60"]]

        colour = ["#950092", "#ea7000", "#c10022", "#897500", "#0000d0", "#008e00"]

        result = {"status": "OK", "routes": routes, "colours": colour[:len(busroutes)], "busstops": busstops,
                  "st": start_time, "depot": depot, "par": par}

    return JsonResponse(result)


def relief_page(request, instance):
    return render(request, instance+'/relief.html', {'instance': instance})
