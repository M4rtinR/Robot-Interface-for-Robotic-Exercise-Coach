#!/usr/bin/env python
# coding: utf-8
import time
import sys

import numpy as np
from PIL import Image

import qi
import vision_definitions
import cv2 as cv
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask('output_api')
api = Api(app)

robot_ip = "192.168.1.5"
# robot_ip = "localhost"
port = 9559
# port = 45653
memory = None
ReactToTouch = None
questionCount = 0
expectingTouch = False

class Action(Resource):
    def post(self):
        if request.is_json:
            print("request is json")
            content = request.get_json()
            '''try:
                tabletService = ALProxy("ALTabletService", "192.168.1.37", 9559)

                # Ensure that the tablet wifi is enable
                tabletService.enableWifi()

                # Play a video from the web and display the player
                # If you want to play a local video, the ip of the robot from the tablet is 198.18.0.1
                # Put the video in the HTML folder of your behavior
                # "http://198.18.0.1/apps/my_behavior/my_video.mp4"
                print("displaying image")
                tabletService.showImage("http://127.0.0.1/img/HowDidThatFeelOptions.png")

                print("sleep")
                time.sleep(5)

                # Hide the web view
                tabletService.hideImage()
            except Exception as e:
                print("Error was: ", e)'''
            motion_service = ALProxy("ALMotion", robot_ip, port)

            try:
                # tabletService = ALProxy("ALTabletService", "192.168.1.37", 9559)
                tabletService = ALProxy("ALTabletService", robot_ip, port)
                # Ensure that the tablet wifi is enable
                tabletService.enableWifi()
                # Show the initial screen on tablet
                print("Showing tablet view")
                tabletService.playVideo("VideoFiles/TabletopCircles.mp4")
                #tabletService.showWebview("192.168.1.207:8000/display")
            except Exception as e:
                print("Error was: ", e)

            if 'start' in content:
                posture_service = ALProxy("ALRobotPosture", robot_ip, port)

                # Wake up robot
                motion_service.wakeUp()

                # Send robot to Stand
                posture_service.goToPosture("StandInit", 0.5)

                # Show the initial screen on tablet
                tabletService.showWebview("192.168.1.207:8000/display")

            elif 'stop' in content:
                ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                # ttsAnimated.setParameter("speed", 100)
                configuration = {"bodyLanguageMode": "contextual"}
                ttsAnimated.say("That's 10, you can stop there.", configuration)
            else:
                action = content['utterance']
                print(action)
                if 'demo' in content:
                    tts = ALProxy("ALTextToSpeech", robot_ip, port)
                    # tts.setParameter("speed", 100)
                    tts.post.say(str(action))
                    demoString = str(content['demo'])

                    if demoString == "racket_up_pos":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_up_pos_left":
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-1.09, -2.09, -0.01, -0.15, 1.55, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_up_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.32, 2.08, 0.01, 0.93, -0.39, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_up_neg_left":
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-0.32, -2.08, -0.01, 0.93, 0.39, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_face_pos":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                        speedLists = 0.3
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.5)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_face_pos_left":
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.55, 0.01]
                        speedLists = 0.3
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.5)
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.03, 0.01]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_face_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.85, -0.03]
                        speedLists = 0.3
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.5)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.13, -0.03]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_face_neg_left":
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.85, 0.03]
                        speedLists = 0.3
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.5)
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.13, 0.03]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "follow_through_pos":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.52, 1.68, 0.01, 0.62, -0.12, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.3)
                        # motion_service.post.moveTo(0, 0, 0.79)
                        names.append("HipPitch")
                        angleLists = [0.02, 1.68, 0.01, 0.62, -1.00, -0.02, -0.08]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "follow_through_pos_left":
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-0.52, -1.68, -0.01, 0.62, 0.12, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.3)
                        # motion_service.post.moveTo(0, 0, 0.79)
                        names.append("HipPitch")
                        angleLists = [-0.02, -1.68, -0.01, 0.62, 1.00, 0.02, -0.08]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "follow_through_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.52, 1.68, 0.01, 0.62, -0.12, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.3)
                        angleLists = [0.31, 1.68, 0.01, 0.62, -0.27, -0.02]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "follow_through_neg_left":
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-0.52, -1.68, -0.01, 0.62, 0.12, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.3)
                        angleLists = [-0.31, -1.68, -0.01, 0.62, 0.27, 0.02]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "forehand_drive_pos":
                        motion_service.post.moveTo(0, 0, -0.79)
                        time.sleep(2.0)
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, 1.58)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.23, -0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.31, 1.68, 0.01, 0.29, -0.01, -0.02]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(1.0)
                        motion_service.post.moveTo(0, 0, -0.79)
                    elif demoString == "forehand_drive_pos_left":
                        motion_service.post.moveTo(0, 0, 0.79)
                        time.sleep(2.0)
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-1.09, -2.09, -0.01, 0.15, 1.55, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, -1.58)
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.55, 0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.23, 0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.31, -1.68, -0.01, 0.29, 0.01, 0.02]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(1.0)
                        motion_service.post.moveTo(0, 0, 0.79)
                    elif demoString == "forehand_drive_neg_left":
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-1.09, -2.09, -0.01, 0.15, 1.55, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.23, 0.01]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "forehand_drive_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.23, -0.01]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "backhand_drive_pos":
                        motion_service.post.moveTo(0, 0, 1.58)
                        time.sleep(2.0)
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.75, 2.08, 0.01, -0.21, -0.02, -0.26]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, -1.58)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.13, -0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.85, -0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        names.append("HipPitch")
                        angleLists = [0.02, 1.68, 0.01, 0.62, -1.00, -0.02, -0.08]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "backhand_drive_pos_left":
                        motion_service.post.moveTo(0, 0, -1.58)
                        time.sleep(2.0)
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-0.75, -2.08, -0.01, -0.21, 0.02, 0.26]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, 1.58)
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.13, 0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.85, 0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        names.append("HipPitch")
                        angleLists = [-0.02, -1.68, -0.01, 0.62, 1.00, 0.02, -0.08]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "backhand_drive_neg":
                        motion_service.post.moveTo(0, 0, 0.79)
                        time.sleep(2.0)
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.45, 2.08, 0.01, 0.40, -0.02, -0.26]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, -0.79)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.13, -0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.85, -0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "backhand_drive_neg_left":
                        motion_service.post.moveTo(0, 0, -0.79)
                        time.sleep(2.0)
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-0.45, -2.08, -0.01, 0.40, 0.02, 0.26]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, 0.79)
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.13, 0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.85, 0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "drop_pos":
                        motion_service.post.moveTo(0, 0, -0.79)
                        time.sleep(2.0)
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, 1.58)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.23, -0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.31, 1.68, 0.01, 0.29, -0.01, -0.02]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(1.0)
                        motion_service.post.moveTo(0, 0, -0.79)
                    elif demoString == "drop_pos_left":
                        motion_service.post.moveTo(0, 0, 0.79)
                        time.sleep(2.0)
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-1.09, -2.09, -0.01, 0.15, 1.55, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, -1.58)
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.55, 0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.23, 0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.31, -1.68, -0.01, 0.29, 0.01, 0.02]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(1.0)
                        motion_service.post.moveTo(0, 0, 0.79)
                    elif demoString == "drop_neg":
                        motion_service.post.moveTo(0, 0, -0.79)
                        time.sleep(2.0)
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, 1.58)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.85, -0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.13, -0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(1.0)
                        motion_service.post.moveTo(0, 0, -0.79)
                    elif demoString == "drop_neg_left":
                        motion_service.post.moveTo(0, 0, 0.79)
                        time.sleep(2.0)
                        names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [-1.09, -2.09, -0.01, 0.15, 1.55, 0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, -1.58)
                        angleLists = [-0.53, -2.07, -0.01, 0.93, 0.55, 0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.85, 0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [-0.53, -0.75, -0.01, 0.93, 0.13, 0.03]
                        speedLists = 0.15
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(1.0)
                        motion_service.post.moveTo(0, 0, 0.79)
                    elif demoString == "reset":
                        motion_service.post.moveTo(0, 0, 0.79)
                else:
                    if 'question' in content:
                        ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                        # ttsAnimated.setParameter("speed", 100)
                        configuration = {"bodyLanguageMode": "contextual"}
                        if content['question'] == 'GoodBad':
                            print("GoodBad question detected")
                            global expectingTouch
                            expectingTouch = True
                            ttsAnimated.say(str(action), configuration)
                            names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                                     "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                            angleLists = [0.98, 1.69, 0.01, 0.79, -0.09, -0.03, -0.98, -1.69, 0.01, 0.79, 0.09, 0.03]
                            speedLists = 0.3
                            motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                            global ReactToTouch
                            global questionCount
                            if questionCount == 0:
                                ReactToTouch = ReactToTouch("ReactToTouch")

                            questionCount += 1

                            time.sleep(5.0)
                            expectingTouch = False
                        else:
                            print("Concurrent question detected")
                            ttsAnimated.say(str(action), configuration)
                    else:
                        ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                        # ttsAnimated.setParameter("speed", 100)
                        configuration = {"bodyLanguageMode": "contextual"}
                        # Show the initial screen on tablet
                        tabletService.showWebview("192.168.1.207:8000/display")
                        ttsAnimated.say(str(action), configuration)
                # TODO: Deal with videos
                return {'completed': 1}, 200
        else:
            print("ERROR: request is not json")
            return {'message': 'Request not json'}, 500


class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        print "initialising"
        ALModule.__init__(self, name)

        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("TouchChanged",
                                "ReactToTouch",
                                "onTouched")

    def onTouched(self, strVarName, value):
        print("onTouched")
        global expectingTouch
        if not expectingTouch:
            return
        memory.unsubscribeToEvent("TouchChanged", "ReactToTouch")

        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])

        self.say(touched_bodies)

        memory.subscribeToEvent("TouchChanged",
                                "ReactToTouch",
                                "onTouched")

    def say(self, bodies):
        if (bodies == []):
            return

        ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
        ttsAnimated.setParameter("speed", 100)
        configuration = {"bodyLanguageMode": "contextual"}
        if "LArm" in bodies or "RArm" in bodies or "LHand/Touch/Back" in bodies or "RHand/Touch/Back" in bodies:
            ttsAnimated.say("Great!", configuration)
        else:
            ttsAnimated.say("OK, don't worry. We can keep improving together!")

api.add_resource(Action, '/output')

def test(session):
    ''''"""
       This is just an example script that shows how images can be accessed
       through ALVideoDevice in Python.
       Nothing interesting is done with the images in this example.
       """
    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")

    # Register a Generic Video Module
    resolution = vision_definitions.kQQVGA
    colorSpace = vision_definitions.kYUVColorSpace
    fps = 20

    nameId = video_service.subscribe("python_GVM", resolution, colorSpace, fps)

    print 'getting images in remote'
    for i in range(0, 20):
        print "getting image " + str(i)
        video_service.getImageRemote(nameId)
        time.sleep(0.05)

    video_service.unsubscribe(nameId)'''

    '''"""
        First get an image, then show it on the screen with PIL.
        """
    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")
    resolution = 2  # VGA
    colorSpace = 11  # RGB

    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    pepperImage = video_service.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print "acquisition delay ", t1 - t0

    video_service.unsubscribe(videoClient)

    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = pepperImage[0]
    imageHeight = pepperImage[1]
    array = pepperImage[6]
    image_string = str(bytearray(array))

    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

    # Save the image.
    im.save("camImage.png", "PNG")

    im.show()'''

    '''videoDevice = session.service("ALVideoDevice")

    # subscribe top camera
    AL_kTopCamera = 0
    AL_kQVGA = 1  # 320x240
    AL_kBGRColorSpace = 13
    captureDevice = videoDevice.subscribeCamera(
        "test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
    resolution = 2  # VGA
    colorSpace = 11  # RGB
    # create image
    width = 320
    height = 240
    image = np.zeros((height, width, 3), np.uint8)

    # videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)
    while True:

        # get image
        device = videoDevice.getImageRemote(captureDevice)

        if device == None:
            print 'cannot capture.'
        elif device[6] == None:
            print 'no image data string.'
        else:

            # translate value to mat
            values = device[6]
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3

            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            # show image
            cv.imshow("pepper-top-camera-320x240", gray)

        # exit by [ESC]
        if cv.waitKey(33) == 27:
            break'''


    '''cap = cv.VideoCapture(session)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()'''

    '''
    # Get the service ALTabletService.
    tabletService = session.service("ALTabletService")

    try:
        # Display a local web page located in boot-config/html folder
        # The ip of the robot from the tablet is 198.18.0.1
        # tabletService.showWebview("http://doc.aldebaran.com/2-4/naoqi/core/altabletservice-api.html?highlight=getwifi")
        tabletService.showWebview("https://www.macs.hw.ac.uk/~mkr30/Test.html")
        # tabletService.showWebview("https: // www.macs.hw.ac.uk / ~mkr30 / TowelSlide - rotation - 1.png.webp")

    except Exception, e:
        print "Error was:", e

    '''
    tts = ALProxy("ALTextToSpeech", robot_ip, port)
    configuration = {"bodyLanguageMode": "contextual"}
    tts.say("Hi, welcome to today's session.")
    tts.setParameter("speed", 50)
    tts.say("Hi, welcome to today's session.")

if __name__ == "__main__":
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
                        "0.0.0.0",  # listen to anyone
                        0,  # find a free port and use it
                        robot_ip,  # parent broker IP
                        port)  # parent broker port

    '''session = qi.Session()
    try:
        session.connect("tcp://" + robot_ip + ":" + str(port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + robot_ip + "\" on port " + str(port) + ".\nPlease check your script arguments. Run with -h option for help.")
        sys.exit(1)
    test(session)
    '''

    app.run(host='0.0.0.0', port=4999)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)
