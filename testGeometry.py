from geometry import *
from math import sin, cos
import math

def testRegular():
    x_0 = 2
    a = np.array([x_0, 0])
    b = np.array([x_0, 20])
    p = np.array([0, 0])
    theta = math.pi / 6
    d = np.array([cos(theta), sin(theta)])
    lineSeg = LineSegment(a, b)
    ray = Ray(p, d)
    print(calculateIntersection(ray, lineSeg))

def testParallelNoIntersection():
    p = np.array([0, 0])
    theta = math.pi / 6
    d = np.array([cos(theta), sin(theta)])
    a = np.array([2, 0])
    b = a + d
    lineSeg = LineSegment(a, b)
    ray = Ray(p, d)
    print(calculateIntersection(ray, lineSeg))

def testParallelWithIntersectionA():
    p = np.array([0, 0])
    theta = math.pi / 6
    d = np.array([cos(theta), sin(theta)])
    a = 3 * d
    b = a + d
    lineSeg = LineSegment(a, b)
    ray = Ray(p, d)
    print(calculateIntersection(ray, lineSeg))

def testParallelWithIntersectionB():
    p = np.array([0, 0])
    theta = math.pi / 6
    d = np.array([cos(theta), sin(theta)])
    a = 3 * d
    b = a - d
    lineSeg = LineSegment(a, b)
    ray = Ray(p, d)
    print(calculateIntersection(ray, lineSeg))

if __name__ == "__main__":
    #testParallelNoIntersection()
    testParallelWithIntersectionB()