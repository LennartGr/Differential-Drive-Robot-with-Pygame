import threading
import time
import pygame
from datetime import datetime
import difDriveRobot as robot
import environment
import math
from math import sin, cos, tan

UPDATES_PER_SECOND = 20
# how many measurements are taken with a single rotation
ROTATION_STEPS = 360
# how many seconds shall one rotation take (for display reasons)
ROTATION_TIME = 3

# fetched from environment
BOARD_WIDTH = 0
BOARD_HEIGHT = 0

# class inherits from Thread
# knows the environment and changes the robot's control parameters following some strategy
class Algorithm(threading.Thread):

    def __init__(self, robot, environment):
        # call super class constructor
        threading.Thread.__init__(self)
        self.running = True
        self.robot = robot
        self.environment = environment
        BOARD_WIDTH = self.environment.WIDTH - 2 * self.environment.WALL_SIZE
        BOARD_HEIGHT = self.environment.HEIGHT - 2 * self.environment.WALL_SIZE

    def run(self):
        self.scannerAlgorithm()

    def scannerAlgorithm(self):
        D_DOOR = 300

        dt = 0
        lasttime = datetime.now()
        while(self.running): # basically while(true)
            # time difference to last action
            dt = (datetime.now() - lasttime).total_seconds()
            lasttime = datetime.now()
            measurements = self.robotFullRotationMeasuring()
            (doorDetected, indexDoorMiddle) = self.detectDoor(measurements)
            if doorDetected:
                # make the robot look to the supposed center of the door
                self.robotPartialRotation(indexDoorMiddle)
                self.robotMoveForwardAnimated(D_DOOR)
            elif self.isOnCenterLine(measurements):
                pass
            else:
                (centerLineDetected, indexCenterLine, distance) = self.detectCenterLine(measurements)
                if centerLineDetected:
                    pass
                else: # random action
                    self.behaveRandomly(measurements)
                        
    def detectDoor(self, measurements):   
        CUTOFF_DELTA = 150
        print("MEASUREMENTS")
        self.printArray(measurements)
        # TODO list of drop and increase indices
        dropIndex = -1
        increaseIndex = -1
        for i in range(ROTATION_STEPS):
            if measurements[i - 1] + CUTOFF_DELTA < measurements[i]:
                dropIndex = i
            if measurements[i] > measurements[(i + 1) % len(measurements)] + CUTOFF_DELTA:
                increaseIndex = i
        # find index of angle corresponding to door
        indexDoorMiddle = -1
        doorDetected = dropIndex != -1 and increaseIndex != -1
        if doorDetected:
            # calculate estimated middle of the door
            if dropIndex < increaseIndex:
                indexDoorMiddle = round(0.5 * (increaseIndex + dropIndex))
            else:
                indexDoorMiddle = round((0.5 * (dropIndex + increaseIndex + len(measurements))) % len(measurements))
        print("drop index   door index   increaseIndex", (dropIndex, indexDoorMiddle, increaseIndex))
        return (doorDetected, indexDoorMiddle)

    def isOnCenterLine(self, measurements):
        epsilon = 10
        return False

    def detectCenterLine(self, measurements):
        centerLineDetected = False
        indexCenterLine = 0
        distance = 100
        return (centerLineDetected, indexCenterLine, distance)

    def hasObstacleInGazeDirection(self, measurements):
        return False

    def behaveRandomly(self, measurements):
        SAFETY_DISTANCE = 100
        MOVING_DISTANCE = 80
        print("Falling back to random behaviour")
        while self.hasObstacleInGazeDirection(measurements):
            pass

    # just for the simulation
    def robotMoveForwardAnimated(self, distance):
        # TODO use
        MOVING_SPEED = 50 
        FPS = 30
        forwardStep = MOVING_SPEED / FPS
        distanceLeft = distance
        while distanceLeft > forwardStep:
            self.robotMoveForward(forwardStep)
            time.sleep(1 / FPS)
            distanceLeft -= forwardStep
        #do what's left to go the distance precisely
        if distanceLeft > 0:
            self.robotMoveForward(distanceLeft)

    # very simple algorithm for testing
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

    # search for the middle of the door by determining the two spots where the measured distance suddenly increases / drops significantly
    # go some distance in the direction of that spot
    def scannerAlgorithmSimple(self):
        epsilon = 10
        cutoffDelta = 170
        forwardAfterRotation = 300 # shall be a whole number
        dt = 0
        lasttime = datetime.now()
        while(self.running):
            # time difference to last action
            dt = (datetime.now() - lasttime).total_seconds()
            lasttime = datetime.now()
            measurements = self.robotFullRotationMeasuring()
            # search measurements for the two closest points on each horizontal wall
            # distance roughly BOARD_HEIGHT to each other
            # search for four non-monotone spots
            monotoneIndices = []
            monotoneValues = []
            dropIndex = -1
            increaseIndex = -1
            for i in range(ROTATION_STEPS):
                if measurements[i - 1] < measurements[i] and measurements[i] < measurements[(i + 1) % len(measurements)]:
                    monotoneIndices.append(i)
                if measurements[i - 1] + cutoffDelta < measurements[i]:
                    dropIndex = i
                elif measurements[i] > measurements[(i + 1) % len(measurements)] + cutoffDelta:
                    increaseIndex = i
            # find index of angle corresponding to door
            if dropIndex < increaseIndex:
                doorIndex = round(0.5 * (increaseIndex + dropIndex))
            else:
                doorIndex = round((0.5 * (dropIndex + increaseIndex + len(measurements))) % len(measurements))
            print("drop index   door index   increaseIndex", (dropIndex, doorIndex, increaseIndex))
            # rotate to the spot where we assume the middle of the door to be
            time.sleep(1)
            # self.robotPartialRotation(doorIndex)
            self.robotTurn(2 * math.pi * (doorIndex / ROTATION_STEPS))

            # go forward some distance
            distanceToGo = forwardAfterRotation
            while distanceToGo > 0:
                self.robotMoveForward(1)
                time.sleep(0.01)
                distanceToGo -= 1
            

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

    def robotFullRotationMeasuring(self):
        measurements = []
        for i in range(ROTATION_STEPS):
            measurements.append(self.environment.getDistanceToObstacle(self.robot.x, self.robot.y, self.robot.theta))
            self.robotTurn(2 * math.pi / ROTATION_STEPS)
            time.sleep(ROTATION_TIME / ROTATION_STEPS)
        return measurements

    # make a partial rotation without taking measurements
    def robotPartialRotation(self, steps):
        if steps < ROTATION_STEPS / 2:
            for i in range(steps):
                self.robotTurn(2 * math.pi / ROTATION_STEPS)
                time.sleep(ROTATION_TIME / ROTATION_STEPS)
        else:
            # more efficient to rotate in the other direction
            for i in range(ROTATION_STEPS - steps):
                self.robotTurn(2 * math.pi / ROTATION_STEPS)
                time.sleep(ROTATION_TIME / ROTATION_STEPS)

    def printArray(self, array):
        for i in range(0, len(array)):
            print(str(i) + "   " + str(array[i]))
