import math
from math import tan

class LinearFunction:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta
        epsilon = 0.005
        self.vertical = False
        if abs(abs(theta) - math.pi / 2) < epsilon:
            self.vertical = True
            self.m = math.nan
            self.b = math.nan
            return
        #attention: theta 0.5 pi or -0.5 pi
        self.m = tan(theta)
        self.b = y - x * self.m
        print(self.m)
        print(self.b)

    def evaluateAt(self, x):
        if self.vertical:
            return self.y
        return self.b + x * self.m

    #call only if m not 0
    def getX(self, y):
        return (y - self.b) / self.m

class Rectangle:
    def __init__(self, minX, minY, maxX, maxY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY

#return intersection point of linear function and rectangle if it exists
def findIntersection(linearFunction, rectangle):
    return findIntersectionHelper(linearFunction, rectangle.minX, rectangle.minY, rectangle.maxX, rectangle.maxY) 


def findIntersectionHelper(linearFunction, minX, minY, maxX, maxY):
    #check left side of rectangle
    y_left = linearFunction.evaluateAt(minX)
    if inBetween(y_left, minX, maxX):
        return (True, (minX, y_left))
    #check right side of rectangle
    y_right = linearFunction.evaluateAt(maxX)
    if inBetween(y_right, minX, maxX):
        return (True, (maxX, y_right))
    if linearFunction.m == 0:
        return (False, (0, 0))
    x_bottom = linearFunction.getX(minY)
    if inBetween(x_bottom, minY, maxX):
        return (True, (x_bottom, minY))
    x_top = linearFunction.getX(maxY)
    if inBetween(x_top, minY, maxX):
        return (True, (x_top, maxY))
    #no intersection
    return (True, (maxX, y_right))

def inBetween(x, a, b):
    return x >= a and x <= b


if __name__ == '__main__':
    linfun = LinearFunction(1, 1, math.pi / 6)
    rect = Rectangle(10, 0, 12, 20)
    (doesIntersect, (x, y)) = findIntersection(linfun, rect)
