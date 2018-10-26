def findCanteen(criteria):
    pass

def updateCanteen(canteen, params):
    pass

print("Welcome to NTU F&B Recommendations!\n\
       What would you like to do?\n\
       1. Find a canteen (based on distance, price, rank)\n\
       2. Update information about a canteen\n\
       3. Exit")

user_input = input()
while not user_input.isdigit() or int(user_input) not in range(1,4):
    user_input = input("Give a valid input (1/2/3)")

print("Thanks")
