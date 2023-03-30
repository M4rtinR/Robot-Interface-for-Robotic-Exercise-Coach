# RobotTest
This repo contains code for running both the squash coaching and stroke rehabilitation systems on Pepper. This is where the interaction with the user is done through Pepper. All of the actions are sent here to be conducted by Pepper and any use of Pepper's touch sensors/limbs is dealt with here. Written in Python 2. The main code can be found here: https://github.com/M4rtinR/coachingPolicies.

## Downloading the Code
Similar to the main coaching policy code, clone the robot test repo into a new Pycharm project. You should then be able to select the required branch for the particular demo you wish to run. The master branch contains the code for the stroke rehabilitation demo, and the Squash_output branch contains the code for the squash demo.

## Running the Demo
  1. Set the Python Interpreter and configuration in the same way as you did for the main coaching policy program. NOTE: this time the Python Interpreter should be set to Python 2.7.
  
  2. Similar to the main coaching policy, a few packages need to be installed before the code will run. Do this in the same way as you did for the main coaching policies code. The required packages are as follows:
  
   (i) flask
    
   (ii) flask_restful
   
   (iii) requests
    
  3. You will also need to install naoqi, which is a little more complicated because we are using an old version of the SDK. 
  
   a) Go to https://www-aldebaran-com.translate.goog/fr/support/pepper-naoqi-2-9/downloads-softwares?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en, scroll down and expand "Old: Pepper SDK 2.5", then click "Old: Pepper SDK 2.5 2.5.10 - Python 2.7 SDK" under Linux to download the tar.
    
   b) Extract the files to a location of your choice (mine are in /home/martin/Programs/pynaoqi-python2.7-2.5.7.1-linux64).
    
   c) Execute the following commands to point Python2.7 to your newly installed naoqi SDK:
    
        export PYTHONPATH=${PYTHONPATH}:/home/martin/Programs/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages
        export QI_SDK_PREFIX=/home/martin/Programs/pynaoqi-python2.7-2.5.7.1-linux64

   Make sure you replace the file path (/home/martin/Programs/pynaoqi-python2.7-2.5.7.1-linux64/lib) with your install location.
   
  4. Make sure the ip address and port is correct for the robot you want to connect to. For the ITT_Pepper robot, it should be: robot_ip = "192.168.1.5" and port = 9559.
  
  5. Click Run.
