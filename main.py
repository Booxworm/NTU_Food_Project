import gui
import algo

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
        userInput = input("Give a valid input ({}): ".format('/'.join(range(1,len(options)+2))))
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
    choice = getInput(actionMsg, actionList)

    # Finds the canteen based on criteria
    if choice == '1':
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
    elif choice == '2':
        getInput(updateMsg, updateList)

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

if __name__ == '__main__':
    main()
