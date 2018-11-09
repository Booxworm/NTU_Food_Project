import main
def writeFile(canData):
    """
    Writes data of canteens to file
    Overwrites exitsting data
    Data space-separated, with coords, opening hours, and food:price pairs comma-separated
    File is written in this format:
        name1 x_coord1,y_coord1 rank1 opening_hours1,closing_hours1 food1a:price1a,food1b,price1b
        name2 x_coords2,y_coord2 rank2 opening_hours2,closing_hours1 food2a:price2a,food2b,price2b
    """
    # Opens the file to write to
    with open(pathToFile, 'w') as f:
        # Iterates through each canteen
        for c in canData:
            foodList = []
            for food, price in c['food'].items():
                foodList.append("{}:{}".format(food,price))
            f.write("{} {},{} {} {},{} {}\n".format(c['name'],
                                                 c['coords'][0],c['coords'][1],
                                                 c['rank'],
                                                 c['opening_hours'][0],c['opening_hours'][1],
                                                 ','.join(foodList)))

def readFile():
    """
    Reads data of file and returns it as a list of canteens
    Each canteen has the following structure:
    {
        'name' : 'can1',
        'coords' : (291,311),
        'rank' : 1,
        'opening_hours' : ('0700','2100'),
        'food' : {
            'apple' : 2.00,
            'banana' : 4.00,
        }
    }
    """
    canteens = []
    # Opens file
    with open(pathToFile, 'r') as f:
        # Reads file line by line
        for line in f:
            c = {}
            data = line.rstrip('\n').split(' ')
            c['name'] = data[0]
            c['coords'] = tuple(map(int,data[1].split(',')))
            c['rank'] = int(data[2])
            c['opening_hours'] = tuple(data[3].split(','))
            c['food'] = {}
            foodList = data[4].split(',')
            newList = []
            for foodPair in foodList:
                foodPair = foodPair.split(':')
                foodPair[1] = float(foodPair[1])
                newList.append(foodPair)
            c['food'].update(newList)
            canteens.append(c)
    return canteens

def updateInfo()    # Updates canteen
    finish = False
    while !finish:
        
        update = main.getInput(updateMsg, updateList)
        canteens = readFile()
        newcanteens = canteens
    #    while update != '3':
            if update == '1':
                # Lists all canteens
                main.printCanteens()
                break
            if update == '2':
            # Fetch a canteen and edit information
                editCan = getInput(editMsg, editList)
                #canteens[editCan-1]
                editType = getInput(typeMsg,typeList)
                invalidInput = True
                while invalidInput:
                    newstuff = input("New "+typeList[int(editType)-1]]+" for "+editList[int(editCan)-1]+":")
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
                    
                
updateMsg = "What would you like to do?"
updateList = ["List out all information",
              "Select a canteen to update the information"]

editMsg = "which canteen?"
editList = [c['name'] for c in db.readFile()]

typeMsg = "Which type of info?"
typeList = ['coords','rank','opening_hours','food']


pathToFile = "./resources/db.txt"
