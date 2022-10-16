#!/usr/bin/env python
# coding: utf-8
import time
import sys

import numpy as np
import requests
from PIL import Image

import qi
import vision_definitions
import cv2 as cv
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime

app = Flask('output_api')
api = Api(app)

# ITT_Pepper:
robot_ip = "192.168.1.5"
port = 9559

# Dusty in HRI_Lab_5G
# robot_ip = "192.168.1.53"
# port = 9559

# Simulation:
# robot_ip = "localhost"
# port = 36729

# Phone hotspot:
# robot_ip = "192.168.43.57"
# port = 9559

# Post address for controller api.
post_address = "http://192.168.1.207:5000/cue"

memory = None
ReactToTouch = None
questionCount = 0
ReactToTouch_FirstTimeQuestion = None
questionCount_FirstTimeQuestion = 0
expectingTouch = False
goodBadQuestion = False
pause = 0
remembered_content = None
previous_content = None

class Action(Resource):
    def post(self):
        global pause
        global remembered_content
        global previous_content
        if request.is_json:
            print("request is json")
            content = request.get_json()
            if pause == 1:
                if 'pause' in content:  # User has selected stop button so stop session until we get more info.
                    if content['pause'] == '0':
                        pause = 0
                        if 'stop' in content:
                            remembered_content = None
                        elif remembered_content is not None:
                            self._display(remembered_content)
                else:
                    remembered_content = content
            else:
                if 'repeat' in content:
                    self._display(previous_content)
                else:
                    self._display(content)

        else:
            print("ERROR: request is not json")
            return {'message': 'Request not json'}, 500

    def _display(self, content):
        global pause
        global previous_content
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
            '''print("Showing image")
            tabletService.showWebview("http://192.18.0.1/apps/boot_config/preloading_dialog.html")
            time.sleep(5.0)
            # Show the initial screen on tablet
            print("Showing tablet view")
            tabletService.playVideo("http://192.18.0.1/img/help_charger.png")'''
            # tabletService.showWebview("192.168.1.207:8000/display")
        except Exception as e:
            print("Error was: ", e)

        if 'start' in content:
            posture_service = ALProxy("ALRobotPosture", robot_ip, port)

            # Wake up robot
            motion_service.wakeUp()

            # Send robot to Stand
            posture_service.goToPosture("StandInit", 0.5)

            # Show the initial screen on tablet
            # tabletService.showWebview("192.168.1.207:8000/display")

        elif 'stop' in content:
            # ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
            tts = ALProxy("ALTextToSpeech", robot_ip, port)
            tts.setParameter("speed", 90)
            # configuration = {"bodyLanguageMode": "contextual"}
            tts.say("OK, you can stop there.")
        elif 'pause' in content:  # User has selected stop button so stop session until we get more info.
            pause = 1
            tts = ALProxy("ALTextToSpeech", robot_ip, port)
            tts.setParameter("speed", 90)
            tts.post.say("OK, would you like to stop the whole session or just this exercise set?")
            tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
        elif 'silence' in content:
            tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
        else:
            action = content['utterance']
            print(action)
            if 'demo' in content:
                tts = ALProxy("ALTextToSpeech", robot_ip, port)
                tts.setParameter("speed", 90)
                tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
                tts.post.say(str(action))
                demoString = str(content['demo'])

                if demoString == "racketPreparation_high":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "racketPreparation_high_left":
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.09, -2.09, -0.01, -0.15, 1.55, 0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "racketPreparation_low":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.32, 2.08, 0.01, 0.93, -0.39, -0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "racketPreparation_low_left":
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.32, -2.08, -0.01, 0.93, 0.39, 0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_racketPreparation_high":
                    print('demoString == "backhand_racketPreparation_high":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.75, 2.08, 0.01, -0.21, -0.02, -0.26]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_racketPreparation_high_left":
                    print('demoString == "backhand_racketPreparation_high_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.75, -2.08, -0.01, -0.21, 0.02, 0.26]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_racketPreparation_low":
                    print('demoString == "backhand_racketPreparation_low":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_racketPreparation_low_left":
                    print('demoString == "backhand_racketPreparation_low_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.28, -1.20, -0.01, 0.22, 0.01, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_open_pos":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_open_pos_left":
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.53, -2.07, -0.01, 0.93, 0.55, 0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    angleLists = [-0.53, -2.07, -0.01, 0.93, 0.03, 0.01]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_open_neg":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.53, 0.75, 0.01, 0.93, -0.85, -0.03]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    angleLists = [0.53, 0.75, 0.01, 0.93, -0.13, -0.03]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_open_neg_left":
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.53, -0.75, -0.01, 0.93, 0.85, 0.03]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    angleLists = [-0.53, -0.75, -0.01, 0.93, 0.13, 0.03]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_open_pos":
                    print('demoString == "backhand_impactCutAngle_open_pos":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.74, 1.19, 0.01, 0.38, -0.39, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_open_pos_left":
                    print('demoString == "backhand_impactCutAngle_open_pos_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.74, -1.19, -0.01, 0.38, 0.39, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.2, -1.38, -0.01, 0.59, 0.75, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_open_neg":
                    print('demoString == "backhand_impactCutAngle_open_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.77, 1.72, 0.01, 0.56, -0.01, 0.38]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.8, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_open_neg_left":
                    print('demoString == "backhand_impactCutAngle_open_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.77, -1.72, -0.01, 0.56, 0.01, -0.38]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.8, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_closed_pos":
                    print('demoString == "impactCutAngle_closed_pos":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.36, 1.80, 0.01, 0.83, -0.01, 0.38]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.8, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_closed_pos_left":
                    print('demoString == "impactCutAngle_closed_pos_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.36, -1.80, -0.01, 0.83, 0.01, -0.38]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.8, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_closed_neg":
                    print('demoString == "impactCutAngle_closed_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.36, 2.03, 0.01, 0.83, -0.78, 0.31]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.03, 0.01, 0.83, -0.06, 0.72]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impactCutAngle_closed_neg_left":
                    print('demoString == "impactCutAngle_closed_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.36, -2.03, -0.01, 0.83, 0.78, -0.31]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.03, -0.01, 0.83, 0.06, -0.72]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_closed_pos":
                    print('demoString == "backhand_impactCutAngle_closed_pos":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.77, 1.19, 0.01, 0.56, -0.08, 0.38]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 1.64, 0.01, 0.8, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_closed_pos_left":
                    print('demoString == "backhand_impactCutAngle_closed_pos_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.77, -1.19, -0.01, 0.56, 0.08, -0.38]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -1.64, -0.01, 0.8, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_closed_neg":
                    print('demoString == "backhand_impactCutAngle_closed_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.77, 0.51, 0.01, 0.33, -0.17, -0.06]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.23, 0.72, 0.01, 0.54, -0.77, -0.49]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impactCutAngle_closed_neg_left":
                    print('demoString == "backhand_impactCutAngle_closed_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.77, -0.51, -0.01, 0.33, 0.17, 0.06]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.23, -0.72, -0.01, 0.54, 0.77, 0.49]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "followThroughTime_long":
                    print("followThroughTime_long")
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.52, 1.68, 0.01, 0.62, -0.12, -0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                    names.append("HipPitch")
                    angleLists = [0.02, 1.68, 0.01, 0.62, -1.00, -0.02, -0.08]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "followThroughTime_long_left":
                    print("followThroughTime_long_left")
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.52, -1.68, -0.01, 0.62, 0.12, 0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    names.append("HipPitch")
                    angleLists = [-0.02, -1.68, -0.01, 0.62, 1.00, 0.02, -0.08]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "followThroughTime_short":
                    print("followThroughTime_short")
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.52, 1.68, 0.01, 0.62, -0.12, -0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.31, 1.68, 0.01, 0.62, -0.27, -0.02]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "followThroughTime_short_left":
                    print("followThroughTime_short_left")
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.52, -1.68, -0.01, 0.62, 0.12, 0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.31, -1.68, -0.01, 0.62, 0.27, 0.02]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_followThroughTime_long":
                    print('demoString == "backhand_followThroughTime_long":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    motion_service.post.moveTo(0, 0, -0.79)
                    angleLists = [0.83, 1.22, 0.01, 0.56, -0.14, -0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [0.62, 1.22, 0.01, 0.64, -0.64, -0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.17, 0.80, 0.01, -0.22, -1.15, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "backhand_followThroughTime_long_left":
                    print('demoString == "backhand_followThroughTime_long_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    motion_service.post.moveTo(0, 0, 0.79)
                    angleLists = [-0.83, -1.22, -0.01, 0.56, 0.14, 0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [-0.62, -1.22, -0.01, 0.64, 0.64, 0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.17, -0.80, -0.01, -0.22, 1.15, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "backhand_followThroughTime_short":
                    print('demoString == "backhand_followThroughTime_short":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    motion_service.post.moveTo(0, 0, -0.79)
                    angleLists = [0.83, 1.22, 0.01, 0.56, -0.14, -0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    angleLists = [0.86, 1.59, 0.01, 0.69, -0.32, -0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_followThroughTime_short_left":
                    print('demoString == "backhand_followThroughTime_short_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    motion_service.post.moveTo(0, 0, 0.79)
                    angleLists = [-0.83, -1.22, 0.01, 0.56, 0.14, 0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                    angleLists = [-0.86, -1.59, -0.01, 0.69, 0.32, 0.60]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impact_speed_fast":
                    print('demoString == "impact_speed_fast":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                    speedLists = 0.5
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impact_speed_fast_left":
                    print('demoString == "impact_speed_fast_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                    speedLists = 0.5
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impact_speed_slow":
                    print('demoString == "impact_speed_slow":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "impact_speed_slow_left":
                    print('demoString == "impact_speed_slow_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impact_speed_fast":
                    print('demoString == "backhand_impact_speed_fast:')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.74, 1.19, 0.01, 0.38, -0.39, -0.61]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61]
                    speedLists = 0.5
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impact_speed_fast_left":
                    print('demoString == "backhand_impact_speed_fast_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [0.74, 1.19, 0.01, 0.38, -0.39, -0.61]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61]
                    speedLists = 0.5
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impact_speed_slow":
                    print('demoString == "backhand_impact_speed_slow":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.74, 1.19, 0.01, 0.38, -0.39, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_impact_speed_slow_left":
                    print('demoString == "backhand_impact_speed_slow_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [0.74, 1.19, 0.01, 0.38, -0.39, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "approachTiming_pos":
                    print('demoString == "approachTiming_pos":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "approachTiming_pos_left":
                    print('demoString == "approachTiming_pos_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.53, -2.07, -0.01, 0.93, 0.55, 0.01]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.53, -2.07, -0.01, 0.93, 0.03, 0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    angleLists = [-0.53, -2.07, -0.01, 0.93, 0.55, 0.01]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.53, -2.07, -0.01, 0.93, 0.03, 0.01]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "approachTiming_infront":
                    print('demoString == "approachTiming_infront":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.52, 1.68, 0.01, 0.62, -0.12, -0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                    names.append("HipPitch")
                    angleLists = [0.02, 1.68, 0.01, 0.62, -1.00, -0.02, -0.08]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(1.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.52, 1.68, 0.01, 0.62, -0.12, -0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                    names.append("HipPitch")
                    angleLists = [0.02, 1.68, 0.01, 0.62, -1.00, -0.02, -0.08]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "approachTiming_infront_left":
                    print('demoString == "approachTiming_infront_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.52, -1.68, -0.01, 0.62, 0.12, 0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    names.append("HipPitch")
                    angleLists = [-0.02, -1.68, -0.01, 0.62, 1.00, 0.02, -0.08]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(1.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.52, -1.68, -0.01, 0.62, 0.12, 0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    names.append("HipPitch")
                    angleLists = [-0.02, -1.68, -0.01, 0.62, 1.00, 0.02, -0.08]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "approachTiming_behind":
                    print('demoString == "approachTiming_behind":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    names.append("HipPitch")
                    angleLists = [0.83, 0.93, 0.01, 1.46, -0.9, 1.34, -0.18]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    names.append("HipPitch")
                    angleLists = [0.83, 0.93, 0.01, 1.46, -0.9, 1.34, -0.18]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "approachTiming_behind_left":
                    print('demoString == "approachTiming_behind_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.09, -2.09, 0.01, 0.15, 1.55, 0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    names.append("HipPitch")
                    angleLists = [-0.83, -0.93, 0.01, 1.46, 0.9, -1.34, 0.18]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.09, -2.09, 0.01, 0.15, 1.55, 0.02]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    names.append("HipPitch")
                    angleLists = [-0.83, -0.93, 0.01, 1.46, 0.9, -1.34, 0.18]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_approachTiming_pos":
                    print('demoString == "backhand_approachTiming_pos":')
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                    angleLists = [0.74, 1.19, 0.01, 0.38, -0.39, -0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(1.0)
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "backhand_approachTiming_pos_left":
                    print('demoString == "backhand_approachTiming_pos_left":')
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.28, -1.20, -0.01, 0.26, 0.01, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    angleLists = [-0.74, -1.19, -0.01, 0.38, 0.39, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(1.0)
                    angleLists = [-1.28, -1.20, -0.01, 0.26, 0.01, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    angleLists = [-0.74, -1.19, -0.01, 0.38, 0.39, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                elif demoString == "backhand_approachTiming_infront_left":
                    print('demoString == "backhand_approachTiming_infront_left":')
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.28, -1.20, -0.01, 0.26, 0.01, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(0.5)
                    names.append("HipPitch")
                    names.append("HipRoll")
                    angleLists = [-0.2, -1.38, -0.01, 0.59, 0.75, 0.61, -0.16, 0.09]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.28, -1.20, -0.01, 0.26, 0.01, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(0.5)
                    names.append("HipPitch")
                    names.append("HipRoll")
                    angleLists = [-0.2, -1.38, -0.01, 0.59, 0.75, 0.61, -0.16, 0.09]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "backhand_approachTiming_infront":
                    print('demoString == "backhand_approachTiming_infront":')
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(0.5)
                    names.append("HipPitch")
                    names.append("HipRoll")
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61, -0.16, -0.09]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(0.5)
                    names.append("HipPitch")
                    names.append("HipRoll")
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61, -0.16, -0.09]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "backhand_approachTiming_behind":
                    print('demoString == "backhand_approachTiming_behind":')
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(0.5)
                    names.append("HipRoll")
                    angleLists = [0.01, 2.08, 0.01, 1.14, -0.01, -0.56, 0.1]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(0.5)
                    names.append("HipRoll")
                    angleLists = [0.01, 2.08, 0.01, 1.14, -0.01, -0.56, 0.1]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "backhand_approachTiming_behind_left":
                    print('demoString == "backhand_approachTiming_behind_left":')
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.28, -1.20, -0.01, 0.26, 0.01, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(0.5)
                    names.append("HipRoll")
                    angleLists = [-0.01, -2.08, -0.01, 1.14, 0.01, 0.56, -0.1]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.28, -1.20, -0.01, 0.26, 0.01, 0.61]
                    speedLists = 0.4
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(0.5)
                    names.append("HipRoll")
                    angleLists = [-0.01, -2.08, -0.01, 1.14, 0.01, 0.56, -0.1]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(1.5)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "followThroughRoll_over":
                    print('demoString == "followThroughRoll_over":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.22, 0.01, 0.56, -0.13, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "followThroughRoll_over_left":
                    print('demoString == "followThroughRoll_over_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.37, -2.08, -0.01, 0.8, 0.85, -0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.9, -1.22, -0.01, 0.56, 0.13, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "followThroughRoll_under":
                    print('demoString == "followThroughRoll_under":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.51, 0.01, 0.56, -0.01, 1.82]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "followThroughRoll_under_left":
                    print('demoString == "followThroughRoll_under_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.37, -2.08, -0.01, 0.8, 0.85, -0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.9, -1.51, -0.01, 0.56, 0.01, -1.82]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_followThroughRoll_over":
                    print('demoString == "backhand_followThroughRoll_over":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.9, 1.23, 0.01, 0.57, -0.13, -0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.80, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_followThroughRoll_over_left":
                    print('demoString == "backhand_followThroughRoll_over_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.80, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_followThroughRoll_under":
                    print('demoString == "backhand_followThroughRoll_under":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.9, 1.23, 0.01, 0.57, -0.13, -0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.13, 0.35, 0.01, 0.54, -0.85, -0.49]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_followThroughRoll_under_left":
                    print('demoString == "backhand_followThroughRoll_under_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.13, -0.35, -0.01, 0.54, 0.85, 0.49]
                    speedLists = 0.2
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
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
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
                elif demoString == "backhand_drop_pos":
                    print('demoString == "backhand_drop_pos":')
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.28, 1.20, 0.01, 0.26, -0.01, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [0.74, 1.19, 0.01, 0.38, -0.39, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.2, 1.38, 0.01, 0.59, -0.75, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_drop_pos_left":
                    print('demoString == "backhand_drop_pos_left":')
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.28, -1.20, -0.01, 0.22, 0.01, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [-0.74, -1.19, -0.01, 0.38, 0.39, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.2, -1.38, -0.01, 0.59, 0.75, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_drop_neg":
                    print('demoString == "backhand_drop_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.22, 0.01, 0.56, -0.13, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_drop_neg_left":
                    print('demoString == "backhand_drop_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.80, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_volley_drop_pos":
                    print('demoString == "forehand_volley_drop_pos":')
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.12, 2.05, 0.01, -0.01, -1.45, -0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [0.67, 1.90, 0.01, -0.01, -0.79, -0.01]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.19, 1.90, 0.01, -0.01, -0.22, -0.01]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "forehand_volley_drop_pos_left":
                    print('demoString == "forehand_volley_drop_pos_left":')
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.12, -2.05, -0.01, -0.01, 1.45, 0.02]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [-0.67, -1.90, -0.01, -0.01, 0.79, 0.01]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.19, -1.90, -0.01, -0.01, 0.22, 0.01]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "forehand_volley_drop_neg":
                    print('demoString == "forehand_volley_drop_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.22, 0.01, 0.56, -0.13, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_volley_drop_neg_left":
                    print('demoString == "forehand_volley_drop_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.37, -2.08, -0.01, 0.8, 0.85, -0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.9, -1.22, -0.01, 0.56, 0.13, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_drop_pos":
                    print('demoString == "backhand_volley_drop_pos":')
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.13, 1.78, 0.01, -1.0, -0.03, -0.05]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [0.6, 1.1, 0.01, -0.75, -0.33, -0.03]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.32, 0.69, 0.01, -0.28, -0.89, -0.03]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_drop_pos_left":
                    print('demoString == "backhand_volley_drop_pos_left":')
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.13, -1.78, -0.01, -1.0, 0.03, 0.05]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [-0.6, -1.1, -0.01, -0.75, 0.33, 0.03]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.32, -0.69, -0.01, -0.28, 0.89, 0.03]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_drop_neg":
                    print('demoString == "backhand_volley_drop_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.9, 1.23, 0.01, 0.57, -0.13, -0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.80, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_drop_neg_left":
                    print('demoString == "backhand_volley_drop_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.80, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_kill_pos":
                    print('demoString == "forehand_kill_pos":')
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.86, 1.51, 0.01, -0.95, -0.49, 0.15]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [0.84, 1.82, 0.01, 0.28, -0.64, 0.72]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.47, 1.48, 0.01, 0.59, -0.01, 0.72]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "forehand_kill_pos_left":
                    print('demoString == "forehand_kill_pos_left":')
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.86, -1.51, -0.01, -0.95, 0.49, -0.15]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [-0.84, -1.82, -0.01, 0.28, 0.64, -0.72]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.47, -1.48, -0.01, 0.59, 0.01, -0.72]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "forehand_kill_neg":
                    print('demoString == "forehand_kill_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.22, 0.01, 0.56, -0.13, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_kill_neg_left":
                    print('demoString == "forehand_kill_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.37, -2.08, -0.01, 0.8, 0.85, -0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.9, -1.22, -0.01, 0.56, 0.13, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_kill_pos":
                    print('demoString == "backhand_kill_pos":')
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.83, 1.20, 0.01, -0.46, -0.01, -0.6]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [0.68, 1.04, 0.01, 0.43, -0.57, -0.61]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.11, 1.04, 0.01, 0.30, -0.83, -0.61]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_kill_pos_left":
                    print('demoString == "backhand_kill_pos_left":')
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.83, -1.20, -0.01, -0.46, 0.01, 0.6]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [-0.68, -1.04, -0.01, 0.43, 0.57, 0.61]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.11, -1.04, -0.01, 0.30, 0.83, 0.61]
                    speedLists = 0.25
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_kill_neg":
                    print('demoString == "backhand_kill_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.9, 1.23, 0.01, 0.57, -0.13, -0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.80, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_kill_neg_left":
                    print('demoString == "backhand_kill_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.80, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_volley_kill_pos":
                    print('demoString == "forehand_volley_kill_pos":')
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.96, 1.64, 0.01, -0.71, -0.91, -0.50]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [0.63, 1.64, 0.01, -0.38, -0.65, -0.50]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.28, 1.64, 0.01, 0.38, -0.01, -0.50]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "forehand_volley_kill_pos_left":
                    print('demoString == "forehand_volley_kill_pos_left":')
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [-0.96, -1.64, -0.01, -0.71, 0.91, 0.50]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [-0.63, -1.64, -0.01, -0.38, 0.65, 0.50]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.28, -1.64, -0.01, 0.38, 0.01, 0.50]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "forehand_volley_kill_neg":
                    print('demoString == "forehand_volley_kill_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.22, 0.01, 0.56, -0.13, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_volley_kill_neg_left":
                    print('demoString == "forehand_volley_kill_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.37, -2.08, -0.01, 0.8, 0.85, -0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.9, -1.22, -0.01, 0.56, 0.13, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_kill_pos":
                    print('demoString == "backhand_volley_kill_pos":')
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [1.01, 0.02, 0.01, -0.8, -0.02, 0.37]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [0.82, 0.67, 0.01, -1.04, -0.32, 0.38]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.16, 0.88, 0.01, -0.56, -0.89, -0.83]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_kill_pos_left":
                    print('demoString == "backhand_volley_kill_pos_left":')
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.01, -0.02, -0.01, -0.8, 0.02, -0.37]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [-0.82, -0.67, -0.01, -1.04, 0.32, -0.38]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.16, -0.88, -0.01, -0.56, 0.89, 0.83]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_kill_neg":
                    print('demoString == "backhand_volley_kill_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.9, 1.23, 0.01, 0.57, -0.13, -0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.80, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_volley_kill_neg_left":
                    print('demoString == "backhand_volley_kill_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.80, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_two_wall_boast":
                    print('demoString == "forehand_two_wall_boast":')
                    motion_service.post.moveTo(0, 0, -0.79)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.77, 0.97, 0.01, -0.92, -1.04, 0.22]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [0.7, 2.08, 0.01, 0.93, -0.35, 0.22]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.61, 1.56, 0.01, 0.93, -0.01, 0.7]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -0.79)
                elif demoString == "forehand_two_wall_boast_left":
                    print('demoString == "forehand_two_wall_boast_left":')
                    motion_service.post.moveTo(0, 0, 0.79)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.77, -0.97, -0.01, -0.92, 1.04, -0.22]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [-0.7, -2.08, -0.01, 0.93, 0.35, -0.22]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.61, -1.56, -0.01, 0.93, 0.01, -0.7]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 0.79)
                elif demoString == "forehand_two_wall_boast_neg":
                    print('demoString == "forehand_two_wall_boast_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.22, 0.01, 0.56, -0.13, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_two_wall_boast_neg_left":
                    print('demoString == "forehand_two_wall_boast_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.37, -2.08, -0.01, 0.8, 0.85, -0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.9, -1.22, -0.01, 0.56, 0.13, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_two_wall_boast":
                    print('demoString == "backhand_two_wall_boast":')
                    motion_service.post.moveTo(0, 0, 1.58)
                    time.sleep(2.0)
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [1.30, 1.58, 0.01, 0.13, -0.01, 0.40]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, -1.58)
                    angleLists = [0.90, 1.48, 0.01, 0.49, -0.53, -0.06]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.47, 1.56, 0.01, 0.88, -0.96, -0.58]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_two_wall_boast_left":
                    print('demoString == "backhand_two_wall_boast_left":')
                    motion_service.post.moveTo(0, 0, -1.58)
                    time.sleep(2.0)
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-1.30, -1.58, -0.01, 0.13, 0.01, -0.40]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    motion_service.post.moveTo(0, 0, 1.58)
                    angleLists = [-0.90, -1.48, -0.01, 0.49, 0.53, 0.06]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.47, -1.56, -0.01, 0.88, 0.96, 0.58]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_two_wall_boast_neg":
                    print('demoString == "backhand_two_wall_boast_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.9, 1.23, 0.01, 0.57, -0.13, -0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.80, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_two_wall_boast_neg_left":
                    print('demoString == "backhand_two_wall_boast_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.80, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_lob":
                    print('demoString == "forehand_lob":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "HipPitch", "KneePitch"]
                    angleLists = [0.01, 1.56, 0.01, 0.77, -0.42, 0.96, -0.78, 0.25]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.99, 1.56, 0.01, -0.64, -0.15, 1.2, -0.04, 0.01]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_lob_left":
                    print('demoString == "forehand_lob_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "KneePitch"]
                    angleLists = [-0.01, -1.56, -0.01, 0.77, 0.42, -0.96, -0.78, 0.25]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.99, -1.56, -0.01, -0.64, 0.15, -1.2, -0.04, 0.01]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_lob_neg":
                    print('demoString == "forehand_lob_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.37, 2.08, 0.01, 0.8, -0.85, 0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.9, 1.22, 0.01, 0.56, -0.13, -0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "forehand_lob_neg_left":
                    print('demoString == "forehand_lob_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.37, -2.08, -0.01, 0.8, 0.85, -0.58]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.9, -1.22, -0.01, 0.56, 0.13, 0.61]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_lob":
                    print('demoString == "backhand_lob":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "HipPitch", "KneePitch"]
                    angleLists = [0.68, -0.63, 0.01, 1.15, -0.36, 0.49, -0.78, 0.25]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.2, -0.43, 0.01, -1.09, -0.64, 0.49, -0.04, 0.01]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_lob_left":
                    print('demoString == "backhand_lob_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "KneePitch"]
                    angleLists = [-0.68, 0.63, -0.01, 1.15, 0.36, -0.49, -0.78, 0.25]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.2, 0.43, -0.01, -1.09, 0.64, -0.49, -0.04, 0.01]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_lob_neg":
                    print('demoString == "backhand_lob_neg":')
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                    angleLists = [0.9, 1.23, 0.01, 0.57, -0.13, -0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [0.36, 2.08, 0.01, 0.80, -0.85, 0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "backhand_lob_neg_left":
                    print('demoString == "backhand_lob_neg_left":')
                    names = ["LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                    angleLists = [-0.9, -1.23, -0.01, 0.57, 0.13, 0.6]
                    speedLists = 0.3
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    angleLists = [-0.36, -2.08, -0.01, 0.80, 0.85, -0.54]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "reset":
                    motion_service.post.moveTo(0, 0, 0.79)
            else:
                if 'question' in content:
                    ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                    # ttsAnimated.setParameter("speed", 100)
                    configuration = {"bodyLanguageMode": "contextual"}
                    if content['question'] == 'Concurrent':
                        print("Concurrent question detected")
                        tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
                        ttsAnimated.say(str(action))
                    else:
                        global goodBadQuestion
                        global expectingTouch
                        expectingTouch = True
                        tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
                        ttsAnimated.say(str(action), configuration)
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                                 "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                        angleLists = [0.98, 1.69, 0.01, 0.79, -0.09, -0.03, -0.98, -1.69, 0.01, 0.79, 0.09, 0.03]
                        speedLists = 0.3
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                        if content['question'] == 'GoodBad':
                            goodBadQuestion = True
                            print("GoodBad question detected")
                        else:
                            goodBadQuestion = False
                            print("YesNo question detected")

                        global ReactToTouch
                        global questionCount
                        if questionCount == 0:
                            ReactToTouch = ReactToTouch("ReactToTouch")

                        questionCount += 1

                        # Sleep for 7 seconds or until touch.
                        start_time = datetime.now()
                        sleep_time = datetime.now()
                        time_passed = sleep_time - start_time
                        time_passed_delta = time_passed.total_seconds()
                        while expectingTouch and time_passed_delta < 7.0:
                            sleep_time = datetime.now()
                            time_passed = sleep_time - start_time
                            time_passed_delta = time_passed.total_seconds()

                        expectingTouch = False
                else:
                    ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                    # ttsAnimated.setParameter("speed", 100)
                    configuration = {"bodyLanguageMode": "contextual"}
                    # Show the initial screen on tablet
                    tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
                    ttsAnimated.say(str(action), configuration)

            previous_content = content
            return {'completed': 1}, 200


class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        print "initialising"
        ALModule.__init__(self, name)

        global memory
        memory = ALProxy("ALMemory", robot_ip, port)
        memory.subscribeToEvent("TouchChanged",
                                "ReactToTouch",
                                "onTouched")

    def onTouched(self, strVarName, value):
        print("onTouched")
        global expectingTouch
        if not expectingTouch:
            return -1
        memory.unsubscribeToEvent("TouchChanged", "ReactToTouch")

        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])

        outcome = self.say(touched_bodies)

        memory.subscribeToEvent("TouchChanged", "ReactToTouch", "onTouched")
        expectingTouch = False

        return outcome

    def say(self, bodies):
        global goodBadQuestion
        if bodies == []:
            return -1

        ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
        # ttsAnimated.setParameter("speed", 100)
        configuration = {"bodyLanguageMode": "contextual"}
        if "LArm" in bodies or "RArm" in bodies or "LHand/Touch/Back" in bodies or "RHand/Touch/Back" in bodies:
            ttsAnimated.say("Great!", configuration)
            output = {"questionResponse": "Pos"}
            r = requests.post(post_address, json=output)

            # Wait for response before continuing because the session might be paused.
            while r.status_code is None:
                time.sleep(0.2)
            outcome = 1
        else:
            if goodBadQuestion:
                ttsAnimated.say("OK, don't worry. We can keep improving together!", configuration)
            else:
                ttsAnimated.say("Oops, my mistake!", configuration)
            output = {"questionResponse": "Neg"}
            r = requests.post(post_address, json=output)

            # Wait for response before continuing because the session might be paused.
            while r.status_code is None:
                time.sleep(0.2)
            outcome = 0

        return outcome


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
        print("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)
