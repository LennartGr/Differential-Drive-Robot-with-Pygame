import environment
import math

env = environment.Environment()

OneDegInRad = math.pi * 2 / 360
distClosest = env.getDistanceToObstacleWithIntersection(x = 600, y = 250, theta = math.pi / 2)
distSlightlyBigger = env.getDistanceToObstacleWithIntersection(x = 600, y = 250, theta = math.pi / 2 + OneDegInRad)
print(distClosest)
print(distSlightlyBigger)