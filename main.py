import gui
import algo
import db

def getInput(msg, options=False):
    """
    Prints out the input message, and lists out all the options provided
    Adds an 'Exit' option as the last option
    Accepts the input message, and a list of options [optional] as parameters
    Returns user input as a string, between '1' and the maximum number of options i.e. '5'
    """
    # Displays input message
    print(msg)

    # No options
    if not options:
        userInput = input()
        print()
        return userInput

    # Prints out all options
    for i in range(len(options)):
        print("{}. {}".format(i+1, options[i]))
    print("{}. Exit".format(len(options)+1))

    # Gets user input
    userInput = input("Option: ")
    print()
    while not userInput.isdigit() or int(userInput) not in range(1,len(options)+2):
        userInput = input("Give a valid input ({}): ".format('/'.join(map(str,range(1,len(options)+2)))))
    return userInput

def printCanteens(canteens=db.readFile()):
    """
    Prints out a list of canteens
    Accepts an optional argument list of canteens to print out
    """
    for c in canteens:
        print("{}:".format(c['name']))
        print("  Coordinates - {}".format(c['coords']))
        if 'dist' in c:
            print("  Distance - {}".format(c['dist']))
        print("  Rank - {}".format(c['rank']))
        print("  Opening hours - {}".format(c['opening_hours']))
        print("  Food:")
        for food, price in c['food'].items():
            print("    {0} - ${1:0.2f}".format(food, price))
        print()

def getFood(canteens):
    """
    Asks user for food that user wants to eat, and filters out the canteens
    Accepts a list of canteens
    Returns a list of canteens
    """
    foodList = []
    food = input("What food would you like to eat today?\nEnter all the food you want to eat, and enter #### when done\n")
    while food != '####':
        foodList.append(food)
        food = input()
    print()
    for i in range(len(foodList)):
        # Reformat the searches
        foodList[i] = '_'.join(foodList[i].lower().split())
    temp = algo.searchByFood(foodList, canteens)
    if not len(temp):
        print("Please choose some other food, we could not find your choices in any of the canteens\n")
        return getFood(canteens)
    else:
        canteens = temp
    return canteens

def getPrice(canteens):
    """
    Asks user for upper and lower limits of price, filters out canteens based on the price range
    Accepts a list of canteens
    Returns a list of canteens
    """
    # Asks for upper limit of price
    valid = False
    upper = input("Enter an upper limit, or leave blank for no upper limit\n")
    while not valid:
        try:
            if upper != '':
                upper = float(upper)
            valid = True
        except ValueError:
            upper = input("Invalid input, please enter a number\n")

    # Asks for lower limit of price
    valid = False
    lower = input("Enter a lower limit, or leave blank for no lower limit\n")
    while not valid:
        try:
            if lower != '':
                lower = float(lower)
            valid = True
        except ValueError:
            lower = input("Invalid input, please enter a number\n")
    temp = algo.searchByPrice(lower, upper, alist=canteens)
    if not len(temp):
        print("Sorry, we could not find any canteens within the specified price range\n")
    else:
        print()
        canteens = temp
    return canteens

def main():
    """
    Main function, handles user choice
    - Find a canteen based on:
        - Food
        - Price
    - Sorts the canteens based on:
        - Distance
        - Rank
    - Updates info of a canteen
    """
    print()
    canteens = db.readFile()
    # Get choice
    action = getInput(actionMsg, actionList)

    # Finds the canteen based on criteria
    if action == '1':
        # Search by food
        canteens = getFood(canteens)

        # Search by price
        canteens = getPrice(canteens)

        # Sort
        sort = getInput(sortMsg, sortList)

        # Sort by distance
        if sort == '1':
            print("Please click your current location")
            coords = gui.getCoordsClick(mapPath, scaledSize)
            canteens = algo.sortByDist(coords, canteens)

        # Sort by rank
        elif sort == '2':
            canteens = algo.sortByRank(canteens)

        printCanteens(canteens)




 # Updates canteen
    elif action == '2':
        update = getInput(updateMsg, updateList)
        canteens = db.readFile()
        newcanteens = canteens
        while update != '3':
            if update == '1':
                # Lists all canteens
                printCanteens()
                break
            if update == '2':
            # Fetch a canteen and edit information
                editCan = getInput(editMsg, editList)
                #canteens[editCan-1]
                editType = getInput(typeMsg,typeList)
                invalidInput = True
                while invalidInput:
                    #newstuff = input("New ",typeList[int(editType)-1]]," for ",editList[int(editCan)-1],":")
                    newstuff = input("New stuff:")
                    if editType == '2': #rank
                        if newstuff.isdigit():
                            if 1<=int(newstuff)<=10:
                                newcanteens[int(editCan)-1][typeList[int(editType)-1]] = int(newstuff)
                                invalidInput = False
                        if invalidInput == True:
                            print("Invalid input, try again with a number 1-10.")
                    else:
                        newcanteens[int(editCan)-1][typeList[int(editType)-1]] = newstuff
                        invalidInput = False
                      #  print("invalid input, try agian.")
                canteens = newcanteens
                db.writeFile(canteens)

                exit = input("If you want to finish editing, input 0: ")
                if exit == '0':
                    break

    # End program
    print("Thanks")

# Image of map of NTU
mapPath = "./resources/ntuMap.jpeg"
mapSize = (1310,1600)
scaledSize = (int(mapSize[0]/3), int(mapSize[1]/3))

# List of messages / options
actionMsg = "Welcome to NTU F&B Recommendations!\nWhat would you like to do?"
actionList = ["Find a canteen (based on certain criteria)",
              "Update information about a canteen"]

searchMsg = "How would you like to filter your choices?\nChoose 'Done' when you are done."
searchList = ['Food', 'Price', 'Done']

sortMsg = "How would you like to sort your choices?"
sortList = ['Distance', 'Rank']

updateMsg = "What would you like to do?"
updateList = ["List out all information",
              "Select a canteen to update the information"]

editMsg = "which canteen?"
editList = [c['name'] for c in db.readFile()]

typeMsg = "Which type of info?"
typeList = ['coords','rank','opening_hours','food']

if __name__ == '__main__':
    main()
