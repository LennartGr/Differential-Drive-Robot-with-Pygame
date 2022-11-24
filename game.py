import pygame
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

    robotImage = pygame.image.load('robot.png')

    #robot position
    x = 100
    y = 100
    theta = 0    
    #delta time in seconds
    dt = 0
    lasttime=pygame.time.get_ticks()
    #main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        dt = (pygame.time.get_ticks() - lasttime) / 1000 #dt in seconds
        lasttime=pygame.time.get_ticks()
        vel = 100 #pixel per second
        x = x + vel * dt
        theta += 0.1
        print(pygame.time.get_ticks())

        drawRobot(x, y, theta)
        pygame.display.update()
        

def drawRobot(x, y, theta):
    radius = 20
    #pygame.draw.circle(screen, BLUE, (x, y), radius)
    screen.fill(GREY)
    rotatedImage = pygame.transform.rotate(robotImage, theta)
    #some magic to ensure the center doesn't change when rotating
    new_rect = rotatedImage.get_rect(center = robotImage.get_rect(center = (x, y)).center)
    screen.blit(rotatedImage, new_rect)

if __name__ == '__main__':
    main()