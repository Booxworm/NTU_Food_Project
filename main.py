import gui
import algo
import db

def getInput(msg, options=False, exit=True):
    """
    Prints out the input message, and lists out all the options provided
    Accepts the input message, and a list of options [optional] as parameters
    Adds an 'Exit' option as the last option if exit flag is set
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
    numberOfChoices = len(options)
    for i in range(numberOfChoices):
        print("{}. {}".format(i+1, options[i]))
    if exit:
        numberOfChoices += 1
        print("{}. Exit".format(numberOfChoices))

    # Gets user input
    userInput = input("Option: ")
    print()
    while not userInput.isdigit() or int(userInput) not in range(1,numberOfChoices+1):
        userInput = input("Give a valid input ({}): ".format('/'.join(map(str,range(1,numberOfChoices+1)))))
    return userInput

def getFood(canteens):
    """
    Asks user for food that user wants to eat, and filters out the canteens
    Accepts a list of canteens
    Returns a list of canteens
    """
    foodList = []

    # Gets list of food from user
    food = input("What food would you like to eat today?\nEnter all the food you want to eat, and enter #### when done\nIf empty, will take all foods\n")
    while food != '####':
        foodList.append(food)
        food = input()
    print()

    # Empty list, no filter on food
    if not len(foodList):
        return db.readFile()
    # Filters out canteens based on the food list given
    else:
        for i in range(len(foodList)):
            # Reformat the searches
            foodList[i] = ''.join(foodList[i].lower().split())

        # Searches for the food
        temp = algo.searchByFood(foodList, canteens)

    # Choice not found
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

    # Checks if price is valid for foods chosen
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

        # Exits
        if int(sort) == len(sortList) + 1:
            pass

        else:
            # Sort by distance
            if sort == '1':
                print("Please click your current location")
                coords = gui.getCoordsClick(mapPath, scaledSize)
                canteens = algo.sortByDist(coords, canteens, False)

            # Sort by rank
            elif sort == '2':
                canteens = algo.sortByRank(canteens)

            print(algo.formatCanteens(canteens))

    # Updates canteen
    elif action == '2':
        finish = False
        while not finish:
            # Asks user what he wants to do
            update = getInput(updateMsg, updateList)
            canteens = db.readFile()
            newCanteens = canteens

            # Exit
            if int(update) == len(updateList) + 1:
                finish = True

            # Lists all canteens
            elif update == '1':
                print(algo.formatCanteens(newCanteens))
                continue

            # Fetch a canteen and edit information
            elif update == '2':
                # Asks user which canteen to update, or exits
                editCan = getInput(editMsg, editList)
                if int(editCan) == len(editList) + 1:
                    break
                canIndex = int(editCan) - 1

                # Asks user which property to update, or exits
                editType = getInput(typeMsg,typeList)
                if int(editType) == len(typeList) + 1:
                    break
                type = typeList[int(editType) - 1]

                validInput = False
                while not validInput:
                    # Prints out specific guidelines for the property that the user is trying to update
                    print(guideline[type])
                    newStuff = input("New {} for {}:".format(type, editList[canIndex]))
                    print()

                    # Edit rank
                    if type == 'Edit rank':
                        if newStuff.isdigit() and 1 <= int(newStuff) <= 10:
                            newCanteens[canIndex]['rank'] = int(newStuff)
                            validInput = True
                        else:
                            print("Invalid input, try again with a number 1-10.\n")

                    # Add food
                    elif type == 'Add food':
                        food, price = newStuff.split(':')
                        try:
                            # Format food
                            food = '_'.join(food.lower().split())

                            # Check if price is a positive float
                            if float(price) < 0:
                                raise ValueError

                            # Assigns new price
                            newCanteens[canIndex]['food'][food] = float(price)
                            validInput = True
                        except ValueError:
                            print("Invalid input, try again with this format: <food>:<price>")

                    # Remove food
                    elif type == 'Remove food':
                        pass

                    # Edit food/price
                    elif type == 'Edit food/price':
                        foodList = list(newCanteens[canIndex]['food'].keys())
                        getInput("", foodList, exit=False)

                    else:
                        print("Currently unavailable.")
                        break
                db.writeFile(newCanteens)

    # End program
    print("Thanks for using our app")

# Image of map of NTU
mapPath = "./resources/ntuMap.jpeg"
mapSize = (1310,1600)
scaledSize = (int(mapSize[0]/3), int(mapSize[1]/3))

# List of messages / options
actionMsg = "Welcome to NTU F&B Recommendations!\nWhat would you like to do?"
actionList = ["Find a canteen",
              "Update information"]

sortMsg = "How would you like to sort your choices?"
sortList = ['Distance', 'Rank']

updateMsg = "What would you like to do?"
updateList = ["List out all information",
              "Select a canteen to update the information"]

editMsg = "which canteen?"
editList = [c['name'] for c in db.readFile()]

typeMsg = "Which type of info?"
typeList = ['Edit rank', 'Add food', 'Remove food', 'Edit food/price']

guideline = {
    'rank'          : "For ranking, please input an integer between 1 and 10 :)",
    'food'          : "You can only add food-price pairs.",
    'price'         : "Which of these foods do you want to edit?\nUse the format <food>:<price>\nEg: chicken rice:4"
}

if __name__ == '__main__':
    main()
