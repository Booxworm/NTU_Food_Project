"""
Things to work on:
1. As much as possible, keep functions abstracted
2. Why use so many times of "for __ in range(9)"? Can be consolidated into a single block
3. Calling distance_a_b function, without defining it
4. Wrong indentation of for loop, passnum not defined
5. Bubble sort may be simple to implement, but takes exponentially longer with larger terms. Use mergesort
    - If interested can search "bubble sort complexity"
6. No return statement
7. Overall try comment your code for readability
"""
import math
from resources.db import canteens

def merge(left_list, right_list):

    result_list = []

    # while left and right list has elements
    while left_list and right_list:
        if left_list[0] < right_list[0]:
            result_list.append(left_list[0])
            left_list.pop(0)
        else:
            result_list.append(right_list[0])
            right_list.pop(0)

    #left list still contain elements. Append its contents to end of the result list
    if left_list:
        result_list.extend(left_list)
    else:
    #right list still contain elements. Append its contents to end of the result list
        result_list.extend(right_list)

    return result_list


def mergesort(dist):
    list_len = len(dist)
    # base case
    if list_len < 2:
        return dist
    left_list = dist[:list_len // 2]   # //
    right_list = dist[list_len // 2:]  # "//" to force division

    # merge sort left and right list recursively
    left_list = mergesort(left_list)
    right_list = mergesort(right_list)
    return merge(left_list, right_list)

#sorts dist between user and cateen
def sorted_distance(user_location):

    dist=[]
    for canteen in canteens:
        temp = [canteen['name']]
        temp.append(distance_a_b(user_location,canteen['coords']))
        dist.append(temp)

    asc_dist=mergesort(dist)
    return asc_dist


def search_by_food(foodname,foodlist_canteens):

    found=False
    for canteen in foodlist_canteens.values():
        if(canteen.find(foodname)==True):
            print("food found in", foodlist_canteens.keys())
            found=True

    if not found:
        print("The food isn't available in any of the canteens")
        return 0
    return(list)

def search_by_price(lower=False, upper=False):
    for canteen in canteens:
        for food, price in canteen['food'].items():
            print("{} costs {}".format(food, price))

def distance_a_b(a, b):
    # a and b are tuples with 2 elements
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dist = math.sqrt (dx * dx + dy * dy)
    output = round (dist, 2)
    return dist
