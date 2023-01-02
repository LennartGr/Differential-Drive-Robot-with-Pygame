import threading
import time
import pygame
from datetime import datetime
import difDriveRobot as robot
import environment
import math
from math import sin, cos, tan

UPDATES_PER_SECOND = 20

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
        self.manualControlAlgorithm()

    def backAndForthAlgorithm(self):
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

    # control wheel velocities with keyboard, w-s-e-d keys
    def manualControlAlgorithm(self):
        STEP = 5
        v_l = 0
        v_r = 0
        dt = 0
        lasttime = datetime.now()
        while(self.running):
            # time difference to last action
            dt = (datetime.now() - lasttime).total_seconds()

            # fetch keypress
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key==pygame.K_s:
                    v_l -= STEP
                if event.type == pygame.KEYDOWN and event.key==pygame.K_w:
                    v_l += STEP
                if event.type == pygame.KEYDOWN and event.key==pygame.K_d:
                    v_r -= STEP
                if event.type == pygame.KEYDOWN and event.key==pygame.K_e:
                    v_r += STEP   
                if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                    v_r = 0
                    v_l = 0
            # move robot according to new control variables, but only once in a while
            if dt > (1 / UPDATES_PER_SECOND):
                lasttime = datetime.now()
                self.robot.move(v_l, v_r, dt)

    # manual control that sets x, y, theta of robot directly (not through control variables, namely wheel velocities)
    # use s to turn left, d to turn right
    def manualControlAlgorithmCheating(self):
        dt = 0
        lasttime = datetime.now()
        while(self.running):
            # time difference to last action
            dt = (datetime.now() - lasttime).total_seconds()
            
            # fetch keypress
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key==pygame.K_s:
                    self.robotTurnLeft()
                if event.type == pygame.KEYDOWN and event.key==pygame.K_d:
                    self.robotTurnRight()
            # only move every split second
            if dt > (1 / UPDATES_PER_SECOND):
                lasttime = datetime.now()
                self.robotMoveForward(1)

    # assuming we have solved inverse kinematics, we can tell the robot to drive forward and to turn some angle directly

    def robotMoveForward(self, distance):
        self.robot.x += cos(self.robot.theta) * distance
        self.robot.y += sin(self.robot.theta) * distance

    # make the robot turn clockwise by the given amount in rad
    def robotTurn(self,amount):
        self.robot.theta += amount

    def robotTurnRight(self):
        self.robotTurn(math.pi / 2)

    def robotTurnLeft(self):
        self.robotTurn(- (math.pi / 2))