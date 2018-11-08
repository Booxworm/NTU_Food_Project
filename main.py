import gui
import algo2 as algo
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
    Accepts an optional argument list of canteens
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
    canteens = db.readFile()
    # Get choice
    action = getInput(actionMsg, actionList)

    # Finds the canteen based on criteria
    if action == '1':
        search = 0

        # While user is not done, continue asking for filters
        while not search == '3':
            search = getInput(searchMsg, searchList)

            # Exits program
            if search == str(len(searchList)+1):
                break

            # Find canteen based on criteria
            else:
                # Search by food
                if search == '1':
                    food = getInput("What food would you like to eat today?")
                    temp = algo.searchByFood('_'.join(food.lower().split()), canteens)
                    if not len(temp):
                        print("Are you sure you want {}? We could not find it in any of the canteens\n".format(food))
                    else:
                        canteens = temp

                # Search by price
                elif search == '2':
                    priceRange = getInput("Please enter a price range, separated by a space (2.50 5.00)\nIf left blank, will return all canteens sorted by price")
                    prices = priceRange.split(' ') if priceRange else []
                    canteens = algo.searchByPrice(prices, alist=canteens)

        # Done
        else:
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

        # Lists all canteens
        if update == '1':
            printCanteens()

        # Updates a canteen
        elif update == '2':
            pass

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

if __name__ == '__main__':
    main()
