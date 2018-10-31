def writeFile(canData):
    """
    Writes data of canteens to file
    Overwrites exitsting data
    Data space-separated, with food and price pairs comma-separated
    File is written in this format:
        name1 coords1 rank1 opening_hours1 food1a:price1a,food1b,price1b
        name2 coords2 rank2 opening_hours2 food2a:price2a,food2b,price2b
    """
    # Opens the file to write to
    with open(pathToFile, 'w') as f:
        # Iterates through each canteen
        for c in canData:
            foodList = []
            for food, price in c['food'].items():
                foodList.append("{}:{}".format(food,price))
            f.write("{} {} {} {} {}\n".format(c['name'],c['coords'],int(c['rank']),c['opening_hours'],','.join(foodList)))

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
    with open(pathToFile, 'r') as f:
        for line in f:
            c = {}
            data = line.rstrip('\n').split(' ')
            c['name'],c['coords'],c['rank'],c['opening_hours'] = data[:4]
            c['food'] = {}
            foodList = data[4].split(',')
            newList = []
            for foodPair in foodList:
                newList.append(foodPair.split(':'))
            c['food'].update(newList)
            canteens.append(c)
    return canteens

pathToFile = "./resources/db.txt"
