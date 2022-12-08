import numpy as np

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

#Return (boolIntersection, intersectionPoint)
#if there are multiple intersection points, return the closest one in terms of the ray's parameter p
def calculateIntersection(ray, lineSegment):
    d_prime = np.array([-ray.d[1], ray.d[0]])
    denominator = np.dot(d_prime, lineSegment.b - lineSegment.a)
    #treat special case first: denominator close to zero
    epsilon = 0.005
    if abs(denominator) < epsilon:        
        if (np.linalg.norm(ray.p - lineSegment.a)) <= epsilon:
            return (True, lineSegment.a)
        #case 1.1: lineSegment parallel, but not aligned. No intersection
        #no division by zero possible
        comparison_direction = (ray.p - lineSegment.a) / (np.linalg.norm(ray.p - lineSegment.a))
        #check if comparison direction and ray direction are equal are opposite to each other
        if np.linalg.norm(ray.d - comparison_direction) < epsilon or np.linalg.norm(ray.d + comparison_direction) < epsilon:
            dist_a = np.linalg.norm(ray.p - lineSegment.a)
            dist_b = np.linalg.norm(ray.p - lineSegment.b)
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
    

