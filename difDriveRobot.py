import numpy as np
from math import sin, cos

# kinematics plus state for x, y, theta (in rad) and robot radius
# radius is just for display purposes, assuming a round robot
class DifDriveRobot:

    def __init__(self, r = 1, l = 1, x = 100, y = 100, theta = 0, robotRadius = 20) -> None:
        self.kinematics = DifDriveRobotKinematics(r, l)
        self.x = x
        self.y = y
        self.theta = theta
        self.robotRadius = robotRadius

    def move(self, v_l, v_r, delta_time):        
        new_position = self.kinematics.move(v_l, v_r, self.x, self.y, self.theta, delta_time)
        self.x = new_position[0, 0]
        self.y = new_position[1, 0]
        self.theta = new_position[2, 0]
        return new_position

    
# this class implements the kinematics of a dif drive robot
class DifDriveRobotKinematics:

    # r: radius of each wheel
    # l: space between the two wheels
    def __init__(self, r = 1, l = 1):
        self.r = r
        self.l = l

    # v_l and v_r: left and right wheel velocities in pixel per second
    # (x, y) start coordinates
    # theta: angle in rad with respect to x-axis
    # delta_time: time duration in sec the movement shall be executed for
    # return: [x_prime, y_prime, theta_prime] the new position and angle as a column vector (numpy matrix)
    def moveClassical(self, v_l, v_r, x, y, theta, delta_time):
        epsilon = 0.05
        #case 1: approximately same wheel speed. 
        #Treat this case seperately to avoid division by zero
        if abs(v_r - v_l) < epsilon:
            #taking velocity of v_r
            hypothenuse = delta_time * v_r
            return np.mat([[x + cos(theta) * hypothenuse], [y + sin(theta) * hypothenuse], [theta]])

        #case 2: different wheel speeds
        #see https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjUpp2Dosb7AhWqQ6QEHalVBpcQFnoECA0QAQ&url=https%3A%2F%2Fwww.cs.columbia.edu%2F~allen%2FF17%2FNOTES%2Ficckinematics.pdf&usg=AOvVaw31cwbIU3gIxtxcDbsDjAkL
        w = (v_r - v_l) / self.l
        R = (self.l / 2) * (v_r + v_l) / (v_r - v_l)
        V = (v_r + v_l) / 2
        w_r = v_r / self.r
        w_l = v_l / self.r
        ICC_x = x - R * sin(theta)
        ICC_y = y + R * cos(theta)
        tmp = w * delta_time
        rotation_matrix = np.mat([[cos(tmp), -sin(tmp), 0], [sin(tmp), cos(tmp), 0], [0, 0, 1]])
        a = np.mat([[x - ICC_x], [y - ICC_y], [theta]])
        b = np.mat([[ICC_x], [ICC_y], [tmp]])
        return rotation_matrix * a + b

    #for pygame type coordinate system where origin is top left corner
    def move(self, v_l, v_r, x, y, theta, delta_time):
        #the pygmame type coordinate system means mirroring the original one by the x-axis,
        #so we can simply switch v_l and v_r
        return self.moveClassical(v_r, v_l, x, y, theta, delta_time)