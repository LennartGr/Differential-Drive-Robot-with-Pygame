import pygame
import math
import difDriveRobot as robot

BLUE = (0, 0, 255)
GREY = (100, 100, 100)

def main():
    global screen, robotImage

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
        #really dirty hack to deal with different coordinate system of pygame
        #swith v_l and v_r
        new_position = myRobot.move(v_r, v_l, x, y, theta, dt)
        x = new_position[0, 0]
        y = new_position[1, 0]
        theta = new_position[2, 0]
        print(theta)
        #print(pygame.time.get_ticks())

        drawRobot(myRobotLength, x, y, -theta)
        pygame.display.update()
        

def drawRobot(length, x, y, theta):
    radius = length
    #pygame.draw.circle(screen, BLUE, (x, y), radius)
    screen.fill(GREY)
    theta_deg = theta * 360 / (2 * math.pi) 
    rotatedImage = pygame.transform.rotate(robotImage, theta_deg)
    #some magic to ensure the center doesn't change when rotating
    new_rect = rotatedImage.get_rect(center = robotImage.get_rect(center = (x, y)).center)
    screen.blit(rotatedImage, new_rect)

if __name__ == '__main__':
    main()