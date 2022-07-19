# ship_generator

This is the third attempt at my creation of a random spaceship generator. To use the prebuilt .csv files, unzip the zip file in whatever directory that you are keeping the generator in. Documentation is as follows:

Ships are composed of hulls and modules. Each module belongs to a slot, and each hull has a number of slots defining what modules can generate there. 

In the ships subdirectory, each hull belongs to a ship type (i.e. Light Freighter) that is denoted by a csv file. The first entry on each line is the name, the second is the fitting space (which determines which modules can fit on the hull) and each item after this is the slot type and number of that slot.

In the modules subdirectory, each module belongs to a slot (i.e. Small FTL) that is denoted by a csv file. The first entry on each line is the name, the second entry is the size, the third entry is the power use, and the fourth entry is the number of times the module should be repeated. This is used to ensure that some modules (i.e nacelles) always generate in pairs.
