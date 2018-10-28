import gui

# Gets user input, returns a number based on the option selected
def getInput(msg, options=False):
    # Displays input message
    print(msg)

    # No options
    if not options:
        return input()

    # Prints out all options
    for i in range(len(options)):
        print("{}. {}".format(i+1, options[i]))
    print("{}. Exit".format(len(options)+1))

    # Gets and checks user input
    userInput = input("Option: ")
    print()
    while not userInput.isdigit() or int(userInput) not in range(1,len(options)+2):
        userInput = input("Give a valid input ({}): ".format('/'.join(range(1,len(options)+2))))
    return userInput

# Finds a canteen based on criteria
def findCanteen(criteria, params=False):
    if criteria == 'Distance':
        pass
    elif criteria == 'Price':
        pass
    elif criteria == 'Rank':
        pass
    return True

# Updates information about a canteen
def updateCanteen(canteen, params):
    pass

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


def main():
    # Get choice
    choice = getInput(actionMsg, actionList)

    # Finds the canteen based on criteria
    if choice == '1':
        criteria = getInput(criteriaMsg, criteriaList)

        # Exits program
        if criteria == str(len(criteriaList)+1):
            pass

        # Find canteen based on criteria
        else:
            params = False
            # Distance
            if criteria == '1':
                params = gui.getCoordsClick()
            # Price
            elif criteria == '2':
                params = getInput("Please choose a price")

            canteen = findCanteen(criteriaList[int(criteria)-1], params)
            print(canteen)

    # Updates canteen
    elif choice == '2':
        getInput(updateMsg, updateList)

    # End program
    print("Thanks")

# List of messages / options
actionMsg = "Welcome to NTU F&B Recommendations!\nWhat would you like to do?"
actionList = ["Find a canteen (based on distance, price, rank)",
              "Update information about a canteen"]

criteriaMsg = "What is the criteria you want to use?"
criteriaList = ['Distance', 'Price', 'Rank']

updateMsg = "What would you like to do?"
updateList = ["List out all information",
              "Select a canteen to update the information"]

if __name__ == '__main__':
    main()
