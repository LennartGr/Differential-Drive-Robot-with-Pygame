import numpy as np

class LineSegment:
    def __init__(self, a, b):
        #numpy arrays
        self.a = a
        self.b = b

class Ray:
    def __init__(self, p, d):
        #numpy arrays
        self.p = p
        self.d = d

def calculateIntersection(ray, lineSegment):
    d_prime = np.array([-ray.d[1], ray.d[0]])
    #attention: division by zero possible
    t_line = np.dot(d_prime, ray.p - lineSegment.a) / np.dot(d_prime, lineSegment.b - lineSegment.a)
    t_ray = np.dot(- ray.p + lineSegment.a + t_line * (lineSegment.b - lineSegment.a), ray.d)
    if t_ray >= 0 and t_line >= 0 and t_line <= 1:
        intersectionPoint = lineSegment.a + t_line * (lineSegment.b - lineSegment.a)
        return (True, intersectionPoint)
    else:
        return (False, np.array([0, 0]))
    

