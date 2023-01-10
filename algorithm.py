import threading
import time
import pygame
from datetime import datetime
import difDriveRobot as robot
import environment
import arrayUtils
import math
from math import sin, cos, tan

UPDATES_PER_SECOND = 20
# how many measurements are taken with a single rotation
# attention: buggy when set to something little as four
ROTATION_STEPS = 360
# how many seconds shall one rotation take (for display reasons)
ROTATION_TIME = 0.1
MOVING_SPEED = 200

# fetched from environment
BOARD_WIDTH = environment.Environment.WIDTH - 2 * environment.Environment.WALL_SIZE
BOARD_HEIGHT = environment.Environment.HEIGHT - 2 * environment.Environment.WALL_SIZE

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
        self.scannerAlgorithm()

    # our algorithm
    def scannerAlgorithm(self):
        dt = 0
        lasttime = datetime.now()
        while(self.running): # basically while(true)
            # time difference to last action: for the simulation
            dt = (datetime.now() - lasttime).total_seconds()
            lasttime = datetime.now()
            measurements = self.robotRotationMeasuring()
            centerLineFound = self.searchCenterLineAndMove(measurements)
            if not centerLineFound:
                self.robotMoveRandomly(measurements)

    # searches the center line by analyzing the measurements.
    # if robot already on sensor line: follow it
    # else try to navigate robot in the direction of center line
    # return false if no clue where center line is, in that case robot was not moved
    # else return true
    def searchCenterLineAndMove(self, measurements):
        OPPOSITE_TOLERANCE = 2
        WALL_DISTANCE_EPSILON = 10
        ALREADY_MIDDLE_LINE_EPSILON = 20
        D_ML_FOLLOWING = 80
        D_ML_APPROACHING = 50
        # when the robot is believed to be on the middle line but an obstacle blocks the way with this distance, turn
        D_ML_WALL_TURN = 150
        D_DOOR = 500
        closeDistanceIndices = []
        closeDistanceValues = []

        for i in range(ROTATION_STEPS):
            if measurements[i - 1] > measurements[i] and measurements[i] < measurements[(i + 1) % len(measurements)]:
                closeDistanceIndices.append(i)
                closeDistanceValues.append(measurements[i])
        # high distance indices found
        print("CLOSE DISTANCE INDICES:")
        print(closeDistanceIndices)
        metaIndicesOppositePairs = arrayUtils.getIndicePairsWithValueDistance(closeDistanceIndices, ROTATION_STEPS / 2, OPPOSITE_TOLERANCE)
        spotsFound = False
        # whether the upperWall variables actually correspond to the upper wall is not guaranteed
        upperWallIndex = -1
        lowerWallIndex = -1
        distanceUpperWall = -1
        distanceLowerWall = -1
        for metaIndexTuple in metaIndicesOppositePairs:
            (metaIndexOne, metaIndexTwo) = metaIndexTuple
            dif = abs(closeDistanceValues[metaIndexOne] + closeDistanceValues[metaIndexTwo] - BOARD_HEIGHT)
            if  dif < WALL_DISTANCE_EPSILON:
                # we found two spots that are opposite to each other on our rotation range and that have the correct distance to each other
                spotsFound = True
                upperWallIndex = closeDistanceIndices[metaIndexOne]
                lowerWallIndex = closeDistanceIndices[metaIndexTwo]
                distanceUpperWall = closeDistanceValues[metaIndexOne]
                distanceLowerWall = closeDistanceValues[metaIndexTwo]
                # TODO look for other candidates as well, prefer the one where upper and lower wall are 90 deg. angle to robot gaze
                break
        if spotsFound:
            if abs(distanceLowerWall - distanceUpperWall) < ALREADY_MIDDLE_LINE_EPSILON:
                # case already on the middle line
                # ensure good rotation. If already looking in direction of middle line, no rotation is necessary
                # TODO might result in walking middle line in only one direction
                # check if we can see the door from here and that it is fairly large -----------------------------------------------------------
                correctionDirectionA = round(lowerWallIndex + ROTATION_STEPS / 4) % ROTATION_STEPS
                correctionDirectionB = round(upperWallIndex + ROTATION_STEPS / 4) % ROTATION_STEPS
                self.robotPartialRotation(min(correctionDirectionA, correctionDirectionB))
                # check if robot is close to wall
                if self.getRobotDistToObstacle() < D_ML_WALL_TURN:
                    # make an attempt in detecting and passing the door
                    doorPassed = self.detectDoorSpecific(D_ML_WALL_TURN)
                    if doorPassed:
                        return
                    # turn 180 deg and go to the other side of the wall
                    else:
                        self.robotPartialRotation(round(ROTATION_STEPS / 2))
                # if we are really on the middle line, the robot should be able to move in the other direction without crashing into obstacle
                self.robotMoveForwardAnimated(D_ML_FOLLOWING)
            else:
                # not on the middle line yet
                if distanceUpperWall < distanceLowerWall:
                    self.robotPartialRotation(lowerWallIndex)
                    # min to avoid overshoot
                    self.robotMoveForwardAnimated(min(D_ML_APPROACHING, abs(distanceLowerWall - BOARD_HEIGHT / 2)))
                else: 
                    # upper wall is further away, so move in that direction
                    self.robotPartialRotation(upperWallIndex)
                    self.robotMoveForwardAnimated(min(D_ML_APPROACHING, abs(distanceUpperWall - BOARD_HEIGHT / 2)))
        return spotsFound

    # try to detect the door in a certain angle range, not in a full scan
    # under the assumption the robot is already on the middle line and orientated correctly
    def detectDoorSpecific(self, wallDistance):
        # TODO values shall depend on wall distance and door position
        START_SCAN_INDEX = 320
        END_SCAN_INDEX = 10
        ROTATION_AMOUNT = (ROTATION_STEPS + END_SCAN_INDEX - START_SCAN_INDEX) % ROTATION_STEPS
        CUTOFF_DELTA = 100
        D_DOOR = 250
        # good rotation is ensured 
        # set up for scan
        self.robotPartialRotation(START_SCAN_INDEX)
        measurements = self.robotRotationMeasuring(myRotationSteps = ROTATION_AMOUNT)
        dropIndexList = []
        increaseIndexList = []
        for i in range(len(measurements)):
            if measurements[i - 1] + CUTOFF_DELTA < measurements[i]:
                dropIndexList.append(i)
            if measurements[i] > measurements[(i + 1) % len(measurements)] + CUTOFF_DELTA:
                increaseIndexList.append(i)
        # because we only did a partial rotation, we expect only one drop and one increase index
        if (len(dropIndexList) == 1) and (len(increaseIndexList) == 1):
            indexDoorMiddle = round(0.5 * (dropIndexList[0] + increaseIndexList[0]))
            # make the robot look to the door middle
            self.robotPartialRotation(ROTATION_STEPS - ROTATION_AMOUNT + indexDoorMiddle)
            # make a big step through the door
            self.robotMoveForwardAnimated(D_DOOR)
            return True
        # door not detected, make sure robot is looking in same direction as previously
        self.robotPartialRotation(ROTATION_STEPS - ROTATION_AMOUNT + ROTATION_STEPS - START_SCAN_INDEX)
        return False

    # TODO maybe try something more random
    def robotMoveRandomly(self, measurements):
        SAFETY_DISTANCE = 250
        MOVING_DISTANCE = 70
        AMOUNT_TURN = round(ROTATION_STEPS / 8)
        print("Falling back to random behaviour")
        while self.getRobotDistToObstacle() < SAFETY_DISTANCE:
            self.robotPartialRotation(AMOUNT_TURN)
        self.robotMoveForwardAnimated(MOVING_DISTANCE)

    # do full and partial rotation and collect sensor measurements
    def robotRotationMeasuring(self, myRotationSteps = ROTATION_STEPS):
        measurements = []
        for i in range(myRotationSteps):
            measurements.append(self.getRobotDistToObstacle())
            self.robotTurn(2 * math.pi / ROTATION_STEPS)
            time.sleep(ROTATION_TIME / ROTATION_STEPS)
        return measurements

    # return the distance of the robot to the next obstacle in the robot's gaze direction
    def getRobotDistToObstacle(self, cutoff = True):
        CUTOFF_VALUE = 300
        realDistance = self.environment.getDistanceToObstacle(self.robot.x, self.robot.y, self.robot.theta)
        if cutoff:
            return min(realDistance, CUTOFF_VALUE)
        return realDistance

    # just for the simulation
    def robotMoveForwardAnimated(self, distance):
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

    # move forward by bypassing actual control parameters (assuming we have inverse kinematics solved)
    def robotMoveForward(self, distance):
        self.robot.x += cos(self.robot.theta) * distance
        self.robot.y += sin(self.robot.theta) * distance

    # make the robot turn clockwise by the given amount in rad
    def robotTurn(self,amount):
        self.robot.theta += amount

    # make a partial rotation without taking measurements
    def robotPartialRotation(self, steps):
        # avoid more than one rotation
        steps = steps % ROTATION_STEPS
        if steps < ROTATION_STEPS / 2:
            for i in range(steps):
                self.robotTurn(2 * math.pi / ROTATION_STEPS)
                time.sleep(ROTATION_TIME / ROTATION_STEPS)
        else:
            # more efficient to rotate in the other direction
            for i in range(ROTATION_STEPS - steps):
                self.robotTurn(- 2 * math.pi / ROTATION_STEPS)
                time.sleep(ROTATION_TIME / ROTATION_STEPS)

    # JUST FOR TESTING
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
