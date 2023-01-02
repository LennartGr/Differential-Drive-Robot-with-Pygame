import geometry as geo
import math
import numpy as np

# state holder for obstacles in the map
# doesn't need to know any other component
class Environment:

    def __init__(self):
        self.rectangles = []
        self.initRectangles()

    # calculates the distance to the closest obstacle from the position (x,y)
    # with gaze direction indicated by the angle theta
    # returns (distance, (x_intersection, y_intersection)) as nested tuple
    # if there is no intersection, distance == math.inf
    def getDistanceToObstacleWithIntersection(self, x, y, theta):
        shortestDistance = math.inf
        (shortest_x_intersection, shortest_y_intersection) = (0, 0)
        ray = geo.RayFromPointAndAngle(np.array([x, y]), theta)
        for rectangle in self.rectangles:
            (intersect, (x_intersection, y_intersection)) = geo.calculateIntersectionRayQuadrangle(ray, rectangle)
            if intersect:
                # update shortest distance if necessary
                distanceToIntersectionPoint = np.linalg.norm(np.array([x, y]) - np.array([x_intersection, y_intersection]))
                if distanceToIntersectionPoint < shortestDistance:
                    shortestDistance = distanceToIntersectionPoint
                    shortest_x_intersection = x_intersection
                    shortest_y_intersection = y_intersection
        return (shortestDistance, (shortest_x_intersection, shortest_y_intersection))

    # method to be called by the algorithm who shall only get the distance, not the intersection point
    def getDistanceToObstacle(self, x, y, theta):
        (shortestDistance, (x_intersection, y_intersection)) = self.getDistanceToObstacleWithIntersection(x, y, theta)
        return shortestDistance

    # Method to create initialize rectangle obstacles
    def initRectangles(self):
        # Use this line as reference on how to create rectangles
        self.rectangles.append(geo.RectAsQuadrangle(x_min = 100, x_max = 200, y_min = 100, y_max = 500))
        self.rectangles.append(geo.RectAsQuadrangle(300, 350, 100, 500))