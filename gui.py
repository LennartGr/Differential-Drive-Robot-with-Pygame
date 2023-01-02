import pygame
import math
from math import sin, cos
import difDriveRobot as robot
import environment

BLUE = (0, 0, 255)
GREY = (100, 100, 100)
RECT_COLOR = (255,0,0)
RAY_COLOR = (0, 255, 0)
RAY_COLOR_INTERSECTION = (0, 0, 255)
NO_INTERSECTION_RAY_LENGTH = 200

# displays the robot and the environment
class GUI:

    # width and height are determined by the environment
    WIDTH = 0
    HEIGHT = 0
    ROBOT_IMAGE = pygame.image.load('robot.png')

    def __init__(self, robot, environment):
        self.robot = robot
        self.environment = environment
        self.WIDTH = environment.WIDTH
        self.HEIGHT = environment.HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def display(self):
        running = True
        while running:
            # exit on close
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("Stop GUI")
            shortestDistance = self.drawSensorRay()
            self.drawRobot()
            self.drawEnvironment()
            self.updateCaption(shortestDistance)
    
    def updateCaption(self, shortestDistance):
        caption = "Differential Drive Robot Simulation:    "
        xDisp = str(round(self.robot.x, 2))
        yDisp = str(round(self.robot.y, 2))
        thetaDisp = str(round(self.robot.theta, 2))
        distanceDisp = str(round(shortestDistance, 2))
        caption += "x = " + xDisp + ", y = " + yDisp + ", theta: " + thetaDisp
        caption += ", distance: " + distanceDisp
        pygame.display.set_caption(caption)
    
            

    def drawRobot(self):
        radius = self.robot.robotRadius
        x = self.robot.x
        y = self.robot.y
        theta = self.robot.theta
        self.screen.fill(GREY)
        theta_deg = theta * 360 / (2 * math.pi)
        #we want to rotate clockwise, so use -theta_deg
        rotatedImage = pygame.transform.rotate(self.ROBOT_IMAGE, -theta_deg)
        #some magic to ensure the center doesn't change when rotating
        new_rect = rotatedImage.get_rect(center = self.ROBOT_IMAGE.get_rect(center = (x, y)).center)
        self.screen.blit(rotatedImage, new_rect)

    def drawEnvironment(self):
        # Drawing Rectangle
        for rectangle in self.environment.rectangles:
            x_top = rectangle.c1[0]
            y_top = rectangle.c1[1]
            width =  rectangle.c3[0] - rectangle.c1[0]
            height = rectangle.c2[1] - rectangle.c1[1]
            pygame.draw.rect(self.screen, RECT_COLOR, pygame.Rect(x_top, y_top, width, height))
        pygame.display.flip()
        
    # makes the robot emit a ray in gaze direction.
    # returns the closest distance to an obstacle
    def drawSensorRay(self):
        (shortestDistance, (x_intersection, y_intersection)) = self.environment.getDistanceToObstacleWithIntersection(self.robot.x, self.robot.y, self.robot.theta)
        # case 1: there is some intersecton
        if shortestDistance < math.inf:
            pygame.draw.line(self.screen, RAY_COLOR_INTERSECTION, (self.robot.x, self.robot.y), (x_intersection, y_intersection))
        # case 2: there is no intersection
        else:
            x_end = self.robot.x + cos(self.robot.theta) * NO_INTERSECTION_RAY_LENGTH
            y_end = self.robot.y + sin(self.robot.theta) * NO_INTERSECTION_RAY_LENGTH
            pygame.draw.line(self.screen, RAY_COLOR, (self.robot.x, self.robot.y), (x_end, y_end))
        # update display
        pygame.display.flip()
        return shortestDistance
