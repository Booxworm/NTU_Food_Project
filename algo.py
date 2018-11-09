from math import sqrt
import db

def getDistance(a, b):
    """
    Gets distance between two elements
    Accepts two tuples a and b, in the form (x,y)
    Returns the distance between the two, rounded to 2 dp
    """
    # a and b are tuples with 2 elements
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dist = sqrt (dx * dx + dy * dy)
    return round(dist,2)

def mergeDict(left, right, key):
    """
    Takes two lists, left and right, containing dictionaries, and merges them based on the value of their key
    Returns a sorted list
    """
    merged = []

    # While left and right list has elements
    while left and right:
        if left[0][key] < right[0][key]:
            merged.append(left[0])
            left.pop(0)
        else:
            merged.append(right[0])
            right.pop(0)

    # Left list still contain elements. Append its contents to end of the result list
    if left:
        merged.extend(left)
    else:
    # Right list still contain elements. Append its contents to end of the result list
        merged.extend(right)
    return merged

def mergesort(alist, key):
    """
    Mergesort recursively divides up the list into two, and merges the two serparate lists together
    Returns a sorted list
    """
    listLen = len(alist)
    # Base case
    if listLen < 2:
        return alist

    left = alist[:listLen // 2]
    right = alist[listLen // 2:]  # "//" to force division

    # Mergesort left and right list recursively
    left = mergesort(left, key)
    right = mergesort(right, key)
    return mergeDict(left, right, key)

def searchByFood(food, alist=db.readFile()):
    """
    Searches through a list of canteens, and filters out the canteens which do not contain any of the food
    Accepts a list of food names, and an optional argument list of canteens
    Returns the filtered list of canteens
    """
    # Iterates through the list to filter out the items based on food
    temp = []
    for canteen in alist:
        temp2 = {}
        for k,v in canteen['food'].items():
            if ''.join(k.split('_')) in food:
                temp2[k] = v
        if len(temp2):
            canteen['food'] = temp2
            temp.append(canteen)
    return temp

def searchByPrice(lower, upper, alist=db.readFile()):
    """
    Searches through a list of canteens, and filters out the canteens which do not contain food within the price range
    Accepts a price range, and an option argument list of canteens
    Returns the filtered list of canteens
    """
    # Iterates through the list to filter out the items based on food
    lower = lower if lower else float('-inf')
    upper = upper if upper else float('inf')
    temp = []
    for canteen in alist:
        temp2 = {}
        for k,v in canteen['food'].items():
            if lower <= v <= upper:
                temp2[k] = v
        if len(temp2):
            canteen['food'] = temp2
            temp.append(canteen)
    return temp

def sortByDist(userLocation, canteens=db.readFile()):
    """
    Gets the distance between the user's location and each of the canteens
    Accepts userLocation as tuple (x,y), and optional argument list of canteens
    Returns a sorted list of canteens sorted by distances, in ascending order
    """
    dist = []
    for canteen in canteens:
        dist = getDistance(userLocation,canteen['coords'])
        canteen['dist'] = dist
    return mergesort(canteens, 'dist')

def sortByRank(canteens=db.readFile()):
    """
    Sorts the list of canteens by rank
    Accepts optional argument list of canteens
    Returns a sorted list of canteens
    """
    return mergesort(canteens, 'rank')
