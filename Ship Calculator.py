# Companion Ship Fitting Calculator to the Ship Generator V3
# Ver 0.1.2

import csv, os
from sys import modules
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
                ship_slots_dict[row[0]].append((row[i*2], int(row[i*2+1])))

    global slot_types_list
    slot_types_list = []
    for i in os.listdir(os.path.join(ROOT_DIR, 'modules')):
        slot_types_list.append(i.split(".")[0])

    global ship_modules_dict
    global module_stats_dict
    ship_modules_dict = {}
    module_stats_dict = {}
    for x in range(len(slot_types_list)):
        ship_modules_dict[slot_types_list[x]] = []
        file = list(csv.reader(open(os.path.join(ROOT_DIR, 'modules', slot_types_list[x] + ".csv"))))
        for i in range(len(file)):
            ship_modules_dict[slot_types_list[x]].append(file[i][0])
        for row in file:
                module_stats_dict[row[0]] = row[1:]

    global slot_types_dict
    slot_types_dict = {}
    slot_sizes_list = []
    for i in range(len(slot_types_list)):
        if slot_types_list[i].split()[0] not in slot_sizes_list:
            slot_sizes_list.append(slot_types_list[i].split()[0])
    
    for i in range(len(slot_sizes_list)):
        slot_types_dict[slot_sizes_list[i]] = []
        for x in range(len(slot_types_list)):
            if slot_types_list[x].split()[0] == slot_sizes_list[i]:
                slot_types_dict[slot_sizes_list[i]].append(slot_types_list[x])

def existing_refit():
    for i in range(len(ship_slots_dict[ship_hull][1:])):
        slots_remaining = dict(ship_slots_dict[ship_hull][1:])

    global fitting_space
    fitting_space = int(ship_slots_dict[ship_hull][0])
    global power
    global modules
    fitting_space_cap = fitting_space
    power_cap = 0
    modules = []
    while True:
        try:
            print("Chosen refit: " + ship_hull)
            print("This refit has: ")

            print(str(fitting_space) + " fitting space remaining")
            print(str(power) + " power remaining")
            for i in slots_remaining.keys():
                if slots_remaining[i] > 0:
                    print(str(slots_remaining[i]) + "x " + str(i))

            print()
            print("1: Choose a new module")
            print("2: Print the ship")
            print("3: Quit")
            choice = int(input("Selection: "))
            if choice == 1:
                print("Possible slots:")
                slot_key = []
                i = 0
                for key in slots_remaining.keys():
                    if slots_remaining[key] > 0:
                        print(str(i+1) + ": " + str(key))
                    i += 1
                    slot_key.append(key)

                choice_slot = int(input("Selection: "))
                print("Possible modules:")
                slot = slot_key[choice_slot-1]
                for i in range(1, len(ship_modules_dict[slot])+1):
                    print(str(i) + ": " + str(ship_modules_dict[slot][i-1]))
                choice = int(input("Selection: "))
                module = ship_modules_dict[slot][choice-1]
                power += int(module_stats_dict[module][1])
                fitting_space -= int(module_stats_dict[module][0])
                modules.append(module)
                
                if int(module_stats_dict[module][1]) > 0:
                    power_cap += int(module_stats_dict[module][1])
                slots_remaining[slot] -= 1
                continue

            if choice == 2:
                unique_modules = []
                count = []
                for i in modules:
                    if i not in unique_modules:
                        unique_modules.append(i)
                        count.append(modules.count(i))
                clean_modules = []
                for i in range(len(unique_modules)):
                    clean_modules.append((unique_modules[i], count[i]))
                output = ""
                output += "Power Remaining: " + str(power) + " (" + str(power_cap) + ")\n"
                output += "Fitting Space Remaining: " + str(fitting_space) + " (" + str(fitting_space_cap) + ")\n"
                output += "List of Modules:\n"
                for i in clean_modules:
                    if i[1] > 1:
                        output += i[0] + " x" + str(i[1]) + "\n"
                    else:
                        output += i[0] + "\n"
                print(output)
                continue
            if choice == 3:
                break

        except ValueError: 
            print("That is not a valid integer! Try again.")
        except IndexError: 
            print("That is out of range! Try again.")

def new_refit():
    global fitting_space
    global power
    global modules
    modules = []
    fitting_space_cap = fitting_space
    power_cap = 0
    while True:
        print("Fitting space remaining: " + str(fitting_space))
        print("Power remaining: " + str(power))
        try:
            print()     
            print("1: Choose a new module")
            print("2: Print the ship")
            print("3: Quit")
            choice = int(input("Selection: "))
            if choice == 1:
                print("Possible sizes: ")
                for i in range(len(slot_types_dict.keys())):
                    print((str(i+1) + ": " + list(slot_types_dict.keys())[i]))

                choice = int(input("Selection: "))

                possible_slots = slot_types_dict[list(slot_types_dict.keys())[choice-1]]
                print("Possible slots:")
                for i in range(len(possible_slots)):
                    print(str(i+1) + ": " + possible_slots[i])
                choice = int(input("Selection: "))
                
                possible_modules = ship_modules_dict[possible_slots[choice-1]]
                print("Possible modules:")
                for i in range(len(possible_modules)):
                    print(str(i+1) + ": " + possible_modules[i])
                choice = int(input("Selection: "))

                module = possible_modules[choice-1]
                power += int(module_stats_dict[module][1])
                fitting_space -= int(module_stats_dict[module][0])
                if int(module_stats_dict[module][1]) > 0:
                    power_cap += int(module_stats_dict[module][1])
                modules.append(module)
                continue

            if choice == 2:
                unique_modules = []
                count = []
                for i in modules:
                    if i not in unique_modules:
                        unique_modules.append(i)
                        count.append(modules.count(i))
                clean_modules = []
                for i in range(len(unique_modules)):
                    clean_modules.append((unique_modules[i], count[i]))
                output = ""
                output += "Power Remaining: " + str(power) + " (" + str(power_cap) + ")\n"
                output += "Fitting Space Remaining: " + str(fitting_space) + " (" + str(fitting_space_cap) + ")\n"
                output += "List of Modules:\n"
                for i in clean_modules:
                    if i[1] > 1:
                        output += i[0] + " x" + str(i[1]) + "\n"
                    else:
                        output += i[0] + "\n"
                print(output)
                continue
            if choice == 3:
                break
     

        except ValueError: 
            print("That is not a valid integer! Try again.")
        except IndexError: 
            print("That is out of range! Try again.")


load_from_csv()
while True:
    try:
        print("Possible categories are:")
        for i in range(1, len(hull_types)+1):
            print(str(i) + ": " +hull_types[i-1])
        choice = int(input("Enter the number of the category you want, zero for freeform mode, or -1 to quit: "))
        if choice > 0:   
            ship_category = hull_types[int(choice)-1]
            print("Possible hulls in this category are:")
            for i in range(1, len(ship_type_dict[ship_category])+1):
                print(str(i) + ": " + ship_type_dict[ship_category][i-1])
            choice = int(input("Enter the number of the hull you want, or 0 to go back: "))
            if choice > 0:
                ship_hull = ship_type_dict[ship_category][int(choice)-1]
                power = 0
                existing_refit()
                continue
            else:
                continue
        elif choice < 0:
            break
        else:
            fitting_space = int(input("Enter the fitting space of your ship: "))
            power = 0
            new_refit()
            continue

    except ValueError: 
        print("That is not a valid integer! Try again.")
    except IndexError: 
        print("That is out of range! Try again.")
