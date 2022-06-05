from __future__ import print_function

'''import qi
import argparse
import sys
import time


def main(session):
    """
    This example uses the showImage method.
    To Test ALTabletService, you need to run the script ON the robot.
    """
    # Get the service ALTabletService.

    try:
        tabletService = session.service("ALTabletService")

        # Display a local image located in img folder in the root of the web server
        # The ip of the robot from the tablet is 198.18.0.1
        tabletService.showWebview("http://www.google.com")

        time.sleep(3)

        # Hide the web view
        #tabletService.hideWebview()
    except Exception as e:
        print("Error was: ", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.43.57",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)'''


#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use showWebview Method"""

import qi
import argparse
import sys
import time


def main(session):
    """
    This example uses the showWebview method.
    To Test ALTabletService, you need to run the script ON the robot.
    """
    # Get the service ALTabletService.

    try:
        tabletService = session.service("ALTabletService")

        # Ensure that the tablet wifi is enable
        tabletService.enableWifi()

        # Display a web page on the tablet
        '''tabletService.loadApplication("/home/martin/Stroke Rehab (Physical)/html/index.html")
        time.sleep(3)
        tabletService.showWebview("/home/martin/Stroke Rehab (Physical)/html/index.html")

        time.sleep(3)
        tabletService.hideWebview

        if tabletService.showWebview("https://www.psaworldtour.com"):
            print("Success PSA")
        else:
            print("Fail PSA")

        time.sleep(5)
        tabletService.hideWebview
        time.sleep(3)

        # Display a web page on the tablet
        if tabletService.showWebview("192.168.43.19:8000/display"):
            print("Success ex")
        else:
            print("Fail ex")

        time.sleep(20)'''


        if tabletService.playVideo("http://198.18.0.1/apps/boot-config/TestVid.webm"):
            print("Video playing")
        else:
            print("Video not playing")
        length = tabletService.getVideoLength()
        print("Length of video = " + str(length) + "milliseconds.")
        time.sleep(5)

        if tabletService.playVideo("http://198.18.0.1/apps/boot-config/TestVid.ogg"):
            print("Video playing")
        else:
            print("Video not playing")
        length = tabletService.getVideoLength()
        print("Length of video = " + str(length) + "milliseconds.")
        time.sleep(5)

        tabletService.showImage("http://198.18.0.1/apps/boot-config/icon.png")
        time.sleep(5)

        # Display a local web page located in boot-config/html folder
        # The ip of the robot from the tablet is 198.18.0.1
        if tabletService.showWebview("http://198.18.0.1/apps/boot-config/video.html"):
            print("Success loading")
        else:
            print("Fail loading")

        time.sleep(5)

        # Hide the web view
        # tabletService.hideWebview()
    except Exception as e:
        print("Error was: ", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.43.57",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)