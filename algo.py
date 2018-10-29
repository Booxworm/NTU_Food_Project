import math
from resources.db import canteens

def getDistance(a, b):
    """
    Gets distance between two elements
    Accepts two tuples a and b, in the form (x,y)
    Returns the distance between the two, rounded to 2 dp
    """
    # a and b are tuples with 2 elements
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dist = math.sqrt (dx * dx + dy * dy)
    return round(dist,2)

def merge(leftList, rightList):
    """
    Takes two lists, leftList and rightList, and merges them based on their value
    Returns a sorted list
    """
    merged = []

    # While left and right list has elements
    while leftList and rightList:
        if leftList[0] < rightList[0]:
            merged.append(leftList[0])
            leftList.pop(0)
        else:
            merged.append(rightList[0])
            rightList.pop(0)

    # Left list still contain elements. Append its contents to end of the result list
    if leftList:
        merged.extend(leftList)
    else:
    # Right list still contain elements. Append its contents to end of the result list
        merged.extend(rightList)

    return merged


def mergesort(dist):
    """
    Mergesort recursively divides up the list into two, and merges the two serparate lists together
    Returns a sorted list
    """
    listLen = len(dist)
    # Base case
    if listLen < 2:
        return dist

    leftList = dist[:listLen // 2]
    rightList = dist[listLen // 2:]  # "//" to force division

    # Mergesort left and right list recursively
    leftList = mergesort(leftList)
    rightList = mergesort(rightList)
    return merge(leftList, rightList)


def sortedDistance(userLocation):
    """
    Gets the distance between the user's location and each of the canteens
    Accepts userLocation as tuple (x,y)
    Returns a sorted array of distances from the canteens, in ascending order
        [['65', 'can1'], ['71', 'can9'], ['104', 'NS']]
    """
    dist = []
    for canteen in canteens:
        temp = [getDistance(userLocation,canteen['coords'])]
        temp.append(canteen['name'])
        dist.append(temp)
    return mergesort(dist)

def sortedFood():
    """
    Returns a sorted array of food and the canteen it is from, in ascending order
        [['chicken rice', 'NS'], ['duck rice', 'can9'], ['mala', 'can1']]
    """
    foodList = []
    for canteen in canteens:
        for food in canteen['food'].keys():
            foodList.append([food, canteen['name']])
    return mergesort(foodList)

def sortedPrice():
    """
    Returns a sorted array of prices and food from each canteen, in ascending order
        [['3.00','duck rice','can9'], ['3.50','chicken rice','NS'], ['4.00','mala', 'can1']]
    """
    priceList = []
    for canteen in canteens:
        for food, price in canteen['food'].items():
            priceList.append([price, food, canteen['name']])
    return mergesort(priceList)

def sortedRank():
    """
    Returns a sorted array ranking each canteen, in ascending order
        [[1, 'can1'], [2, 'can2'], [3, 'can9']]
    """
    rank = []
    for canteen in canteens:
        rank.append([canteen['rank'], canteen['name']])
    return mergesort(rank)


def binarySearch(itemList, item):
    """
    Searches through a sorted list
    Accepts a sorted list itemList, and item
    Return True if found, False if not
    """
    lower = 0
    upper = len(itemList) - 1
    found = False
    while lower < upper and not found:
        mid = (lower + upper)//2
        if itemList[mid] == item:
            found = True
        else:
            if item < itemList[mid]:
                upper = mid - 1
            else:
                lower = mid + 1
    return found




def searchFood(food):
    """
    Searches database for the food name
    Accepts string food
    Returns an array of canteens that the food can be found in, or False if not found
    """
    foodList = sortedFood()
    binarySearch(foodList, food)
    if not found:
        print("The food isn't available in any of the canteens")
        return 0
    return(list)

def searchPrice(upper=False, lower=False):
    list=[]
    list2=[]
    for canteen in canteens:
        for food, price in canteen['food'].items():
            print("{} costs {}".format(food, price))
            list.append(canteen['food'].items())

    sort_list=mergesort(list)
    if(lower<=sort_list<=upper):
        list2.append(sort_list['food'])

    return list2
