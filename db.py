def writeFile(canData):
    """
    Writes data of canteens to file
    Overwrites exitsting data
    Data space-separated, with coords, latitude-longtitude, and food:price pairs comma-separated
    File is written in this format:
        name1 x_coord1,y_coord1 lat1,long1 rank1 food1a:price1a,food1b,price1b
        name2 x_coords2,y_coord2 lat2,long2 rank2 food2a:price2a,food2b,price2b
    """
    # Opens the file to write to
    with open(pathToFile, 'w') as f:
        # Iterates through each canteen
        for c in canData:
            foodList = []
            for food, price in c['food'].items():
                foodList.append("{}:{}".format(food,price))
            f.write("{} {},{} {},{} {} {}\n".format(c['name'],
                                                 c['coords'][0],c['coords'][1],
                                                 c['loc'][0],c['loc'][1],
                                                 c['rank'],
                                                 ','.join(foodList)))

def readFile():
    """
    Reads data of file and returns it as a list of canteens
    Each canteen has the following structure:
    {
        'name' : 'can1',
        'coords' : (291,311),
        'loc' : (20.1203140,-11.9241941),
        'rank' : 1,
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
            c['loc'] = tuple(map(float,data[2].split(',')))
            c['rank'] = int(data[3])
            c['food'] = {}

            # Formats food list
            if len(data) == 5 and len(data[4]):
                foodList = data[4].split(',')
                newList = []
                for foodPair in foodList:
                    foodPair = foodPair.split(':')
                    foodPair[1] = float(foodPair[1])
                    newList.append(foodPair)
                c['food'].update(newList)
            canteens.append(c)
    return canteens

pathToFile = "./resources/db.txt"
