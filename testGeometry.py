from geometry import *
from math import sin, cos
import math

x_0 = 2
a = np.array([x_0, 0])
b = np.array([x_0, 20])
p = np.array([0, 0])
theta = math.pi / 6
d = np.array([cos(theta), sin(theta)])
lineSeg = LineSegment(a, b)
ray = Ray(p, d)
print(calculateIntersection(ray, lineSeg))