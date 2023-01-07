import geometry as geo
import math
import numpy as np

# state holder for obstacles in the map
# doesn't need to know any other component
class Environment:

    WIDTH = 1200
    HEIGHT = 500
    WALL_SIZE = 20
    # constants of the door. (x, y) is top left corner of emptiness
    DOOR_X = 1000
    DOOR_Y = 150
    DOOR_WIDTH = 100
    # table constants
    TABLE_HEIGHT = 80
    TABLE_WIDTH = 200
    TABLE_LEG_LENGTH = 15

    def __init__(self):
        self.rectangles = []
        self.initSimpleMap()
        # self.drawFourTables(40, 40, 500)

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
        self.rectangles.append(geo.RectAsQuadrangle(600, 650, 100, 500))

    def initSimpleMap(self):
        # right
        self.rectangles.append(geo.RectAsQuadrangle(0, self.WALL_SIZE, 0, self.HEIGHT))
        # top
        self.rectangles.append(geo.RectAsQuadrangle(0, self.WIDTH, 0, self.WALL_SIZE))
        # left
        self.rectangles.append(geo.RectAsQuadrangle(self.WIDTH - self.WALL_SIZE, self.WIDTH, 0, self.HEIGHT))
        # bottom
        self.rectangles.append(geo.RectAsQuadrangle(0, self.WIDTH, self.HEIGHT - self.WALL_SIZE, self.HEIGHT))
        # door, always on the right. upper part
        self.rectangles.append(geo.RectAsQuadrangle(self.DOOR_X, self.DOOR_X + self.WALL_SIZE, 0, self.DOOR_Y))
        # door, lower part
        self.rectangles.append(geo.RectAsQuadrangle(self.DOOR_X, self.DOOR_X + self.WALL_SIZE, self.DOOR_Y + self.DOOR_WIDTH, self.HEIGHT))

    def drawFourTables(self, gapX, gapY, gapSecondX):
        self.drawTableLegs(gapX, gapY, self.TABLE_LEG_LENGTH, self.TABLE_HEIGHT, self.TABLE_WIDTH)
        self.drawTableLegs(gapX, self.HEIGHT - gapY - self.TABLE_HEIGHT, self.TABLE_LEG_LENGTH, self.TABLE_HEIGHT, self.TABLE_WIDTH)
        self.drawTableLegs(gapSecondX, gapY, self.TABLE_LEG_LENGTH, self.TABLE_HEIGHT, self.TABLE_WIDTH)
        self.drawTableLegs(gapSecondX, self.HEIGHT - gapY - self.TABLE_HEIGHT, self.TABLE_LEG_LENGTH, self.TABLE_HEIGHT, self.TABLE_WIDTH)
        

    # draw four legs of table that is aligned with coordinate system
    def drawTableLegs(self, x, y, tableLegLength, tableHeight, tableWidth):
        # top left
        self.rectangles.append(geo.RectAsQuadrangle(x, x + tableLegLength, y, y + tableLegLength))
        # top right
        self.rectangles.append(geo.RectAsQuadrangle(x + tableWidth - tableLegLength, x + tableWidth, y, y + tableLegLength))
        # bottom left
        self.rectangles.append(geo.RectAsQuadrangle(x, x + tableLegLength, y + tableHeight - tableLegLength, y + tableHeight))
        # bottom right
        self.rectangles.append(geo.RectAsQuadrangle(x + tableWidth - tableLegLength, x + tableWidth, y + tableHeight - tableLegLength, y + tableHeight))
