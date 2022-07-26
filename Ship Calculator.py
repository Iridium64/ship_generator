# Companion Ship Fitting Calculator to the Ship Generator V3
# Ver 0.0.1

import csv, os
from config.definintions import ROOT_DIR

#load from CSV. slightly modfied from the way that the generator handles it internally for readibility reasons
def load_from_csv():
    global hull_types 
    hull_types = []
    for i in os.listdir(os.path.join(ROOT_DIR, 'ships')):
        hull_types.append(i.split(".")[0])
    
    global ship_type_dict
    global ship_slots_dict

    ship_type_dict = {}
    ship_slots_dict = {}
    for x in range(len(hull_types)):
        ship_type_dict[hull_types[x]] = []
        file = list(csv.reader(open(os.path.join(ROOT_DIR, 'ships', hull_types[x] + ".csv"))))
        for i in range(len(file)):
            ship_type_dict[hull_types[x]].append(file[i][0])
        for row in file:   
            ship_slots_dict[row[0]] = [row[1]]
            for i in range(1, int(len(row)/2)):
                ship_slots_dict[row[0]].append((row[i*2], row[i*2+1]))

    global slot_types
    slot_types = []
    for i in os.listdir(os.path.join(ROOT_DIR, 'modules')):
        slot_types.append(i.split(".")[0])

    global ship_modules_dict
    global module_stats_dict
    ship_modules_dict = {}
    module_stats_dict = {}
    for x in range(len(slot_types)):
        ship_modules_dict[slot_types[x]] = []
        file = list(csv.reader(open(os.path.join(ROOT_DIR, 'modules', slot_types[x] + ".csv"))))
        for i in range(len(file)):
            ship_modules_dict[slot_types[x]].append(file[i][0])
        for row in file:
                module_stats_dict[row[0]] = row[1:]

load_from_csv()
while True:
    try:
        print("Possible categories are:")
        for i in range(1, len(hull_types)+1):
            print(str(i) + ": " +hull_types[i-1])
        choice = int(input("Enter the number of the category you want: "))
        ship_category = hull_types[int(choice)-1]

        print("Possible hulls in this category are:")
        for i in range(1, len(ship_type_dict[ship_category])+1):
            print(str(i) + ": " + ship_type_dict[ship_category][i-1])
        choice = int(input("Enter the number of the hull you want, or 0 to go back: "))
        if choice > 0:
            ship_hull = ship_type_dict[ship_category][int(choice)-1]
            break
        else:
            continue

    except ValueError: 
        print("That is not a valid integer! Try again.")

print("Chosen refit: " + ship_hull)
print("This refit has: ")
for i in range(1, len(ship_slots_dict[ship_hull])):
    print(str(ship_slots_dict[ship_hull][i][1]) + "x " + ship_slots_dict[ship_hull][i][0])