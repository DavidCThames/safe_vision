# import the necessary packages
from __future__ import print_function
import argparse
import datetime
import imutils
import cv2
import numpy as np
import sys
import socket
import io


# cap = cv2.VideoCapture(0)



i = 0
people = []
while(True):
    #Start server for Unity Script
    s = socket.socket()
    host = "localhost"
    port = 8800
    s.bind((host, port))

    s.listen(1)
    print("Waiting for a connection...")

    c, addr = s.accept()
    print("Connection from: " + str(addr))

    img_data = c.recv(1024)
    while True:
        data = c.recv(1024)
        if not data:
            break
        img_data += data
    
    # print(img_data)
    nparr = np.fromstring(img_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

    # ret, image = cap.read()
    # image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #     help="path to the input image")
    ap.add_argument("-w", "--win-stride", type=str, default="(8, 8)",
        help="window stride")
    ap.add_argument("-p", "--padding", type=str, default="(16, 16)",
        help="object padding")
    ap.add_argument("-s", "--scale", type=float, default=1.05,
        help="image pyramid scale")
    ap.add_argument("-m", "--mean-shift", type=int, default=-1,
        help="whether or not mean shift grouping should be used")
    args = vars(ap.parse_args())

    # evaluate the command line arguments (using the eval function like
    # this is not good form, but let's tolerate it for the example)
    winStride = eval(args["win_stride"])
    padding = eval(args["padding"])
    meanShift = True if args["mean_shift"] > 0 else False

    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # load the image and resize it
    # image = cv2.imread(args["image"])
    image = imutils.resize(image, width=min(400, image.shape[1]))

    

        

        

    #rotate the image by 90 deg
    image_90 = imutils.rotate_bound(image, 90)


    # detect people in the image
    # start = datetime.datetime.now()
    (rects, weights) = hog.detectMultiScale(image, winStride=winStride,
        padding=padding, scale=args["scale"], useMeanshiftGrouping=meanShift)
    (rects_90, weights_90) = hog.detectMultiScale(image_90, winStride=winStride,
        padding=padding, scale=args["scale"], useMeanshiftGrouping=meanShift)

    # print("[INFO] detection took: {}s".format(
    #    (datetime.datetime.now() - start).total_seconds()))
    
    # draw the original bounding boxes
    
    for (x, y, w, h) in rects:
        people.append((x, y, w, h))            

    for (x, y, w, h) in rects_90:
        people.append((y, x, h, w))


    for (x, y, w, h) in people:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # show the output image
    sys.stdout.write('[')
    for index, (x, y, w, h) in enumerate(people):
        if (index != 0):
            sys.stdout.write(',')
        sys.stdout.write('[' + str(x) + ',' + str(y) + ',' + str(w) + ',' + str(h) + ']')
    sys.stdout.write(']\n')

    i = 0
    people = []

    sys.stdout.flush()
    # cv2.imshow("Detections", image)
    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #     break

cap.release()
cv2.destroyAllWindows()