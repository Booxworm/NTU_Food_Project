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


def mergesort(alist):
    """
    Mergesort recursively divides up the list into two, and merges the two serparate lists together
    Returns a sorted list
    """
    listLen = len(alist)
    # Base case
    if listLen < 2:
        return alist

    leftList = alist[:listLen // 2]
    rightList = alist[listLen // 2:]  # "//" to force division

    # Mergesort left and right list recursively
    leftList = mergesort(leftList)
    rightList = mergesort(rightList)
    return merge(leftList, rightList)

def binarySearchList(itemList, item, findAll=True, ind=0):
    """
    Searches through a sorted list containing lists, and finds item within inner list
    By default, will check index 0 of each inner list

                 |                   |
                 V                   V
            [['item1', 'item2'], ['item3', 'item4'], ...]

    Accepts a sorted list itemList, and item
        - Accepts a range of items, use tuples or lists with max and min
        - ('2.00', '5.00')  or  ['cat', 'dogs']
    If 'all' flag is set, finds all lists containing that item
    Return inner list(s) if found, empty list if not
    """
    # If item is a tuple or a list, search within the range
    if isinstance(item, (list, tuple)):
        item_upper = item[0] if item[0] > item[1] else item[1]
        item_lower = item[0] if item[0] < item[1] else item[1]
    # Else search for the item
    else:
        item_lower = item_upper = item

    lower = 0
    upper = len(itemList) - 1
    mid = (lower + upper) // 2
    searchResult = []
    found = False

    # Iteratively searches through the list for item
    while lower <= upper and not found:
        # Found the first item
        mid = (lower + upper)//2
        if item_lower <= itemList[mid][ind] <= item_upper:
            found = True
            searchResult.append(itemList[mid])

            # Finds the other elements in the list
            if findAll:
                originalMid = mid
                # Checks previous elements for same item
                while mid > 0 and item_lower <= itemList[mid-1][ind] <= item_upper:
                    searchResult.append(itemList[mid-1])
                    mid -= 1
                # Reset mid to original mid
                mid = originalMid
                while  mid+1 < len(itemList) and item_lower <= itemList[mid+1][ind] <= item_upper:
                    searchResult.append(itemList[mid+1])
                    mid += 1

        else:
            # Item smaller than current search
            if item_upper < itemList[mid][ind]:
                upper = mid - 1
            # Item larger than current search
            else:
                lower = mid + 1
    return searchResult

def sortedDistance(userLocation):
    """
    Gets the distance between the user's location and each of the canteens
    Accepts userLocation as tuple (x,y)
    Returns a sorted array of distances from the canteens, in ascending order
        [['65', 'can1'], ['71', 'can9'], ['104', 'NS']]
    """
    dist = []
    canteens = db.readFile()
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
    canteens = db.readFile()
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
    canteens = db.readFile()
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
    canteens = db.readFile()
    for canteen in canteens:
        rank.append([canteen['rank'], canteen['name']])
    return mergesort(rank)

def searchDistance(userLocation, limit=False):
    """
    Searches database for the canteens, based on distance
    Accepts userLocation and integer limit, which limits the canteens to the closest few
    Returns a list of canteens sorted by distance
    """
    distList = sortedDistance(userLocation)
    # No limit specified, returns all canteens
    if not limit:
        return distList
    # Finds closest few canteens
    else:
        return distList[:limit]

def searchFood(food=False):
    """
    Searches database for the food name
    Accepts string food
    Returns a list of canteens that the food can be found in, or empty list if not found
    """
    foodList = sortedFood()
    # No food specified, returns all food
    if not food:
        return foodList
    # Finds all canteens that have that food
    searchedFoodList = binarySearchList(foodList, food)
    # If search returns empty list
    if not len(searchedFoodList):
        print("{} isn't available in any of the canteens".format(food))
    return searchedFoodList

def searchPrice(upper=False, lower=False):
    """
    Searches database for all food within the price range
    Accepts string upper and lower limits of price
        - If no input provided, returns food sorted by price (i.e. ['2.00', 'chicken rice', 'can2'])
        - If upper/lower limit provided, returns food below/above that limit respectively
        - If no food is found to be within the price range, an empty list is returned
    """
    priceList = sortedPrice()
    # No limit specified, returns all food
    if not lower and not upper:
        return priceList
    # Finds all canteens that have food within that price
    searchedPriceList = binarySearchList(priceList, (lower, upper))
    # If search returns empty list
    if not len(searchedPriceList):
        print("{} isn't available in any of the canteens")
    return searchedPriceList

def searchRank(limit=False):
    """
    Searches database for the canteens, based on rank
    Accepts integer limit, which limits the canteens to the top few
    Returns a list of canteens sorted by rank
    """
    rankList = sortedRank()
    # No limit specified, returns all canteens
    if not limit:
        return rankList
    # Finds top few canteens
    else:
        return rankList[:limit]

def filter(criteria, alist):
    pass
