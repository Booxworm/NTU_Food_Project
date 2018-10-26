import gui

# Gets user input, returns a number based on the option selected
def getInput(msg, options):
    # Displays input message and options
    print(msg)
    for i in range(len(options)):
        print("{}. {}".format(i+1, options[i]))
    print("{}. Exit".format(len(options)+1))

    # Gets and checks user input
    userInput = input()
    print()
    while not userInput.isdigit() or int(userInput) not in range(1,len(options)+2):
        userInput = input("Give a valid input ({}): ".format('/'.join(range(1,len(options)+2))))
    return userInput

# Finds a canteen based on criteria
def findCanteen(criteria):
    if criteria == 'Distance':
        print(gui.getCoordsClick())
    return True

# Updates information about a canteen
def updateCanteen(canteen, params):
    pass

# Variable declarations
choiceList = ["Find a canteen (based on distance, price, rank)",\
              "Update information about a canteen"]
criteriaList = ['Distance', 'Price', 'Rank']

# Get choice
choice = getInput("Welcome to NTU F&B Recommendations!\nWhat would you like to do?", choiceList)

# Finds the canteen based on criteria
if choice == '1':
    criteria = getInput("What is the criteria you want to use?", criteriaList)

    # Exits program
    if criteria == str(len(criteriaList)+1):
        pass

    # Find canteen based on criteria
    else:
        canteen = findCanteen(criteriaList[int(criteria)-1])
        print(canteen)

# Updates canteen
elif choice == '2':
    pass

# End program
print("Thanks")
