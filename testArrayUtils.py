from arrayUtils import *

testArr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 103]
print(getIndicePairsWithValueDistance(testArr, 100, 1))

# test door detection
# basic case
dropIndexList = [1, 10, 359]
increaseIndexList = [2, 20]
(doorDetected, di, ii) = detectDoor(dropIndexList, increaseIndexList, 10, 360)
print((doorDetected, di, ii))
assert (doorDetected, di, ii) == (True, 10, 20)

# check gap is well minded
(doorDetected, di, ii) = detectDoor(dropIndexList, increaseIndexList, 11, 360)
assert not doorDetected

# check that next increase index is demanded
dropIndexList = [1, 10, 359]
increaseIndexList = [2, 11, 20]
(doorDetected, di, ii) = detectDoor(dropIndexList, increaseIndexList, 10, 360)
assert not doorDetected

# case door in sight
dropIndexList = [5, 6, 7, 9]
increaseIndexList = [4, 8]
(doorDetected, di, ii) = detectDoor(dropIndexList, increaseIndexList, 5, 10)
assert (doorDetected, di, ii) == (True, 9, 4)
