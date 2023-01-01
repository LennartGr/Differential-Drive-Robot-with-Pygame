import threading
import time
import pygame

# state holder for the robot
# also knows robots movement and control parameters
class Robot:

    def __init__(self, x):
        self.x = x

# class inherits from Thread
# knows the environment and changes the robot's control parameters following some strategy
class Algorithm(threading.Thread):

    def __init__(self, robot, environment):
        # call super class constructor
        threading.Thread.__init__(self)
        self.running = True
        self.robot = robot
        self.environment = environment


    def run(self):
        pygame.init()
        dt = 0
        lasttime = pygame.time.get_ticks()
        sign = 1
        while(self.running):
            # time difference to last action
            dt = (pygame.time.get_ticks() - lasttime) / 1000 
            lasttime = pygame.time.get_ticks()
            # modify state of robot respectively to passed time and the environment
            # if close to obstacle, go to the other direction
            if self.environment.getDistanceToObstacle(self.robot.x) < 1:
                sign = -sign
            # simulate calculation that takes some time
            time.sleep(0.5)
            self.robot.x += sign * dt

# state holder for obstacles in the map
# doesn't need to know any other component
class Environment:

    def __init__(self):
        self.leftBorder = -5
        self.rightBorder = 10

    def getDistanceToObstacle(self, x):
        return min(abs(x - self.leftBorder), abs(x - self.rightBorder))

# displays the robot and the environment
class GUI:

    def __init__(self, robot, environment):
        self.robot = robot
        self.environment = environment

    def display(self):
        while True:
            print("current robot position: ", self.robot.x)


# main method
# create robot, start algorithm and init GUI
myRobot = Robot(0)
myEnv = Environment()
myAlgorithm = Algorithm(myRobot, myEnv)
myGui = GUI(myRobot, myEnv)
# call start, not run
myAlgorithm.start()
myGui.display()
"""
myAlgorithm.test()
myGui.test()
print(myRobot.x)
"""

