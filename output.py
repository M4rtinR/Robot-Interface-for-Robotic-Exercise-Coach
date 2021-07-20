#!/usr/bin/env python
# coding: utf-8
import time

from naoqi import ALProxy
from multiprocessing import Process,Queue,Pipe
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask('output_api')
api = Api(app)


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
                tabletService.showImage("http://localhost/html/Test.png")

                print("sleep")
                time.sleep(5)

                # Hide the web view
                tabletService.hideImage()
            except Exception as e:
                print("Error was: ", e)'''
            motion_service = ALProxy("ALMotion", "192.168.1.37", 9559)

            if 'start' in content:
                posture_service = ALProxy("ALRobotPosture", "192.168.1.37", 9559)

                # Wake up robot
                motion_service.wakeUp()

                # Send robot to Stand
                posture_service.goToPosture("StandInit", 0.5)
            else:
                action = content['utterance']
                print(action)
                if 'demo' in content:
                    tts = ALProxy("ALTextToSpeech", "192.168.1.37", 9559)
                    tts.post.say(str(action))
                    demoString = str(content['demo'])

                    if demoString == "racket_up_pos":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "racket_up_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.32, 2.08, 0.01, 0.93, -0.39, -0.02]
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
                    elif demoString == "racket_face_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.85, -0.03]
                        speedLists = 0.3
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.5)
                        angleLists = [0.53, 0.75, 0.01, 0.93, -0.13, -0.03]
                        speedLists = 0.05
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "follow_through_pos":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.3)
                        motion_service.post.moveTo(0, 0, 0.79)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        names.append("HipPitch")
                        angleLists = [0.18, 2.07, 0.01, 0.52, -0.03, -0.02, -0.18]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(1.5)
                        motion_service.moveTo(0, 0, -0.79)
                    elif demoString == "follow_through_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [1.09, 2.09, 0.01, 0.15, -1.55, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.3)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.03, -0.01]
                        speedLists = 0.4
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                else:
                    ttsAnimated = ALProxy("ALAnimatedSpeech", "192.168.1.37", 9559)
                    configuration = {"bodyLanguageMode": "contextual"}
                    ttsAnimated.say(str(action), configuration)
                # TODO: Deal with videos
                return {'completed': 1}, 200
        else:
            print("ERROR: request is not json")
            return {'message': 'Request not json'}, 500


api.add_resource(Action, '/output')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4999)
