# Ship Generator V3
# Ver 0.5.0
import csv, random, os
from config.definintions import ROOT_DIR

class Spaceship:

    def __init__(self):
        #load from CSV
        hull_types = []
        for i in os.listdir(os.path.join(ROOT_DIR, 'ships')):
            hull_types.append(i.split(".")[0])

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
                    for y in range(int(row[i*2+1])):
                        ship_slots_dict[row[0]].append(row[i*2])

        
        slot_types = []
        for i in os.listdir(os.path.join(ROOT_DIR, 'modules')):
            slot_types.append(i.split(".")[0])
        ship_modules_dict = {}
        module_stats_dict = {}
        for x in range(len(slot_types)):
            ship_modules_dict[slot_types[x]] = []
            file = list(csv.reader(open(os.path.join(ROOT_DIR, 'modules', slot_types[x] + ".csv"))))
            for i in range(len(file)):
                ship_modules_dict[slot_types[x]].append(file[i][0])
            for row in file:
                    module_stats_dict[row[0]] = row[1:]
        
        
        #determine ship type and refit
        print("Possible categories are:")
        for i in range(1, len(hull_types)+1):
            print(str(i) + ": " +hull_types[i-1])
        choice = input("Enter the number of the category you want, or 0 for a random ship: ")
        if int(choice) < 1:
            self.ship_category = random.choice(hull_types)
            self.ship_hull = ship_type_dict[self.ship_category][random.randrange(len(ship_type_dict[self.ship_category]))]
        else:
            self.ship_category = hull_types[int(choice)-1]
        
            print("Possible hulls in this category are:")
            for i in range(1, len(ship_type_dict[self.ship_category])+1):
                print(str(i) + ": " + ship_type_dict[self.ship_category][i-1])
            choice = input("Enter the number of the hull you want, or 0 for random: ")
            if int(choice) < 1:
                self.ship_hull = ship_type_dict[self.ship_category][random.randrange(len(ship_type_dict[self.ship_category]))]
            else:
                self.ship_hull = ship_type_dict[self.ship_category][int(choice)-1]

        
        count = 0
        while True:
            #find the slots for the hull
            self.fitting_space_remaining = int(ship_slots_dict[self.ship_hull][0])
            slots_remaining = ship_slots_dict[self.ship_hull][1:]

            #randomly pick modules for the hull
            self.modules = []
            self.power_remaining = 0
            repeat_dict = {x: [] for x in slots_remaining}

            while slots_remaining:
                slot = slots_remaining.pop(0)
                #set the module
                if len(repeat_dict[slot]) > 0:
                    latest_module = repeat_dict[slot].pop(0)
                else:
                    latest_module = random.choice(ship_modules_dict[slot])
                    if latest_module not in repeat_dict[slot]:
                        #probably a way to do this with list comprehension
                        for repeats in range(int(module_stats_dict[latest_module][2])):
                            repeat_dict[slot].append(latest_module)

                self.modules.append(latest_module)

                #read the module's stats
                self.fitting_space_remaining -= int(module_stats_dict[latest_module][0])
                self.power_remaining += int(module_stats_dict[latest_module][1])

            count += 1
                
            if (self.fitting_space_remaining >= 0 and self.power_remaining >= 0) or count > 250:
                break
        
        #clean up the list of modules to store type and number
        unique_modules = []
        count = []
        for i in self.modules:
            if i not in unique_modules:
                unique_modules.append(i)
                count.append(self.modules.count(i))
        self.modules = []
        for i in range(len(unique_modules)):
            self.modules.append([unique_modules[i], count[i]])
                
            
    def __str__(self):
        output = self.ship_hull + " (" + self.ship_category + ")\n"
        output += "Power Remaining: " + str(self.power_remaining) + "\n"
        output += "Fitting Space Remaining: "+ str(self.fitting_space_remaining) + "\n"
        output += "List of Modules:\n"

        for i in self.modules:
            if i[1] > 1:
                output += i[0] + " x" + str(i[1]) + "\n"
            else:
                output += i[0] + "\n"
        return output

Spaceship = Spaceship()
print(Spaceship)