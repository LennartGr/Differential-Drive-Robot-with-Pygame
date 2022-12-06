import numpy as np
from math import sin, cos

class DifDriveRobot:

    #r: radius of each wheel
    #l: space between the two wheels
    def __init__(self, r = 1, l = 1):
        self.r = r
        self.l = l

    #v_l and v_r: left and right wheel velocities in pixel per second
    #start = (x, y) start coordinates
    #return: [x_prime, y_prime, phi_prime] as column vector (numpy matrix)
    def move(self, v_l, v_r, x, y, theta, delta_time):
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


if __name__ == "__main__":
    myDrive = DifDriveRobot()
    v_l = 1
    v_r = 1
    result = myDrive.move(v_l, v_r, 0, 0, 0, 1)
    print(result)
    print(result.tolist())
    x = result[0, 0]
    print(type(x))
    print(y)
    print(theta)