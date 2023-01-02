import threading
import time
from datetime import datetime
import difDriveRobot as robot
import environment
import math

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
        vel = 5
        dt = 0
        lasttime = datetime.now()
        sign = 1
        while(self.running):
            # time difference to last action
            dt = (datetime.now() - lasttime).total_seconds()
            lasttime = datetime.now()
            # modify state of robot respectively to passed time and the environment
            # if close to obstacle, go to the other direction
            if self.environment.getDistanceToObstacle(self.robot.x, self.robot.y, self.robot.theta) < 10:
                sign = -sign
                self.robot.theta += math.pi
            # simulate calculation that takes some time
            time.sleep(0.5)
            self.robot.x += sign * dt * vel