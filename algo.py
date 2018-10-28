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
#sorts dist between user and cateen
def sorted_distance(user_location,canteen_location):
    candist=[]
    dist=[]
    for j in range(9):
        candist.append(cateens[can1][coords])
    for i in range(9):
        dist[i].append(distance_a_b(user_location,candist[i]))
    for passnum in range(9):
        swapped = False
    for i in range(9-passnum):
        if dist[i]>dist[i+1]:
            temp = dist[i]
            dist[i] = dist[i+1]
            dist[i+1] = temp
            swapped = True
    if not swapped:
        break;
  #dist[0] will be the distance between user and nearest canteen
  x=0
  for i in [1,2,9,11,13,14,16,"NS","Koufu","Quad Cafe"]:
    print(dist[x], "is the dist from canteen",i)
    x=x+1


def search_by_food(foodname,foodlist_canteens):
    list=[]
    found=False
    for i in [1,2,9,11,13,14,16,"NS","Koufu","Quad Cafe"]:
        if(canteens[food][0].find(foodname)==True):
            print("food found in", i)
            list.append(i)
            found=True
    if not found:
        print("The food isn't available in any of the canteens")
        return 0
    return(list)
