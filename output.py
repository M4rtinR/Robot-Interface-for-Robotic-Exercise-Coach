#!/usr/bin/env python
# coding: utf-8
import time

from naoqi import ALProxy
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask('output_api')
api = Api(app)

# robot_ip = "192.168.1.37"
robot_ip = "localhost"
# port = 9559
port = 43255
memory = None

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

            if 'start' in content:
                posture_service = ALProxy("ALRobotPosture", robot_ip, port)

                # Wake up robot
                motion_service.wakeUp()

                # Send robot to Stand
                posture_service.goToPosture("StandInit", 0.5)
            elif 'stop' in content:
                ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                configuration = {"bodyLanguageMode": "contextual"}
                ttsAnimated.say("That's 30, you can stop there.", configuration)
            else:
                action = content['utterance']
                print(action)
                if 'demo' in content:
                    tts = ALProxy("ALTextToSpeech", robot_ip, port)
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
                        angleLists = [0.52, 1.68, 0.01, 0.62, -0.12, -0.02]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.3)
                        # motion_service.post.moveTo(0, 0, 0.79)
                        names.append("HipPitch")
                        angleLists = [0.02, 1.68, 0.01, 0.62, -1.00, -0.02, -0.08]
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
                    elif demoString == "lob_pos":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw", "HipPitch", "KneePitch"]
                        motion_service.post.moveTo(0, 0, -0.79)
                        time.sleep(2.0)
                        angleLists = [0.96, 2.08, 0.01, 0.93, -0.62, -0.02, -0.36, 0.12]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        motion_service.post.moveTo(0, 0, 1.58)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01, -0.36, 0.12]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.23, -0.01, -0.28, 0.08]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        angleLists = [0.35, 2.08, 0.01, -0.21, -0.02, -0.26, -0.16, 0.02]
                        speedLists = 0.1
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(2.0)
                        motion_service.post.moveTo(0, 0, -0.79)
                    elif demoString == "lob_neg":
                        names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]
                        angleLists = [0.53, 2.07, 0.01, 0.93, -0.55, -0.01]
                        speedLists = 0.2
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                        time.sleep(0.6)
                        angleLists = [1.31, 1.45, 0.01, 0.93, -0.04, 0.39]
                        speedLists = 0.5
                        motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                    elif demoString == "reset":
                        motion_service.post.moveTo(0, 0, -3.16)
                else:
                    if 'question' in content:
                        ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                        configuration = {"bodyLanguageMode": "contextual"}
                        if content['question'] == 'GoodBad':
                            print("GoodBad question detected")
                            ttsAnimated.say(str(action), configuration)
                            names = ["RElbowRoll", "RElbowYaw", "RHand", "RShoulderPitch", "RShoulderRoll", "RWristYaw",
                                     "LElbowRoll", "LElbowYaw", "LHand", "LShoulderPitch", "LShoulderRoll", "LWristYaw"]
                            angleLists = [0.98, 1.69, 0.01, 0.79, -0.09, -0.03, -0.98, -1.69, 0.01, 0.79, 0.09, 0.03]
                            speedLists = 0.3
                            motion_service.angleInterpolationWithSpeed(names, angleLists, speedLists)
                            global memory
                            memory = ALProxy("ALMemory", robot_ip, port)
                            memory.subscribeToEvent("TouchChanged", "ReactToTouch", "onTouched")
                            time.sleep(2.0)
                    else:
                        ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
                        configuration = {"bodyLanguageMode": "contextual"}
                        ttsAnimated.say(str(action), configuration)
                # TODO: Deal with videos
                return {'completed': 1}, 200
        else:
            print("ERROR: request is not json")
            return {'message': 'Request not json'}, 500

    def onTouched(self, strVarName, value):
        print("onTouched")
        memory.unsubscribeToEvent("TouchChanged", "ReactToTouch")

        touched = ""
        for p in value:
            if p[1]:
                touched = p[0]

        ttsAnimated = ALProxy("ALAnimatedSpeech", robot_ip, port)
        configuration = {"bodyLanguageMode": "contextual"}
        if touched == "LHand" or touched == "RHand":
            ttsAnimated.say("Great!", configuration)
        else:
            ttsAnimated.say("OK, don't worry. We can keep improving together!")



api.add_resource(Action, '/output')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4999)
