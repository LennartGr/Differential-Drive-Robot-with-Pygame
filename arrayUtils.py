
# returns all the pairs (i, j) with i < j where || array[i] - array[j] | - difference | < tolerance
def getIndicePairsWithValueDistance(myArray, searchedDistance, tolerance):
    pairsList = []
    for i in range(len(myArray)):
        for j in range(i + 1, len(myArray)):
            distance = abs(myArray[i] - myArray[j])
            if abs(distance - searchedDistance) <= tolerance:
                pairsList.append((i, j))
    return pairsList