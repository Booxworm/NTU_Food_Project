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

def searchDict(dict, searchTerm, searchByKey=True):
    for k, v in dict.items():
        if searchByKey and k == searchTerm:
            return True
        elif not searchByKey and v == searchTerm:
            return True
    return False

def addFilter(filter, searchTerm, alist=db.readFile()):
    # If filter by food, checks the keys
    if filter.lower() == 'food':
        searchByKey=True
    # If filter by price, checks the values
    elif filter.lower() == 'price':
        searchByKey=False
    else:
        return False

    # Iterates through the list to filter out the items
    temp = []
    for canteen in alist:
        if searchDict(canteen['food'], searchTerm, searchByKey):
            temp.append(canteen)

    return temp

c = addFilter('pRice', 2)
print(c)


def sortedDistance(userLocation, canteens=db.readFile()):
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

# def sortedFood(canteens=db.readFile()):
#     """
#     Accepts an optional list of canteens
#     Returns a list of canteens, with food sorted in ascending order
#     """
#     return mergesort(canteens, 'food')
#
# def sortedPrice(canteens=db.readFile()):
#     """
#     Accepts an optional list of canteens
#     Returns a sorted array of prices and food from each canteen, in ascending order
#         [['3.00','duck rice','can9'], ['3.50','chicken rice','NS'], ['4.00','mala', 'can1']]
#     """
#     priceList = []
#     for canteen in canteens:
#         for food, price in canteen['food'].items():
#             priceList.append([price, food, canteen['name']])
#     return mergesort(priceList)
#
# def sortedRank(canteens=db.readFile()):
#     """
#     Accepts an optional list of canteens
#     Returns a sorted array ranking each cante en, in ascending order
#         [[1, 'can1'], [2, 'can2'], [3, 'can9']]
#     """
#     return mergesort(canteens, 'rank')
#
# def searchDistance(userLocation, limit=False):
#     """
#     Searches database for the canteens, based on distance
#     Accepts userLocation and integer limit, which limits the canteens to the closest few
#     Returns a list of canteens sorted by distance
#     """
#     distList = sortedDistance(userLocation)
#     # No limit specified, returns all canteens
#     if not limit:
#         return distList
#     # Finds closest few canteens
#     else:
#         return distList[:limit]
#
# def searchFood(food=False):
#     """
#     Searches database for the food name
#     Accepts string food
#     Returns a list of canteens that the food can be found in, or empty list if not found
#     """
#     foodList = sortedFood()
#     # No food specified, returns all food
#     if not food:
#         return foodList
#     # Finds all canteens that have that food
#     searchedFoodList = binarySearchList(foodList, food)
#     # If search returns empty list
#     if not len(searchedFoodList):
#         print("{} isn't available in any of the canteens".format(food))
#     return searchedFoodList
#
# def searchPrice(upper=False, lower=False):
#     """
#     Searches database for all food within the price range
#     Accepts string upper and lower limits of price
#         - If no input provided, returns food sorted by price (i.e. ['2.00', 'chicken rice', 'can2'])
#         - If upper/lower limit provided, returns food below/above that limit respectively
#         - If no food is found to be within the price range, an empty list is returned
#     """
#     priceList = sortedPrice()
#     # No limit specified, returns all food
#     if not lower and not upper:
#         return priceList
#     # Finds all canteens that have food within that price
#     searchedPriceList = binarySearchList(priceList, (lower, upper))
#     # If search returns empty list
#     if not len(searchedPriceList):
#         print("{} isn't available in any of the canteens")
#     return searchedPriceList
#
# def searchRank(limit=False):
#     """
#     Searches database for the canteens, based on rank
#     Accepts integer limit, which limits the canteens to the top few
#     Returns a list of canteens sorted by rank
#     """
#
#
#
#     rankList = sortedRank()
#     # No limit specified, returns all canteens
#     if not limit:
#         return rankList
#     # Finds top few canteens
#     else:
#         return rankList[:limit]
#
