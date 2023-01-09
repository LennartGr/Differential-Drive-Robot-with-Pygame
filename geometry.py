import numpy as np
import math
from math import sin, cos

class LineSegment:

    def __init__(self, a, b):
        #numpy arrays
        self.a = a
        self.b = b

class Ray:

    #if you want direction d from some angle theta:
    #Use d = np.array([cos(theta), sin(theta)])
    def __init__(self, p, d):
        #numpy arrays
        self.p = p
        self.d = d

def RayFromPointAndAngle(p, theta):
    return Ray(p, d = np.array([cos(theta), sin(theta)]))

class Quadrangle:
    
    #corner points. Line segments are c1c2, c2c3, c3c4, c4d1
    def __init__(self, c1, c2, c3, c4):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

#construct special quadrangle, namely an axis-aligned rectangle
def RectAsQuadrangle(x_min, x_max, y_min, y_max):
    c1 = np.array([x_min, y_min])
    c2 = np.array([x_min, y_max])
    c3 = np.array([x_max, y_max])
    c4 = np.array([x_max, y_min])
    return Quadrangle(c1, c2, c3, c4)

# point as np.array
# return (dist to closest point on segment, closest point on segment)
def calculateDistancePointLineSegment(point, lineSegment):
    # d is direction vector from a to b, the two points defining the line segment
    d = lineSegment.b - lineSegment.a
    d = d / np.linalg.norm(d)
    # let the projection v = a + t * d be the projection of point to the LINE defined by the line segment
    # calculate t by
    t = np.dot(point, d) - np.dot(lineSegment.a, d)
    projection = lineSegment.a + t * d
    # check if v is actually on the line segment. If not, the point is closest to one of the ends
    if t < 0 or t > np.linalg.norm(lineSegment.b - lineSegment.a):
        # projection not on the line segment
        distPointToA = np.linalg.norm(point - lineSegment.a)
        distPointToB = np.linalg.norm(point - lineSegment.b)
        if (distPointToA < distPointToB):
            return (distPointToA, lineSegment.a)
        else:
            return (distPointToB, lineSegment.b)
    # projection lies on the line segment
    return (np.linalg.norm(point - projection), projection)


#Return (boolIntersection, intersectionPoint)
#if there are multiple intersection points, return the closest one in terms of the ray's parameter p
def calculateIntersectionRayLineSegment(ray, lineSegment):
    # case one: ray.p already on line segment. distance zero
    (dist, projection) = calculateDistancePointLineSegment(ray.p, lineSegment)
    if dist == 0:
        return (0, projection)
    # other cases: p not on line segment
    d_prime = np.array([-ray.d[1], ray.d[0]])
    denominator = np.dot(d_prime, lineSegment.b - lineSegment.a)
    #treat special case first: denominator close to zero. ray and line segment are parallel
    epsilon = 0.005
    if abs(denominator) < epsilon: 
        # do this to avoid division by close to zero
        if (np.linalg.norm(ray.p - lineSegment.a)) <= epsilon:
            return (True, lineSegment.a)
        
        # vector from p to a
        comparison_direction = (lineSegment.a - ray.p)
        comparison_direction = comparison_direction / np.linalg.norm(comparison_direction)
        # check if comparison direction and ray direction are EQUAL 
        # if they are opposite to each other, there is no intersection !!!
        if np.linalg.norm(ray.d - comparison_direction) < epsilon:
            # because p doesn't lie on the segment, it is closest to one of the end points
            dist_a = np.linalg.norm(lineSegment.a - ray.p)
            dist_b = np.linalg.norm(lineSegment.b - ray.p)
            if dist_a <= dist_b:
                return (True, lineSegment.a)
            else:
                return (True, lineSegment.b)
        else:
            #not alligned, no intersection
            return (False, np.array([0, 0]))
        

    #regular case: lineSegment direction and ray direction not parallel
    t_line = np.dot(d_prime, ray.p - lineSegment.a) / denominator
    t_ray = np.dot(- ray.p + lineSegment.a + t_line * (lineSegment.b - lineSegment.a), ray.d)
    if t_ray >= 0 and t_line >= 0 and t_line <= 1:
        intersectionPoint = lineSegment.a + t_line * (lineSegment.b - lineSegment.a)
        return (True, intersectionPoint)
    else:
        return (False, np.array([0, 0]))

def calculateIntersectionRayQuadrangle(ray, quadrangle):
    #build all line segments of rectangle and calc intersection
    l1 = LineSegment(quadrangle.c1, quadrangle.c2)
    l2 = LineSegment(quadrangle.c2, quadrangle.c3)
    l3 = LineSegment(quadrangle.c3, quadrangle.c4)
    l4 = LineSegment(quadrangle.c4, quadrangle.c1)
    lineSegmentList = [l1, l2, l3, l4]
    intersection = False
    intersectionPoint = np.array([0, 0])
    for lineSegment in lineSegmentList:
        (segmentIntersects, segmentIntersectionPoint) = calculateIntersectionRayLineSegment(ray, lineSegment)
        if segmentIntersects:
            #is this the first intersection we found?
            if not intersection:
                intersection = True
                intersectionPoint = segmentIntersectionPoint
            #if this is not the first intersection we found, is it better then the previous ones (i.e. closer)?
            elif np.linalg.norm(ray.p - segmentIntersectionPoint) < np.linalg.norm(ray.p - intersectionPoint):
                intersectionPoint = segmentIntersectionPoint
    return (intersection, intersectionPoint)


            

    

