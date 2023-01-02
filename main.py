import difDriveRobot
import environment
import algorithm
import gui
import math

ROBOT_WHEEL_RADIUS = 4
ROBOT_RADIUS = 20

# main method
# create robot, start algorithm and init GUI

# TODO later: spawn robot at random spot on the map
myRobot = difDriveRobot.DifDriveRobot(r = ROBOT_WHEEL_RADIUS, l = 20, x = 100, y = 100, theta = 0)
myEnv = environment.Environment()
myAlgorithm = algorithm.Algorithm(myRobot, myEnv)
myGui = gui.GUI(myRobot, myEnv)
# call start, not run
myAlgorithm.start()
myGui.display()