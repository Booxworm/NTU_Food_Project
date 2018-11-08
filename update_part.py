     # Updates canteen
        elif action == '2':
            update = getInput(updateMsg, updateList)
            canteens = db.readFile()
            newcanteens = canteens
            while not update == '3':
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
                if update == '2':
                # Fetch a canteen and edit information
                    editCan = getInput(editMsg, editList)
                    #canteens[editCan-1]
                    editType = getInput(typeMsg,typeList)
                    invalidInput = True
                    while invalidInput:
                        newstuff = input()
                        if editType == '2': #rank
                            if newstuff.isdigit():
                                newcanteens[int(editCan)-1][typeList[int(editType)-1]] = int(newstuff)
                                invalidInput = False
                            else:
                                print("Invalid input, try again with a number 1-10")
                        else:
                            newcanteens[int(editCan)-1][typeList[int(editType)-1]] = newstuff
                            invalidInput = False
                          #  print("invalid input, try agian.")
                    canteens = newcanteens
                    db.writeFile(canteens)
                    
                    update = input("If you want to finish editing, input 3")


updateMsg = "What would you like to do?"
updateList = ["List out all information",
              "Select a canteen to update the information"]

editMsg = "which canteen?"
editList = [c['name'] for c in db.readFile()]

typeMsg = "Which type of info?"
typeList = ['coords','rank','opening_hours','food']