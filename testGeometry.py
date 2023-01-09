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

def testCorrectIntersectionPoint():
    rect = RectAsQuadrangle(0, 1000, 500 - 20, 500)
    ray = RayFromPointAndAngle(np.array([600, 250]), math.pi / 2)
    print(calculateIntersectionRayQuadrangle(ray, rect))

    lineSegment = LineSegment(np.array([0, 480]), np.array([1000, 480]))
    print(calculateIntersectionRayLineSegment(ray, lineSegment))

def testForNoIntersectionPoint():
    rect = RectAsQuadrangle(1000, 1200, 250, 500)
    ray = RayFromPointAndAngle(np.array([600, 250]), math.pi)
    (intersection, point) = calculateIntersectionRayQuadrangle(ray, rect)
    assert intersection == False

    
def testDistPointLineSegment():
    epsilon = 0.000001
    point = np.array([0, 0])

    l1 = LineSegment(np.array([-1, 0]), np.array([1, 0]))
    (dist, proj) = calculateDistancePointLineSegment(point, l1)
    assert dist == 0

    l2 = LineSegment(np.array([-1, 1]), np.array([10, 1]))
    (dist, proj) = calculateDistancePointLineSegment(point, l2)
    assert dist == 1
    assert areEqual(proj, np.array([0, 1]))

    l3 = LineSegment(np.array([3, 1]), np.array([4, 1]))
    (dist, proj) = calculateDistancePointLineSegment(point, l3)
    assert dist == math.sqrt(pow(3, 2) + pow(1, 2))
    assert areEqual(proj, np.array([3, 1]))

def areEqual(pointA, pointB):
    epsilon = 0.0000001
    return np.linalg.norm(pointA - pointB) < epsilon

if __name__ == "__main__":
    #testParallelNoIntersection()
    #testParallelWithIntersectionB()
    # testIntersectionRayQuadrangle()
    testForNoIntersectionPoint()
    testDistPointLineSegment()