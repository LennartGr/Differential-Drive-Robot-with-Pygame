## Differential Drive Robot in Python

To start the simulation, run `game.py`.

Current state: You can use the keyboard to make the robot move. Unit of speed: pixel per second.
The current control variables and the robot's angle in rad are displayed in the window caption.
- left wheel +1 forward: W
- left wheel -1 forward: S
- right wheel +1 forward: E
- right wheel -1 forward: D

To add another rectangle-like obstacle to the map, modify the method `initRectangles()` of `game.py`.

To run an algorithm instead of the manual control, 
adapt the parameters `v_l` and `v_r` inside `main()` of `game.py` dependent of the sensor data.
The last fetched sensor data is contained in the variable `distance`.
