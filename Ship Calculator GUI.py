# Ship Calculator - GUI Edition
# Ver 0.1.0
from tkinter import *
from tkinter import ttk
from copy import deepcopy

from config.definintions import ROOT_DIR
import csv, os

class ShipCalculator:
    def __init__(self):
        self.load_from_csv()

        self.power_use = 0
        self.power_total = 0
        self.fitting_space_use = 0
        self.fitting_space_total = 0
        self.part_selection_level = 0
        self.slots_remaining = []
        self.modules = []
        self.slots_filled_list = []

        self.root = Tk()
        self.root.title("Ship Fitting Calculator")

        self.mainframe = ttk.Frame(self.root)
        self.mainframe.grid(column=0,row=0,sticky=("N","S","E","W"))

        self.class_selection = StringVar(value="Category selection...")
        self.class_selector_CB = ttk.Combobox(self.mainframe, textvariable=self.class_selection, values=["Freeform Mode"] + self.hull_types, state="readonly", width=48)
        self.class_selector_CB.grid(column=0, row=0, sticky=("W", "N"))
        self.class_selector_CB.bind('<<ComboboxSelected>>', lambda e : self.update_ship_selector())

        self.ship_selection = StringVar(value="Ship selection...")
        self.ship_selector_CB = ttk.Combobox(self.mainframe, textvariable=self.ship_selection, state="readonly", width=48)
        self.ship_selector_CB.grid(column=2, row=0, sticky=("E", "N"))
        self.ship_selector_CB.bind('<<ComboboxSelected>>', lambda e : self.ship_selected())

        self.parts_listvar = StringVar()
        self.module_selector_LB = Listbox(self.mainframe, listvariable=self.parts_listvar, width=48, height=16)
        self.module_selector_LB.grid(column=0, row=1, sticky=("S", "N", "W"))
        self.module_selector_LB.bind("<<ListboxSelect>>", lambda e : self.part_selection())

        self.fittings_listvar = StringVar()
        self.fittings_display_LB = Listbox(self.mainframe, listvariable=self.fittings_listvar, width=48, height=16)
        self.fittings_display_LB.grid(column=2, row=1, sticky=("S", "N", "E"))
        self.fittings_display_LB.bind("<<ListboxSelect>>", lambda e : self.remove_part())

        self.total_use_lbl = ttk.Label(self.mainframe, text="Fitting Space Remaining: 0\nPower Remaining: 0")
        self.total_use_lbl.grid(column=1, row=1)
        
        self.back_btn = ttk.Button(self.mainframe, text="Back", command=self.back_button_pressed)
        self.back_btn.grid(column=0, row=2)

        self.reset_btn = ttk.Button(self.mainframe, text="Reset", command=self.reset_button_pressed)
        self.reset_btn.grid(column=2, row=2)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.columnconfigure(2, weight=1)

        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=1)
        
        self.print_btn = ttk.Button(self.mainframe, text="Print", command=self.print_modules)
        self.print_btn.grid(column=1, row=2)

        self.output_box = Text(self.mainframe)
        self.output_box.grid(column=0, row=3, columnspan=3)

        self.root.mainloop()
    
    def load_from_csv(self): 
        self.hull_types = []
        for i in os.listdir(os.path.join(ROOT_DIR, 'ships')):
            self.hull_types.append(i.split(".")[0])

        self.ship_type_dict = {}
        self.ship_slots_dict = {}
        for x in range(len(self.hull_types)):
            self.ship_type_dict[self.hull_types[x]] = []
            file = list(csv.reader(open(os.path.join(ROOT_DIR, 'ships', self.hull_types[x] + ".csv"))))
            for i in range(len(file)):
                self.ship_type_dict[self.hull_types[x]].append(file[i][0])
            for row in file:   
                self.ship_slots_dict[row[0]] = [row[1]]
                for i in range(1, int(len(row)/2)):
                    self.ship_slots_dict[row[0]].append([row[i*2], int(row[i*2+1])])

        self.slot_types_list = []
        for i in os.listdir(os.path.join(ROOT_DIR, 'modules')):
            self.slot_types_list.append(i.split(".")[0])

        self.ship_modules_dict = {}
        self.module_stats_dict = {}
        for x in range(len(self.slot_types_list)):
            self.ship_modules_dict[self.slot_types_list[x]] = []
            file = list(csv.reader(open(os.path.join(ROOT_DIR, 'modules', self.slot_types_list[x] + ".csv"))))
            for i in range(len(file)):
                self.ship_modules_dict[self.slot_types_list[x]].append(file[i][0])
            for row in file:
                    self.module_stats_dict[row[0]] = row[1:]
                    self.module_stats_dict[row[0]].append(self.slot_types_list[x])

        self.slot_types_dict = {}
        self.slot_sizes_list = []
        for i in range(len(self.slot_types_list)):
            if self.slot_types_list[i].split()[0] not in self.slot_sizes_list:
                self.slot_sizes_list.append(self.slot_types_list[i].split()[0])
        
        for i in range(len(self.slot_sizes_list)):
            self.slot_types_dict[self.slot_sizes_list[i]] = []
            for x in range(len(self.slot_types_list)):
                if self.slot_types_list[x].split()[0] == self.slot_sizes_list[i]:
                    self.slot_types_dict[self.slot_sizes_list[i]].append(self.slot_types_list[x])

    def update_ship_selector(self):
        self.class_selector_CB.selection_clear()
        if self.class_selection.get() == "Freeform Mode":
            self.ship_selector_CB.state(["disabled"])
            self.dialogue_box = Toplevel(self.root)
            subframe = ttk.Frame(self.dialogue_box)
            subframe.grid(column=0, row=0, sticky=("N", "E", "S", "W"))

            self.fitting_space_entry_variable = StringVar()
            fitting_space_entry = ttk.Entry(subframe, textvariable=self.fitting_space_entry_variable)
            enter_btn = ttk.Button(subframe, text="Confirm", command=self.set_fitting_space)
            direction_lbl = ttk.Label(subframe, text="Enter the fitting space of the ship:")
            fitting_space_entry.grid(row=1, column=0)
            enter_btn.grid(row=1, column=1, sticky=("S", "E"))
            direction_lbl.grid(row=0, column=0)
        else:
            self.ship_selector_CB.state(["!disabled"]) 
            self.ship_selector_CB["values"] = self.ship_type_dict[self.class_selection.get()]

    def update_running_total(self):
        self.fitting_space_remaining = self.fitting_space_total - self.fitting_space_use
        self.power_remaining = self.power_total - self.power_use
        output = "Fitting Space Remaining: " + str(self.fitting_space_remaining) + " (" + str(self.fitting_space_total) + ")"
        output += "\nPower Remaining: " + str(self.power_remaining) + " (" + str(self.power_total) + ")"
        self.total_use_lbl["text"] = output
    
    def set_fitting_space(self):
        self.part_selection_level = 0
        self.fitting_space_total = int(self.fitting_space_entry_variable.get())
        self.parts_listvar.set(self.slot_sizes_list)
        self.ship_selection.set("Ship selection...")
        self.dialogue_box.destroy()
        self.reset_button_pressed()
        self.update_running_total()
        self.update_module_list()

    def ship_selected(self):
        self.part_selection_level = 0
        self.ship_selector_CB.selection_clear()
        self.fitting_space_total = int(deepcopy(self.ship_slots_dict[self.ship_selection.get()][0]))
        self.slots_remaining = deepcopy(self.ship_slots_dict[self.ship_selection.get()][1:])
        self.parts_listvar.set([str(str(x[1]) + "x " + x[0]) for x in self.slots_remaining if x[1] > 0])
        self.update_running_total()
        self.reset_button_pressed()

    def part_selection(self):
        if self.class_selection.get() == "Freeform Mode":
            if len(self.module_selector_LB.curselection()):
                if self.part_selection_level == 0:
                    self.parts_listvar.set(self.slot_types_dict[self.module_selector_LB.selection_get()])
                    self.module_selector_LB.selection_clear(0, END)
                    self.part_selection_level = 1
                elif self.part_selection_level == 1:
                    self.parts_listvar.set(self.ship_modules_dict[self.module_selector_LB.selection_get()])
                    self.module_selector_LB.selection_clear(0, END)
                    self.part_selection_level = 2
                elif self.part_selection_level == 2:
                    self.part_added(self.module_selector_LB.selection_get())
                    self.module_selector_LB.selection_clear(0, END)
                    self.parts_listvar.set(self.slot_sizes_list)  
        else:
            if self.part_selection_level == 0:
                self.slot = ""
                if len(self.module_selector_LB.curselection()) > 0:
                    for i in self.module_selector_LB.selection_get().split()[1:]:
                        self.slot += i + " "

                    self.slot = self.slot.strip()
                    self.parts_listvar.set(self.ship_modules_dict[self.slot])
                    self.part_selection_level = 1
                    self.module_selector_LB.selection_clear(0, END)
            elif self.part_selection_level == 1:
                self.part_added(self.module_selector_LB.selection_get())
                self.parts_listvar.set([str(str(x[1]) + "x " + x[0]) for x in self.slots_remaining if x[1] > 0])

    def back_button_pressed(self):
        if self.part_selection_level > 0:
            self.module_selector_LB.selection_clear(0, END)
            self.part_selection_level -= 1
            if self.part_selection_level == 0:
                if self.class_selection.get() != "Freeform Mode":
                    self.parts_listvar.set([str(str(x[1]) + "x " + x[0]) for x in self.slots_remaining if x[1] > 0])
                else:
                    self.parts_listvar.set(self.slot_sizes_list)
            elif self.part_selection_level == 1 and self.class_selection.get() != "Freeform Mode":
                pass
            self.update_running_total()
            self.part_selection()

    def part_added(self, part):
        self.part_selection_level = 0
        self.fitting_space_use += deepcopy(int(self.module_stats_dict[part][0]))
        if int(self.module_stats_dict[part][1]) < 0:
            self.power_use -= deepcopy(int(self.module_stats_dict[part][1]))
        self.modules.append(part)
        for i in range(len(self.slots_remaining)):
            if self.slot in self.slots_remaining[i] and self.slots_remaining[i][1] > 0:
               self.slots_remaining[i][1] -= 1
        if int(self.module_stats_dict[part][1]) > 0:
            self.power_total += deepcopy(int(self.module_stats_dict[part][1]))
    
        self.update_running_total()
        self.update_module_list()

    def update_module_list(self):
        unique_modules = []
        count = []
        for i in self.modules:
            if i not in unique_modules:
                unique_modules.append(i)
                count.append(self.modules.count(i))
        self.clean_modules = []
        for i in range(len(unique_modules)):
            self.clean_modules.append([unique_modules[i], count[i]])

        output = []
        for i in self.clean_modules:
            if i[1] > 1:
                output.append(str(i[1])+ "x " + i[0])
            else:
                output.append(i[0])
        
        self.fittings_listvar.set(output)


    def remove_part(self):
        if len(self.fittings_display_LB.curselection()) > 0:
            removal = ""
            index = self.fittings_display_LB.curselection()[0]
            removal = self.clean_modules[index][0]

            self.fitting_space_use -=deepcopy(int(self.module_stats_dict[removal][0]))            
            if int(self.module_stats_dict[removal][1]) > 0:
                self.power_total -= deepcopy(int(self.module_stats_dict[removal][1]))
            else:
                self.power_use += deepcopy(int(self.module_stats_dict[removal][1]))
            self.modules.remove(removal)
            for i in self.slots_remaining:
                if i[0] == self.module_stats_dict[removal][3]:
                    i[1] += 1

            self.update_running_total()
            self.update_module_list()
            self.fittings_display_LB.selection_clear(0, END)
            if self.class_selection.get() != "Freeform Mode":
                self.parts_listvar.set([str(str(x[1]) + "x " + x[0]) for x in self.slots_remaining if x[1] > 0])

    def reset_button_pressed(self):
        if self.class_selection.get() != "Freeform Mode":
            self.fitting_space_total = int(deepcopy(self.ship_slots_dict[self.ship_selection.get()][0]))
            self.slots_remaining = deepcopy(self.ship_slots_dict[self.ship_selection.get()][1:])
            self.parts_listvar.set([str(str(x[1]) + "x " + x[0]) for x in self.slots_remaining if x[1] > 0])

        self.fitting_space_use = 0
        self.power_use = 0
        self.power_total = 0
        self.modules = []
        self.update_running_total()
        self.update_module_list()
        self.print_modules()
    
    def print_modules(self):
        self.output_box.delete("1.0", "end")
        output = "Power Remaining: " + str(self.power_remaining) + " (" + str(self.power_total) + ")\n"
        output += "Fitting Space Remaining: " + str(self.fitting_space_remaining) + " (" + str(self.fitting_space_total) + ")\n"
        output += "List of Modules:\n"

        for i in self.clean_modules:
            if i[1] > 1:
                output += i[0] + " x" + str(i[1]) + "\n"
            else:
                output += i[0] + "\n"
        self.output_box.insert("1.0", output)


ShipCalculator()