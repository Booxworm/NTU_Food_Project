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

def searchDict(dict, searchTerm, searchByKey=True):
    """
    Linearly searches through a dictionary, to see if the dict contains the searchTerm
    If searchByKey flag is set, searches through keys only
    Else searches through values only
    Returns True if dict contains the search term, else returns False
    """
    # Checks if search term is a list/tuple or a single value
    if isinstance(searchTerm, (list, tuple)):
        searchUpper = searchTerm[0] if searchTerm[0] > searchTerm[1] else searchTerm[1]
        searchLower = searchTerm[0] if searchTerm[0] < searchTerm[1] else searchTerm[1]
    else:
        searchUpper = searchLower = searchTerm
    # Iterates through all key:value pairs
    for k, v in dict.items():
        if searchByKey and searchLower <= k <= searchUpper:
            return True
        elif not searchByKey and searchLower <= v <= searchUpper:
            return True
    return False

def searchByFood(food, alist=db.readFile()):
    """
    Searches through a list of canteens, and filters out the canteens which do not contain the food
    Accepts a food name, and an optional argument list of canteens
    Returns the filtered list of canteens
    """
    # Iterates through the list to filter out the items based on food
    temp = []
    for canteen in alist:
        if searchDict(canteen['food'], food):
            temp.append(canteen)
    return temp

def searchByPrice(price=[], alist=db.readFile()):
    """
    Searches through a list of canteens, and filters out the canteens which do not contain foodwithin the price range
    Accepts a price range, and an option argument list of canteens
    Returns the filtered list of canteens
    """
    # Iterates through the list to filter out the items based on price
    temp = []
    # Range is set to all real numbers if price is not assigned a value
    if len(price) < 2:
        if not len(price):
            price.append(float("inf"))
        price.append(float("-inf"))
    for canteen in alist:
        if searchDict(canteen['food'], list(map(float, price)), searchByKey=False):
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
