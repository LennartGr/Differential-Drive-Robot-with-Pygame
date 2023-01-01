import threading
import time

# class inherits from Thread
class PrototypeRobot(threading.Thread):

    def __init__(self):
        # call super class constructor
        threading.Thread.__init__(self)
        self.running = True


    def run(self):
        for i in range(100, 110):
            if not self.running: 
                return
            print(i)


t1 = PrototypeRobot()



# start method is inherited by thread, calls run method
t1.start()

for j in range(10):
    print(j)
    if j == 5:
        t1.running = False