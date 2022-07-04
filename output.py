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
from datetime import datetime

app = Flask('output_api')
api = Api(app)

# ITT_Pepper:
robot_ip = "192.168.1.5"
port = 9559

# Simulation:
# robot_ip = "localhost"
# port = 45053

# Phone hotspot:
# robot_ip = "192.168.43.57"
# port = 9559

memory = None
ReactToTouch = None
questionCount = 0
ReactToTouch_FirstTimeQuestion = None
questionCount_FirstTimeQuestion = 0
expectingTouch = False
goodBadQuestion = False
pause = 0
remembered_content = None

class Action(Resource):
    def post(self):
        global pause
        global remembered_content
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
                self._display(content)

        else:
            print("ERROR: request is not json")
            return {'message': 'Request not json'}, 500

    def _display(self, content):
        global pause
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
            tts.setParameter("speed", 75)
            # configuration = {"bodyLanguageMode": "contextual"}
            tts.say("OK, you can stop there.")
        elif 'pause' in content:  # User has selected stop button so stop session until we get more info.
            pause = 1
            time.sleep(1)  # Not the most elegant solution but wait for page to be updated in robot's memory to display pause page.
            tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
            tts = ALProxy("ALTextToSpeech", robot_ip, port)
            tts.setParameter("speed", 75)
            tts.post.say("OK, would you like to stop the whole session or just this exercise set?")
        elif 'silence' in content:
            tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
        else:
            action = content['utterance']
            print(action)
            if 'demo' in content:
                tts = ALProxy("ALTextToSpeech", robot_ip, port)
                tts.setParameter("speed", 75)
                tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
                tts.post.say(str(action))
                demoString = str(content['demo'])

                if demoString == "tabletop_circles_pos":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    angleLists = [0.90, 0.69, 0.01, 0.98, 0.01, 0.29,
                                  -1.15, -0.76, 0.01, 1.13, 0.01, -0.45,
                                  -0.25, 0.02, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    motion_service.post.moveTo(0, 0, 0.39)
                    angleLists = [0.80, 0.57, 0.01, 0.80, 0.01, 0.60,
                                  -0.54, -0.80, 0.01, 0.75, 0.01, -0.45,
                                  -0.37, 0.22, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.1)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [0.70, 0.48, 0.01, -0.19, 0.01, 0.26,
                                  -0.78, -0.84, 0.01, -0.01, 0.01, -0.45,
                                  -0.68, 0.02, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.1)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [0.76, 1.19, 0.01, 0.91, 0.01, -0.08,
                                  -0.86, -0.71, 0.01, 0.89, 0.01, -0.45,
                                  -0.38, -0.19, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.1)
                    motion_service.post.moveTo(0, 0, 0.39)
                    angleLists = [0.90, 0.69, 0.01, 0.98, 0.01, 0.29,
                                  -1.15, -0.76, 0.01, 1.13, 0.01, -0.45,
                                  -0.25, 0.02, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                elif demoString == "tabletop_circles_pos_vid":
                    print("Play video for tabletop_circles_pos")

                elif demoString == "tabletop_circles_neg":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    angleLists = [0.90, 0.69, 0.01, 0.98, 0.01, 0.29,
                                  -1.15, -0.76, 0.01, 1.13, 0.01, -0.45,
                                  -0.25, 0.02, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    motion_service.post.moveTo(0, 0, 0.39)
                    angleLists = [0.80, 0.57, 0.01, 0.80, 0.01, 0.60,
                                  -0.54, -0.80, 0.01, 0.75, 0.01, -0.45,
                                  -0.37, -0.23, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.1)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [0.70, 0.48, 0.01, -0.19, 0.01, 0.26,
                                  -0.78, -0.84, 0.01, -0.01, 0.01, -0.45,
                                  -0.68, -0.23, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.1)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [0.76, 1.19, 0.01, 0.91, 0.01, -0.08,
                                  -0.86, -0.71, 0.01, 0.89, 0.01, -0.45,
                                  -0.38, -0.23, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.1)
                    motion_service.post.moveTo(0, 0, 0.39)
                    angleLists = [0.90, 0.69, 0.01, 0.98, 0.01, 0.29,
                                  -1.15, -0.76, 0.01, 1.13, 0.01, -0.45,
                                  -0.25, 0.02, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                elif demoString == "tabletop_circles_neg_vid":
                    print("Play video for tabletop_circles_neg")

                elif demoString == "towel_slide_pos":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    angleLists = [0.83, 0.72, 0.01, 0.67, 0.13, -0.70,
                                  -0.87, -0.87, 0.01, 0.79, 0.08, 0.51,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    angleLists = [0.60, 0.67, 0.01, -0.43, 0.13, -0.70,
                                  -0.58, -0.87, 0.01, -0.35, 0.08, 0.51,
                                  -0.70, 0.00, 0.25]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.2)
                    angleLists = [0.83, 0.72, 0.01, 0.67, 0.13, -0.70,
                                  -0.87, -0.87, 0.01, 0.79, 0.08, 0.51,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                elif demoString == "towel_slide_pos_vid":
                    print("Play video for towel_slide_pos")

                elif demoString == "towel_slide_neg":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    angleLists = [0.83, 0.72, 0.01, 0.67, 0.13, -0.70,
                                  -0.87, -0.87, 0.01, 0.79, 0.08, 0.51,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    angleLists = [0.60, 0.67, 0.01, -0.43, 0.13, -0.70,
                                  -0.58, -0.87, 0.01, -0.35, 0.08, 0.51,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.2)
                    angleLists = [0.83, 0.72, 0.01, 0.67, 0.13, -0.70,
                                  -0.87, -0.87, 0.01, 0.79, 0.08, 0.51,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.1
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                elif demoString == "towel_slide_neg_vid":
                    print("Play video for towel_slide_neg")

                elif demoString == "external_rotations_with_cane_pos":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    angleLists = [1.26, 1.40, 0.01, 1.27, 0.15, 1.55,
                                  -1.25, -1.51, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [1.26, 2.08, 0.01, 1.27, 0.15, 1.55,
                                  -1.25, -1.20, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.2)
                    motion_service.post.moveTo(0, 0, 0.79)
                    angleLists = [1.26, 1.20, 0.01, 1.27, 0.15, 1.55,
                                  -1.25, -2.08, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.2)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [1.26, 1.40, 0.01, 1.27, 0.15, 1.55,
                                  -1.25, -1.51, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                elif demoString == "external_rotations_with_cane_pos_vid":
                    print("Play video for external_rotations_with_cane_pos")

                elif demoString == "external_rotations_with_cane_neg":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    angleLists = [1.26, 1.40, 0.01, 1.27, 0.15, 1.55,
                                  -1.25, -1.51, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [0.96, 2.08, 0.01, 1.27, 0.15, 1.55,
                                  -0.95, -1.20, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.2)
                    motion_service.post.moveTo(0, 0, 0.79)
                    angleLists = [0.66, 1.20, 0.01, 1.27, 0.15, 1.55,
                                  -0.65, -2.08, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.2)
                    motion_service.post.moveTo(0, 0, -0.39)
                    angleLists = [0.56, 1.40, 0.01, 1.27, 0.15, 1.55,
                                  -0.55, -1.51, 0.01, 1.39, 0.13, -1.62,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.05
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                elif demoString == "external_rotations_with_cane_neg_vid":
                    print("Play video for external_roatations_with_cane_neg")

                elif demoString == "shoulder_openers_pos":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    angleLists = [1.26, 1.40, 0.01, 1.27, 0.15, 0.14,
                                  -1.25, -1.51, 0.01, 1.39, 0.13, -0.14,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    for i in [0, 1]:
                        angleLists = [1.26, 2.08, 0.01, 1.27, 0.15, 0.14,
                                      -1.25, -2.08, 0.01, 1.39, 0.13, -0.14,
                                      -0.35, 0.00, 0.17]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.2)
                        angleLists = [1.26, 1.40, 0.01, 1.27, 0.15, 0.14,
                                      -1.25, -1.51, 0.01, 1.39, 0.13, -0.14,
                                      -0.35, 0.00, 0.17]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)

                elif demoString == "shoulder_openers_pos_vid":
                    print("Play video for shoulder_openers_pos")

                elif demoString == "shoulder_openers_neg":
                    names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                             "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                             "HipPitch", "HipRoll", "KneePitch"]
                    RElbowRoll = 1.26
                    LElbowRoll = -1.25
                    angleLists = [RElbowRoll, 1.40, 0.01, 1.27, 0.15, 0.14,
                                  LElbowRoll, -1.51, 0.01, 1.39, 0.13, -0.14,
                                  -0.35, 0.00, 0.17]
                    speedLists = 0.2
                    motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    time.sleep(0.5)
                    for i in [0, 1]:
                        RElbowRoll -= 0.25
                        LElbowRoll += 0.25
                        angleLists = [RElbowRoll, 2.08, 0.01, 1.27, 0.15, 0.14,
                                      LElbowRoll, -2.08, 0.01, 1.39, 0.13, -0.14,
                                      -0.35, 0.00, 0.17]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.2)
                        RElbowRoll -= 0.25
                        LElbowRoll += 0.25
                        angleLists = [RElbowRoll, 1.40, 0.01, 1.27, 0.15, 0.14,
                                      LElbowRoll, -1.51, 0.01, 1.39, 0.13, -0.14,
                                      -0.35, 0.00, 0.17]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                elif demoString == "shoulder_openers_neg_vid":
                    print("Play video for shoulder_openers_neg")

            else:
                if 'question' in content:
                    # ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                    tts = ALProxy("ALTextToSpeech", robot_ip, port)
                    tts.setParameter("speed", 75)
                    # configuration = {"bodyLanguageMode": "contextual"}
                    if content['question'] == 'Concurrent':
                        print("Concurrent question detected")
                        tts.say(str(action))
                    else:
                        global goodBadQuestion
                        global expectingTouch
                        expectingTouch = True
                        tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
                        tts.say(str(action))
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
                    # ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                    tts = ALProxy("ALTextToSpeech", robot_ip, port)
                    tts.setParameter("speed", 75)
                    # configuration = {"bodyLanguageMode": "contextual"}
                    # Show the initial screen on tablet
                    tabletService.showWebview("http://198.18.0.1/apps/boot-config/index.html")
                    tts.say(str(action))

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
        if (bodies == []):
            return -1

        # ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
        tts = ALProxy("ALTextToSpeech", robot_ip, port)
        tts.setParameter("speed", 75)
        # configuration = {"bodyLanguageMode": "contextual"}
        if "LArm" in bodies or "RArm" in bodies or "LHand/Touch/Back" in bodies or "RHand/Touch/Back" in bodies:
            tts.say("Great!")
            outcome = 1
        else:
            if goodBadQuestion:
                tts.say("OK, don't worry. We can keep improving together!")
            else:
                tts.say("Oops, my mistake!")
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
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)
