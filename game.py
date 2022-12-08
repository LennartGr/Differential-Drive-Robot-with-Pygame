import pygame
import math
from math import sin, cos
import numpy as np
import difDriveRobot as robot
import geometry as geo

BLUE = (0, 0, 255)
GREY = (100, 100, 100)

def main():
    global screen, robotImage, myRobot, rectangles

    pygame.init()
    WIDTH = 1000
    HEIGHT = 750
    screen  = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Differential Drive Robot Simulation")
    running = True

    myRobotLength = 20
    myRobotWheelRadius = 4
    myRobot = robot.DifDriveRobot(r = myRobotWheelRadius, l = myRobotLength, )
    robotImage = pygame.image.load('robot.png')
    rectangles = []
    initRectangles()

    #robot position and wheel velocities
    x = 250
    y = 250
    v_l = 0
    v_r = 0
    theta = 0    
    #delta time in seconds
    dt = 0
    lasttime=pygame.time.get_ticks()

    #main loop
    while running:
        step = 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #change velocities according to keypress
            if event.type == pygame.KEYDOWN and event.key==pygame.K_s:
                v_l -= step
            if event.type == pygame.KEYDOWN and event.key==pygame.K_w:
                v_l += step
            if event.type == pygame.KEYDOWN and event.key==pygame.K_d:
                v_r -= step
            if event.type == pygame.KEYDOWN and event.key==pygame.K_e:
                v_r += step   
            if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                v_r = 0
                v_l = 0
            

        print('v_l={:d}, v_r={:d}'.format(v_l, v_r))

        
        dt = (pygame.time.get_ticks() - lasttime) / 1000 #dt in seconds
        lasttime=pygame.time.get_ticks()
        new_position = myRobot.move(v_l, v_r, x, y, theta, dt)
        x = new_position[0, 0]
        y = new_position[1, 0]
        theta = new_position[2, 0]
        print("theta={:f}".format(theta))
        #print(pygame.time.get_ticks())

        drawRectangles()
        drawRobot(myRobotLength, x, y, theta)
        emitRays(x, y, theta)
        pygame.display.update()
        

def drawRobot(length, x, y, theta):
    radius = length
    #pygame.draw.circle(screen, BLUE, (x, y), radius)
    screen.fill(GREY)
    theta_deg = theta * 360 / (2 * math.pi)
    #we want to rotate clockwise, so use -theta_deg
    rotatedImage = pygame.transform.rotate(robotImage, -theta_deg)
    #some magic to ensure the center doesn't change when rotating
    new_rect = rotatedImage.get_rect(center = robotImage.get_rect(center = (x, y)).center)
    screen.blit(rotatedImage, new_rect)

def initRectangles():
    rectangles.append(geo.RectAsQuadrangle(x_min = 100, x_max = 200, y_min = 100, y_max = 500))

def drawRectangles():
    color = (255,0,0)
    # Drawing Rectangle
    for rectangle in rectangles:
        x_top = rectangle.c1[0]
        y_top = rectangle.c1[1]
        width =  rectangle.c3[0] - rectangle.c1[0]
        height = rectangle.c2[1] - rectangle.c1[1]
        pygame.draw.rect(screen, color, pygame.Rect(x_top, y_top, width, height))
    pygame.display.flip()
    

def emitRays(x, y, theta):
    lineColor = (0, 255, 0)
    lineColorIntersection = (0, 0, 255)
    noIntersectionLineLength = 200
    ray = geo.RayFromPointAndAngle(np.array([x, y]), theta)
    for rectangle in rectangles:
        (intersect, (x_intersection, y_intersection)) = geo.calculateIntersectionRayQuadrangle(ray, rectangle)
        #TODO if intersect
        if intersect:
            print((x_intersection, y_intersection))
            pygame.draw.line(screen, lineColorIntersection, (x, y), (x_intersection, y_intersection))
        else:
            x_end = x + cos(theta) * noIntersectionLineLength
            y_end = y + sin(theta) * noIntersectionLineLength
            pygame.draw.line(screen, lineColor, (x, y), (x_end, y_end))



    pygame.display.flip()



if __name__ == '__main__':
    main()