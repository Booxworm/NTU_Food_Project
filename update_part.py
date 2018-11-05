    # Stuff to be solved: 1. writeFile might have some errors evrey time rewrite sth others disappear
    
    # Updates canteen
    elif action == '2':
        update = getInput(updateMsg, updateList)
        canteens = db.readFile()
        while not update == '3':
            if update == '1':
            # Lists all canteens
                for c in canteens:
                    print("{}:".format(c['name']))
                    print("  Coordinates - {}".format(c['coords']))
                    print("  Rank - {}".format(c['rank']))
                    print("  Opening hours - {}".format(c['opening_hours']))
                    print("  Food:")
                    for food, price in c['food'].items():
                        print("    {0} - ${1:0.2f}".format(food, price))
                    print()
            if update == '2':
            # Fetch a canteen and edit information
                editCan = getInput(editMsg, editList)
                #canteens[editCan-1]
                editType = getInput(typeMsg,typeList)
                invalidInput = True
                while invalidInput:
                    newstuff = input()
                    if editType == '3': #rank
                        if newstuff.isdigit():
                            canteens[int(editCan)-1][typeList[int(editType)-1]] = int(newstuff)
                            invalidInput = False
                    else:
                        canteens[int(editCan)-1][typeList[int(editType)-1]] = newstuff
                        invalidInput = False
                      #  print("invalid input, try agian.")
                db.writeFile(canteens[int(editCan)-1])
                
                update = input("If you want to finish editing, input 0")
