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


def main():
    """
    Main function, handles user choice
    - Find a canteen based on:
        - Distance
        - Price
        - Rank
    - Update info of a canteen
    """
    print()
    # Get choice
    action = getInput(actionMsg, actionList)

    # Finds the canteen based on criteria
    if action == '1':
        criteria = getInput(criteriaMsg, criteriaList)

        # Exits program
        if criteria == str(len(criteriaList)+1):
            pass

        # Find canteen based on criteria
        else:
            # Distance
            if criteria == '1':
                print("Please click your current location")
                coords = gui.getCoordsClick(mapPath, scaledSize)
                sortedByDist = algo.sortedDistance(coords)
                for (dist, canteen) in sortedByDist:
                    print("{}: {}".format(canteen, dist))
            # Food
            elif criteria == '2':
                food = getInput("What food would you like to eat today?")
                sortedByFood = algo.searchFood(food.lower())
                if sortedByFood:
                    for (food, canteen) in sortedByFood:
                        print("{} has {}".format(canteen, food))
            # Price
            elif criteria == '3':
                priceRange = getInput("Please enter a price range, separated by a space (2.50 5.00)\nIf left blank, will return all canteens sorted by price")
                prices = priceRange.split(' ')

                # Empty input
                if not len(priceRange):
                    sortedByPrice = algo.searchPrice()
                # User entered only one number - upper limit
                elif len(prices) < 2:
                    sortedByPrice = algo.searchPrice(float(prices[0]))
                # User entered two numbers - lower limit
                else:
                    sortedByPrice = algo.searchPrice(float(prices[1]), float(prices[0]))
                if sortedByPrice:
                    for (price, food, canteen) in sortedByPrice:
                        print("{} has {} which costs {}".format(canteen, food, price))
            # Rank
            elif criteria == '4':
                rank = getInput("How many results do you want to get?")
                sortedByRank = algo.searchRank(int(rank))
                for (rank, canteen) in sortedByRank:
                    print("{}. {}".format(rank, canteen))


 # Updates canteen
    elif action == '2':
        update = getInput(updateMsg, updateList)
        canteens = db.readFile()
        newcanteens = canteens
        while update != '3':
            if update == '1':
            # Lists all canteens
                for c in newcanteens:
                    print("{}:".format(c['name']))
                    print("  Coordinates - {}".format(c['coords']))
                    print("  Rank - {}".format(c['rank']))
                    print("  Opening hours - {}".format(c['opening_hours']))
                    print("  Food:")
                    for food, price in c['food'].items():
                        print("    {0} - ${1:0.2f}".format(food, price))
                    print()
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
                
                update = input("If you want to finish editing, input 3: ")

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

criteriaMsg = "What is the criteria you want to use?"
criteriaList = ['Distance', 'Food', 'Price', 'Rank']

updateMsg = "What would you like to do?"
updateList = ["List out all information",
              "Select a canteen to update the information"]

editMsg = "which canteen?"
editList = [c['name'] for c in db.readFile()]

typeMsg = "Which type of info?"
typeList = ['coords','rank','opening_hours','food']

if __name__ == '__main__':
    main()
