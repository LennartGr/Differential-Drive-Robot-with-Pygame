
# returns all the pairs (i, j) with i < j where || array[i] - array[j] | - difference | < tolerance
def getIndicePairsWithValueDistance(myArray, searchedDistance, tolerance):
    pairsList = []
    for i in range(len(myArray)):
        for j in range(i + 1, len(myArray)):
            distance = abs(myArray[i] - myArray[j])
            if abs(distance - searchedDistance) <= tolerance:
                pairsList.append((i, j))
    return pairsList

# find the first (i, j) with i drop index, j increase index such that i and j have the min required gap and j is the first increase index higher than i
def detectDoor(dropIndexList, increaseIndexList, minRequiredGap, rotationSteps):
    # special case checked first: do we start by looking at the center of the door?
    # only the very last drop index is a candidate with the very first increase index
    singleDropIndex = len(dropIndexList) == 1
    dropIndex = dropIndexList[-1]
    increaseIndex = increaseIndexList[0]
    # condition:
    # 1. really this case
    # 2. gap is respected
    # 3. no other drop index in between
    if (dropIndex > increaseIndex) and ((dropIndex - rotationSteps + minRequiredGap) <= increaseIndex) and (singleDropIndex or (increaseIndex < dropIndexList[0])):
        return (True, dropIndex, increaseIndex) 
    # regular case : we do not start by looking at the door
    # thus increaseIndex < dropIndex
    for i in range(len(dropIndexList)):
        dropIndex = dropIndexList[i]
        for increaseIndex in increaseIndexList:
            # found the first bigger increase index
            if dropIndex <= increaseIndex:
                # check if the gap is big enough and that there is no other drop index in between
                # TODO check that there is no other drop index in between (special case only one dropIndex)
                # if dropIndex + minRequiredGap <= increaseIndex and increaseIndex < dropIndexList[i + 1]:
                # condition: 1. gap is respected, 2. no other drop index in between
                if dropIndex + minRequiredGap <= increaseIndex:
                    # check no drop index in between
                    if (i < (len(dropIndexList) - 1)) and (increaseIndex < dropIndexList[i + 1]): 
                        return (True, dropIndex, increaseIndex)
                    elif i == (len(dropIndexList) -1):
                        # very last drop index
                        return (True, dropIndex, increaseIndex)
                break
    # nothing found
    return (False, 0, 0)
