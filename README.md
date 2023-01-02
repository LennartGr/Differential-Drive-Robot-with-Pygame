## Differential Drive Robot in Python

To start the simulation, run `main.py`.

Current state: You can use the keyboard to make the robot move. Unit of speed: pixel per second.
The current control variables and the robot's angle in rad are displayed in the window caption.
- left wheel +1 forward: W
- left wheel -1 forward: S
- right wheel +1 forward: E
- right wheel -1 forward: D

To add another rectangle-like obstacle to the map, modify the method `initRectangles()` of `environment.py`.

The robot's movement is determined by an algorithm object that runs in a seperate thread.
The algorithm is allowed to fetch to distance of the robot to the nearest obstacle of the environment.
