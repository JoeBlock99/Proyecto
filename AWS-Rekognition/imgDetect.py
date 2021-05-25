'''
        Proyecto IA

Img Detect

Creado por:

Juan Fernando De Leon Quezada   17822
Jose Gabriel Block Staackman    18935
'''

import csv
import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
import time
import json
import sys

def start_model(access_key_id, secret_access_key, project_arn, model_arn, version_name, min_inference_units):
    '''Start AWS Rekognition Model'''

    client=boto3.client('rekognition', region_name='us-east-2', aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key)

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response=client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        #Get the running status
        describe_response=client.describe_project_versions(ProjectArn=project_arn,
            VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage']) 
    except Exception as e:
        print(e)
        
    print('Done...')
    
def display_image(img_path, labels):
    '''Display Image with bounding boxes'''

    image=Image.open(img_path)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)
    
    # # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for: ' + img_path)
    for customLabel in labels:
        if customLabel['Name'] != "Pool-Table":
            print('\nLabel ' + str(customLabel['Name']))
            print('Confidence ' + str(customLabel['Confidence']))
            if 'Geometry' in customLabel:
                box = customLabel['Geometry']['BoundingBox']
                left = imgWidth * box['Left']
                top = imgHeight * box['Top']
                width = imgWidth * box['Width']
                height = imgHeight * box['Height']

                fnt = ImageFont.truetype('/Library/Fonts/arial.ttf', 50)
                draw.text((left,top), customLabel['Name'], fill='#00d400', font=fnt)

                print('Left: ' + '{0:.0f}'.format(left))
                print('Top: ' + '{0:.0f}'.format(top))
                print('Label Width: ' + "{0:.0f}".format(width))
                print('Label Height: ' + "{0:.0f}".format(height))

                points = (
                    (left,top),
                    (left + width, top),
                    (left + width, top + height),
                    (left , top + height),
                    (left, top))
                draw.line(points, fill='#00d400', width=5)

    # Display Img
    image.show()
    # Save Img
    filename = img_path.split(".")[1]
    image.save("." + filename + "-PROCESSED.jpg")

def show_custom_labels(source_bytes, access_key_id, secret_access_key, model, min_confidence):
    '''Detect custom lables in frame'''

    client=boto3.client('rekognition', region_name='us-east-2', aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key)

    #Call DetectCustomLabels
    response = client.detect_custom_labels(Image={'Bytes': source_bytes},
        MinConfidence=min_confidence,
        ProjectVersionArn=model,
        MaxResults=4)
    
    return response['CustomLabels']

def stop_model(access_key_id, secret_access_key, model_arn):
    '''Stop AWS Rekognition Model'''

    client=boto3.client('rekognition', region_name='us-east-2', aws_access_key_id = access_key_id, aws_secret_access_key = secret_access_key)

    print('Stopping model:' + model_arn)

    #Stop the model
    try:
        response=client.stop_project_version(ProjectVersionArn=model_arn)
        status=response['Status']
        print ('Status: ' + status)
    except Exception as e:  
        print(e)  

    print('Done...')

def img_detect(source_bytes, access_key_id, secret_access_key, frameDim):
    '''Detect all labels in frame'''
    model='arn:aws:rekognition:us-east-2:064950492112:project/3-CUSHION-CAROM-BILLIARD-AI-PROJECT/version/3-CUSHION-CAROM-BILLIARD-AI-PROJECT.2021-05-23T20.03.55/1621821835434'
    min_confidence=65

    labels_detected=show_custom_labels(source_bytes, access_key_id, secret_access_key, model, min_confidence)
    print("Custom labels detected: " + str(len(labels_detected)))

    return labels_detected

def img_detect_start_model(access_key_id, secret_access_key):
    '''Start AWS Model'''

    project_arn='arn:aws:rekognition:us-east-2:064950492112:project/3-CUSHION-CAROM-BILLIARD-AI-PROJECT/1621696163384'
    model_arn='arn:aws:rekognition:us-east-2:064950492112:project/3-CUSHION-CAROM-BILLIARD-AI-PROJECT/version/3-CUSHION-CAROM-BILLIARD-AI-PROJECT.2021-05-23T20.03.55/1621821835434'

    min_inference_units=1 
    version_name='3-CUSHION-CAROM-BILLIARD-AI-PROJECT.2021-05-23T20.03.55'
    
    start_model(access_key_id, secret_access_key, project_arn, model_arn, version_name, min_inference_units)

def img_detect_stop_model(access_key_id, secret_access_key):
    '''Stop AWS Model'''

    model_arn='arn:aws:rekognition:us-east-2:064950492112:project/3-CUSHION-CAROM-BILLIARD-AI-PROJECT/version/3-CUSHION-CAROM-BILLIARD-AI-PROJECT.2021-05-23T20.03.55/1621821835434'
    stop_model(access_key_id, secret_access_key, model_arn)