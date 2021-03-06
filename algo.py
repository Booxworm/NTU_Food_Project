from math import sin, cos, sqrt, atan2, radians
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

def getDistLatLong(a,b):
    """
    Gets distance between two elements
    Accepts two tuples a and b, in the form (lat,long)
    Returns the distance between the two, rounded to 2 dp
    """
    # Approximate radius of earth in km
    R = 6373.0

    lat1 = radians(a[0])
    lon1 = radians(a[1])
    lat2 = radians(b[0])
    lon2 = radians(b[1])

    # Dist between the two points
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Returns distance in meters
    return round(R*c * 1000, 2)

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
        # Searches for a string
        for k,v in canteen['food'].items():
            formatedKey = ''.join(k.split('_'))
            for f in food:
                if formatedKey.find(f) >= 0:

                    temp2[k] = v
        if len(temp2):
            canteen['food'] = temp2
            temp.append(canteen)
    return temp

def searchByPrice(upper, alist=db.readFile()):
    """
    Searches through a list of canteens, and filters out the canteens which do not contain food within the price range
    Accepts an upper limit, and an option argument list of canteens
    Returns the filtered list of canteens
    """
    # Iterates through the list to filter out the items based on food
    upper = upper if upper else float('inf')
    temp = []
    for canteen in alist:
        temp2 = {}
        for k,v in canteen['food'].items():
            if v <= upper:
                temp2[k] = v
        if len(temp2):
            canteen['food'] = temp2
            temp.append(canteen)
    return temp

def sortByDist(userLocation, canteens=db.readFile(), latlong=True):
    """
    Gets the distance between the user's location and each of the canteens
    Accepts userLocation as tuple (x,y), and optional argument list of canteens
    If flag latlong is set, gets distance based on latitude and longtitude
    Returns a sorted list of canteens sorted by distances, in ascending order
    """
    dist = []
    for canteen in canteens:
        # Uses either latitude-longtitude or coordinates
        dist = getDistLatLong(userLocation, canteen['loc']) if latlong else getDistance(userLocation, canteen['coords'])
        canteen['dist'] = dist

    return mergesort(canteens, 'dist')

def sortByRank(canteens=db.readFile()):
    """
    Sorts the list of canteens by rank
    Accepts optional argument list of canteens
    Returns a sorted list of canteens
    """
    return mergesort(canteens, 'rank')

def formatCanteens(canteens=db.readFile()):
    """
    Formats a list of canteens for printing
    Accepts an optional argument list of canteens to print out
    Returns a formated list of canteens
    """
    msg = ""
    for c in canteens:
        msg += "{}\n".format(c['name'])
        if 'dist' in c:
            msg += "  Distance - {} m\n".format(c['dist'])
        msg += "  Rank - {}\n".format(c['rank'])
        msg += "  Food:\n"
        for food, price in c['food'].items():
            msg += "    {0} - ${1:0.2f}\n".format(food, price)
        msg += "\n"
    return msg
