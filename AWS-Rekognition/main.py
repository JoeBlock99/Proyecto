'''
        Proyecto IA

            Main

Creado por:

Juan Fernando De Leon Quezada   17822
Jose Gabriel Block Staackman    18935
'''
import csv
import cv2
import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
import time
import json
import sys
from imgDetect import img_detect_start_model, img_detect, img_detect_stop_model, display_image
from pointsEngine import ballsContact, railContact

access_key_id = ''
secret_access_key = ''

with open('new_user_credentials_1.csv', 'r') as input:
        next(input)
        reader = csv.reader(input)
        for line in reader:
            access_key_id = line[2]
            secret_access_key = line[3]

def frame_into_bytes(frame):
    return cv2.imencode('.jpg', frame)[1].tobytes()

if __name__ == "__main__":

    # display_image()

    # Start Model
    # img_detect_start_model(access_key_id, secret_access_key)

    
    # Run detection

    # #Opens the Video file
    cap= cv2.VideoCapture('./Videos/3-CUSHION-4.mov')
    
    # Frame Counter
    i=0

    # Rail Touches Counter
    railCtr = 0

    # Verify if a rail is touched
    touched_rail = False

    # Verify if red ball is touched
    red_ball_touched = False
    # Verify if opponent;s ball is touched
    opponent_ball_touched = False
    
    # These is to keep track of balls
    red_ball_previous_frame = None
    players_ball_previous_frame = None
    opponent_ball_previous_frame = None

    # Player in turn Ball
    playersBall = "White-Ball"

    # Players Ball Info
    players_ball_previous_frame_info = (None, [])

    show_image = False

    # Iterate frames    
    while(cap.isOpened()):
        
        # Read one frame
        ret, frame = cap.read()
        
        if ret == False:
            break

        # if 200 <= i <= 205:
        # Frame Dimesions
        height, width, _ = frame.shape
        frameDim = (height, width)
        
        print("\nFrame #", i)
        print("----------------")
        
        # Turn frame into bytes
        source_bytes = frame_into_bytes(frame)
        
        # Detect Labels in scene
        labels_detected = img_detect(source_bytes, access_key_id, secret_access_key, frameDim)

        # Analize Scene

        # Verify if players ball is in contact with any rail
        players_ball_new_frame, rail_contact_ctr, rails_touched_new_frame = railContact(labels_detected, playersBall, frameDim, players_ball_previous_frame_info)

        if players_ball_new_frame:
            players_ball_previous_frame_info = (players_ball_new_frame, rails_touched_new_frame)
            if rail_contact_ctr > 0:
                railCtr += 1
                show_image = True

        # Extract Balls Positions, get if balls are in contact
        player_ball_current_frame, opponent_ball_current_frame, red_ball_current_frame, touch_between_balls = ballsContact(labels_detected, playersBall, frameDim)

        # If balls are in contact
        if type(touch_between_balls) is tuple:
            if touch_between_balls[1]:
                if (touch_between_balls[0] == "player_red_touch"):
                    red_ball_touched = True
                    show_image = True
                if (touch_between_balls[0] == "player_opponent_touch"):
                    opponent_ball_touched = True
                    show_image = True
        
        if show_image:
            # Save reference frame
            cv2.imwrite('./Img/3-CUSHION-'+str(i)+'.jpg',frame)
            # Display Frame with bounding boxes
            display_image('./Img/3-CUSHION-'+str(i)+'.jpg', labels_detected)
            show_image = False

        # Print Frame analysis results
        print("Rail touches", railCtr)
        print("Contact with red ball: ", red_ball_touched)
        print("Contact with opponent's ball: ", opponent_ball_touched)
        
        # Next Frame
        i+=1

    cap.release()
    cv2.destroyAllWindows()

    # Stop Model
    # img_detect_stop_model(access_key_id, secret_access_key)