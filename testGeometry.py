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
    print(calculateIntersectionRayLineSegment(ray, lineSeg))

def testParallelNoIntersection():
    p = np.array([0, 0])
    theta = math.pi / 6
    d = np.array([cos(theta), sin(theta)])
    a = np.array([2, 0])
    b = a + d
    lineSeg = LineSegment(a, b)
    ray = Ray(p, d)
    print(calculateIntersectionRayLineSegment(ray, lineSeg))

def testParallelWithIntersectionA():
    p = np.array([0, 0])
    theta = math.pi / 6
    d = np.array([cos(theta), sin(theta)])
    a = 3 * d
    b = a + d
    lineSeg = LineSegment(a, b)
    ray = Ray(p, d)
    print(calculateIntersectionRayLineSegment(ray, lineSeg))

def testParallelWithIntersectionB():
    p = np.array([0, 0])
    theta = math.pi / 6
    d = np.array([cos(theta), sin(theta)])
    a = 3 * d
    b = a - d
    lineSeg = LineSegment(a, b)
    ray = Ray(p, d)
    print(calculateIntersectionRayLineSegment(ray, lineSeg))

def testIntersectionRayQuadrangle():
    p = np.array([0, 0])
    theta = math.pi / 4
    d = np.array([cos(theta), sin(theta)])
    c1 = np.array([7, 3])
    c2 = np.array([8, 6])
    c3 = np.array([3, 5])
    c4 = np.array([5, 3])
    ray = Ray(p, d)
    quadrangle = Quadrangle(c1, c2, c3, c4)
    #expecting (True, (4, 4))
    print(calculateIntersectionRayQuadrangle(ray, quadrangle))

if __name__ == "__main__":
    #testParallelNoIntersection()
    #testParallelWithIntersectionB()
    testIntersectionRayQuadrangle()