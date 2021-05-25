'''
        Proyecto IA

Creado por:

Juan Fernando De Leon Quezada       17822
Jose Gabriel Block Staackman        18935

'''

import cv2
from tracker import *

def main():
    # Create Tracker Object
    tracker = EuclideanDistTracker()

    # Read frames from video
    cap = cv2.VideoCapture("./Videos/Video-2-IA.mp4")

    # Object Detection
    '''This will detect the moving objects'''
    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    while True:
        ret, frame = cap.read()

        # height, width, _ = frame.shape()

        # Region of Interest
        roi = frame[240:850, 320:1600]

        if ret == True:

            # 1. Object detection
            mask = object_detector.apply(roi)
            # Remove shadows
            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            detections = []

            for cnt in contours:

                # Calculate Area and remove elements
                area = cv2.contourArea(cnt)
                
                if 450 < area < 1250:
                    # cv2.drawContours(roi, [cnt], -1, (0,255,0), 1)
                    # Draw a rectangle
                    x, y, w, h = cv2.boundingRect(cnt)

                    detections.append([x, y, w, h])

            # 2. Object tracking
            boxes_ids = tracker.update(detections)

            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0 ,0), 1)
                cv2.rectangle(roi, (x,y), (x + w, y + h), (0,255,0), 2)

            cv2.imshow("ROI", roi)
            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)

            key = cv2.waitKey(30)
            if (key == 27):
                break
        else:
            break


    cap.release()
    cv2.destroyAllWindows()

if  __name__ == '__main__':
    main()