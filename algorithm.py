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

    def scannerAlgorithm(self):
        D_DOOR = 300

        dt = 0
        lasttime = datetime.now()
        while(self.running): # basically while(true)
            # time difference to last action
            dt = (datetime.now() - lasttime).total_seconds()
            lasttime = datetime.now()
            measurements = self.robotFullRotationMeasuring()
            centerLineFound = self.searchCenterLineAndMove(measurements)
            if not centerLineFound:
                self.robotMoveRandomly(measurements)
                
                        
    def detectDoor(self, measurements):   
        CUTOFF_DELTA = 500
        MIN_DOOR_INDEX_WIDTH = round(ROTATION_STEPS / 36)
        print("MEASUREMENTS")
        self.printArray(measurements)
        # TODO list of drop and increase indices
        dropIndexList = []
        increaseIndexList = []
        for i in range(ROTATION_STEPS):
            if measurements[i - 1] + CUTOFF_DELTA < measurements[i]:
                dropIndexList.append(i)
            if measurements[i] > measurements[(i + 1) % len(measurements)] + CUTOFF_DELTA:
                increaseIndexList.append(i)
        # find index of angle corresponding to door
        (doorDetected, doorStartIndex, doorEndIndex) = arrayUtils.detectDoor(dropIndexList, increaseIndexList, MIN_DOOR_INDEX_WIDTH, ROTATION_STEPS)
        if not doorDetected:
            return (False, 0)
        # door detected, calculate door middle
        indexDoorMiddle = -1
        # calculate estimated middle of the door
        if doorStartIndex < doorEndIndex:
            indexDoorMiddle = round(0.5 * (doorEndIndex + doorStartIndex))
        else:
            indexDoorMiddle = round((0.5 * (doorStartIndex + doorEndIndex + len(measurements))) % len(measurements))
        print("drop index   door index   increaseIndex", (doorStartIndex, indexDoorMiddle, doorEndIndex))
        return (doorDetected, indexDoorMiddle)

    # searches the center line by analyzing the measurements.
    # if robot already on sensor line: follow it
    # else try to navigate robot in the direction of center line
    # return false if no clue where center line is, in that case robot was not moved
    # else return true
    # TODO on center line but wall ahead
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
                (doorDetected, indexDoorMiddle) = self.detectDoor(measurements)
                if doorDetected:
                    # make the robot look to the supposed center of the door
                    print("Door detected, approaching it")
                    self.robotPartialRotation(indexDoorMiddle)
                    self.robotMoveForwardAnimated(D_DOOR)
                # ------------------------------------------------------------------------------------------------------------------------------
                else:     
                    correctionDirectionA = round(lowerWallIndex + ROTATION_STEPS / 4) % ROTATION_STEPS
                    correctionDirectionB = round(upperWallIndex + ROTATION_STEPS / 4) % ROTATION_STEPS
                    self.robotPartialRotation(min(correctionDirectionA, correctionDirectionB))
                    # check if robot needs to turn 180 degree
                    if self.getRobotDistToObstacle() < D_ML_WALL_TURN:
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

    # TODO maybe try something more random
    def robotMoveRandomly(self, measurements):
        SAFETY_DISTANCE = 100
        MOVING_DISTANCE = 70
        AMOUNT_TURN = round(ROTATION_STEPS / 8)
        print("Falling back to random behaviour")
        while self.getRobotDistToObstacle() < SAFETY_DISTANCE:
            self.robotPartialRotation(AMOUNT_TURN)
        self.robotMoveForwardAnimated(MOVING_DISTANCE)

    # just for the simulation
    def robotMoveForwardAnimated(self, distance):
        # TODO use
        
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

    # return the distance of the robot to the next obstacle in the robot's gaze direction
    def getRobotDistToObstacle(self):
        return self.environment.getDistanceToObstacle(self.robot.x, self.robot.y, self.robot.theta)

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

    def printArray(self, array):
        for i in range(0, len(array)):
            print(str(i) + "   " + str(array[i]))
