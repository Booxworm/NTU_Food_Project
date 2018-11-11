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
            f.write("{} {},{} {} {},{} {} {},{}\n".format(c['name'],
                                                 c['coords'][0],c['coords'][1],
                                                 c['rank'],
                                                 
                                                 c['opening_hours'][0],c['opening_hours'][1],
                                                 ','.join(foodList),
                                                 c['loc'][0],c['loc'][1]  ))

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
            c['loc'] = tuple(map(float,data[5].split(',')))
            
            newList = []
            for foodPair in foodList:
                foodPair = foodPair.split(':')
                foodPair[1] = float(foodPair[1])
                newList.append(foodPair)
            c['food'].update(newList)
            canteens.append(c)
    return canteens

pathToFile = "./resources/db.txt"
