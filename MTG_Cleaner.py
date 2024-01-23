import numpy as np
import pandas as pd
import pandas as pdb
import json

# This part is only needed if new data need to be read in otherwise use MTG_LOP_data.csv / see below

# important some internodes have no number but they are marked as N
"""
mtg = pd.read_csv("C:/Users/jacob/pythonProject/General_raw_data/MTG_Files/MTGs_FINAL.csv")

print(mtg.columns)
print(mtg.loc[:,"Date"].unique())

# create a subdataset with only the three dates in need
data_on_lop_dates = []

list_of_dates = [20231113, 20231114, 20231115, 20231211, 20231212, 20231213, 20240110]
print(type(list_of_dates[-1]))

for row_index in range(len(mtg)):
    try:
        line = mtg.loc[row_index]
        ID = str(mtg.loc[row_index,"ID"])
        ID = float(ID[0:8])
        ID = int(ID)
        if ID in list_of_dates:
            data_on_lop_dates.append(line)
    except TypeError:
        print(f"On index {row_index} the following value occurs: {ID, type(ID)}")
    except ValueError:
        print(f"On index {row_index} the following value occurs: {ID, type(ID)}")

data_on_lop_dates = pd.DataFrame(data=data_on_lop_dates)
data_on_lop_dates.to_csv("C:/Users/jacob/pythonProject/General_raw_data/MTG_Files/MTGs_LOP_Data.csv", index= False)
"""

# IMPORT of the Data
'_________________________________________________________________'
mtg = pd.read_csv("C:/Users/jacob/pythonProject/General_raw_data/MTG_Files/MTGs_FINAL.csv")
# Selects only the ID column and drops all the empty cells which are usually at the end of an Excel file
mtg = mtg['ID'].dropna()
# the mtg file needs an ID column which is used otherwise KeyError
'_________________________________________________________________'


# FUNCTIONS

def create_plant_statistic(id, MTG_dict):
    plant_statistic_template = {
        "Plant base": [0],
        "Internode Main Stem": [0, []],
        "Internode Side Branch": [0, {}],
        "Cotyledon": [0, []],
        "Leaf Main Stem": [0, {}],
        "Leaf Side Branch": [0, {}],
        "Shoot": [0, []],
        "Truss": [0, []]
    }
    if id[0:8] not in MTG_dict:
        MTG_dict[id[0:8]] = {}
    if id[9:15] not in MTG_dict[id[0:8]]:
        MTG_dict[id[0:8]][id[9:15]] = {}
    if id[16:18] not in MTG_dict[id[0:8]][id[9:15]]:
        MTG_dict[id[0:8]][id[9:15]][id[16:18]] = {}
    if id[19:20] == '0':
        MTG_dict[id[0:8]][id[9:15]][id[16:18]]["Plant_Statistic"] = plant_statistic_template
        # print(f" {row_index} PLANT {id[16:18]} created.")



def format_order_one(order_one, row_index):
    if order_one[0].upper() == 'T':
        order_one = order_one[0].upper() + '000'
    elif order_one[0].upper() == 'S':
        order_one = 'S000'
    else:
        if len(order_one) == 2:
            # adds two zeros if I and num. = I00num
            if order_one[0].upper() == 'I' and order_one[1].isnumeric():
                order_one = order_one[0].upper() + '00' + order_one[1]
            else:
                if 'A' in order_one.upper():
                    print(f"Index: {row_index} has an A in it")
                else:
                    print(f"Index: {row_index} has an unusual format. {order_one}")
        elif len(order_one) == 3:
            if order_one[0].upper() == 'I' and order_one[1:3].isnumeric():
                order_one = order_one[0].upper() + '0' + order_one[1:3]
            if order_one[0].upper() == 'I' and 'A' in order_one.upper():
                if order_one[1].upper() == 'A' and order_one[2].isnumeric():
                    order_one = order_one[0].upper() + order_one[1].upper() + '0' + order_one[2]
                else:
                    print(f"Index: {row_index} has an unusual format. {order_one}")
        elif len(order_one) == 4:
            if order_one[0].upper() == 'I' and 'A' in order_one.upper():
                if order_one[1].upper() != 'A':
                    print(f"Index: {row_index} has an unusual format. {order_one}")
    if len(order_one) == 4 and order_one != None:
        return order_one.upper()
    else:
        print(f"Index: {row_index} something went wrong. Order 1: {order_one}")


def format_order_two(order_two, row_index):
    if order_two == '' or order_two == (None):
        order_two = '0000'
    else:
        len_order_2 = len(order_two)
        if len_order_2 == 1:
            if order_two[0] == 'T':
                order_two = 'T000'
            elif order_two[0] == 'S':
                order_two = 'S000'
            elif order_two[0] == 'I':
                order_two = 'I00N'
        if len_order_2 > 1:
            if order_two[0] == 'X':
                if order_two[1] == 'S':
                    order_two = 'XS00'
                elif order_two[1] == 'T':
                    order_two = 'XT00'
                elif order_two[1] == 'L':
                    order_two = 'XL01'
                elif order_two[1] == 'C':
                    order_two = 'XC0' + str(order_two[-1])
                elif order_two[1] == 'I':
                    order_two = 'XI01'
            else:
                if order_two[0] == 'S':
                    order_two = 'S000'
                elif order_two[0] == 'T':
                    order_two = 'T000'
                elif order_two[0] == 'L':
                    order_two = 'L001'
                elif order_two[0] == 'I':
                    order_two = 'I00' + order_two[-1]

    if len(order_two) == 4:
        return order_two
    else:
        print(f"Index: {row_index} is not 4 digits long. Order two: {order_two}")


def format_order_three(order_three, row_index):
    if order_three == '' or order_three == None or order_three == '0':
        order_three = '0000'
    else:
        if order_three[0] == 'X':
            if order_three[1] == 'L':
                order_three = 'XL01'
            elif order_three[1] == 'T':
                order_three = 'XT00'
            elif order_three[1] == 'I':
                order_three = 'XI01'
            elif order_three[1] == 'S':
                order_three = 'XS00'
        else:
            if order_three[0] == 'I':
                order_three = 'I00N'
            elif order_three[0] == 'S':
                order_three = 'S000'
            elif order_three[0] == 'T':
                order_three = 'T000'
            elif order_three[0] == 'L':
                order_three = 'L00N'

    if len(order_three) == 4:
        return order_three
    else:
        print(f"Index: {row_index} is not 4 digits long. Order 3: {order_three}")


def drop_As(id):
    if "A" in id:
        letter_to_drop = 'A'
        # Drop all occurrences of 'A'
        id = id.replace(letter_to_drop, '')
        return id
    else:
        return id


def format_the_orders(id, row_index):
    o1, o2, o3 = id[19:].split(".")
    if o1 != '':
        o1 = format_order_one(o1, row_index)
        o2 = format_order_two(o2, row_index)
        o3 = format_order_three(o3, row_index)
    return o1, o2, o3


def add_info_to_array(id, o1, o2, o3, row_index):
    single_info_array = np.zeros((1, 24))
    for i, i_id in enumerate(id[0:8]):
        single_info_array[:, i] = ord(i_id)
    # too ASCII code
    single_info_array[:, 8] = ord(id[13])
    single_info_array[:, 9] = ord(id[14])
    single_info_array[:, 10] = ord(id[16])
    single_info_array[:, 11] = ord(id[17])
    for index_shift, order in zip([12, 16, 20], [o1, o2, o3]):
        try:
            for i, i_id in enumerate(order):
                i = i + index_shift
                single_info_array[:, i] = ord(i_id)
        except TypeError:
            print(f"Index {row_index}: The variable order (= {order}) has the type {type(order)} and is not string.")
    return single_info_array


# functions to read the ASCII
def get_date(row_array):
    output_string = ''
    for element in row_array[0:8]:
        output_string += chr(element)
    return output_string


def get_cell(row_array):
    output_string = ''
    for element in row_array[8:10]:
        output_string += chr(element)
    return output_string


def get_plant(row_array):
    output_string = ''
    for element in row_array[10:12]:
        output_string += chr(element)
    return output_string


def get_order_1(row_array):
    output_string = ''
    for element in row_array[12:16]:
        output_string += chr(element)
    return output_string


def get_order_2(row_array):
    output_string = ''
    for element in row_array[16:20]:
        output_string += chr(element)
    return output_string


def get_order_3(row_array):
    output_string = ''
    for element in row_array[20:25]:
        output_string += chr(element)
    return output_string


def get_internode_number(internode_number):
    if len(str(internode_number)) == 1:
        internode_number = f"00{internode_number}"
    elif len(str(internode_number)) == 2:
        internode_number = f"0{internode_number}"
    return internode_number


'_________________________________________________________________'


def clean(mtg, out_array = True, out_dictionary = True):
    MTG_dict = {}
    mtg_array = np.zeros((1, 24))
    # loops through all the data in the mtg data file (.csv)
    for row_index in range(len(mtg)):
        try:
            id = mtg[row_index].upper()
        except AttributeError:
            print("error", mtg[row_index], type(mtg[row_index]))

        # key error is triggered if the plant statistic is not yet created
        try:
            # cleaning of the data
            if MTG_dict[id[0:8]][id[9:15]][id[16:18]]["Plant_Statistic"]["Plant base"][0] == 0:
                # removes As from the id
                id = drop_As(id)
                # splits the id in the three orders and cleans each order separately raises error if mistake occurs
                o1, o2, o3 = format_the_orders(id, row_index)
                # converts data into numpy array with ASCII notation
                mtg_array = np.append(mtg_array, add_info_to_array(id, o1, o2, o3, row_index), axis=0)
        except KeyError:
            create_plant_statistic(id, MTG_dict)
        # before returning the first row of zeros from the mtg_array is deleted
    mtg_array = mtg_array[1:].astype(int)

    stored_o1 = ''
    internode_stored_o2 = ''
    stored_o3 = ''
    for i, row in enumerate(mtg_array):
        date = get_date(row)
        cell = get_cell(row)
        plant = get_plant(row)

        o1 = get_order_1(row)
        o2 = get_order_2(row)
        o3 = get_order_3(row)
        if "I" in o2:
            if internode_stored_o2 != o2:
                if o2[-1] == "N":
                    if "X" in o2:
                        internode_stored_o2 = 'I001'
                    else:
                        try:
                            internode_number_o2 = len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1]) + 1
                            internode_number_o2 = get_internode_number(internode_number_o2)
                            internode_stored_o2 = f'I{internode_number_o2}'
                        except KeyError:
                            print(f"The key {o1} was not found on position {i,date,cell,plant} \n"
                                  f"!!! One possible reason can be that the branching of the first Internode was not indicated. !!!")
                else:
                    if "X" in o2:
                        internode_stored_o2 = 'I001'
                    else:
                        internode_stored_o2 = o2


        if o2 == '0000' and o3 == '0000':
            if o1[0] == 'I':
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Main Stem"][0] += 1
                if o1[-1] == 'N':
                    internode_number = len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Main Stem"][1])+1
                    internode_number = get_internode_number(internode_number)
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Main Stem"][1] += [f"I{internode_number}"]
                else:
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Main Stem"][1] += [o1]
            elif o1[0] == 'S':
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Shoot"][0] += 1
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Shoot"][1] += [o1]
            elif o1[0] == 'T':
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Truss"][0] += 1
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Truss"][1] += [o1]
            else:
                print(f'Problem: Organ can not be identified. Position: Date({date}), Cell({cell}, Plant({plant}, Order 1({o1}))')

        elif o2 != '0000' and o3 == '0000':
            if 'C' in o2:
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Cotyledon"][0] += 1
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Cotyledon"][1] += [o2]
            elif 'L' in o2:
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Main Stem"][0] += 1
                if o1 not in MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Main Stem"][1]:
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Main Stem"][1][o1] = ["L001"]
                else:
                    leaf_number =  len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Main Stem"][1][o1])+1
                    if len(str(leaf_number)) == 1:
                        leaf_number = f"00{leaf_number}"
                    elif len(str(leaf_number)) == 2:
                        leaf_number = f"0{leaf_number}"
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Main Stem"][1][o1] += ['L'+leaf_number]
            # checks for Organ to be an Internode
            elif 'I' in o2:
                # adds one to the counter
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][0] += 1
                # checks if index is unknown by checking the N
                if o2[-1] == 'N':
                    #initialises or resets the index of the side branch
                    index_side_branch = 0
                    # checks if parent of the organ (internode on order 2) is in the dictionary
                    if o1 not in MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1]:
                        # adds the first branching internode
                        MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1] = ["XI01"]
                        index_side_branch = len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1])
                    else:
                        # parent is already known
                        # how many organs are already known from this parent add one to get the number of the current one
                        internode_number = len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1])+1
                        #check if it is not the first branching
                        if MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1][:index_side_branch] == "XI01":
                            # sets the internode number to
                            internode_number = internode_number - len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1][:index_side_branch])
                            internode_number = get_internode_number(internode_number)
                            MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1] += [f"I{internode_number}"]
                else:
                    if o1 not in MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1]:
                        MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1] = [o2]
                    else:
                        MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Internode Side Branch"][1][o1] += [o2]
            elif 'S' in o2:
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Shoot"][0] += 1


        elif o2 == '0000' and o3 != '0000':
            # checks if is a leaf
            if 'L' in o3:
                #counts a leaf
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][0] += 1
                #check if parent is in dictionary if not creates a dict for the grandparent
                if o1 not in MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1]:
                     #creates organ dictionary for grandparent and parent  + adding the organ
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1] = {}
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][internode_stored_o2] = []
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][internode_stored_o2] += ["XL01"]
                else:
                    if internode_stored_o2 not in MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1]:
                        MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][internode_stored_o2] = []
                        leaf_number = len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][internode_stored_o2])+1
                        if leaf_number == 1:
                            leaf_number = f'0{leaf_number}'
                        MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][internode_stored_o2] += [f'XL{leaf_number}']
            elif 'S' in o3:
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Shoot"][0] += 1
                # Description of organ not added yet.
            elif 'T' in o3:
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Truss"][0] += 1
                # Description of organ not added yet.
        elif o2 != '0000' and o3 != '0000':
            #checks if organ is leaf on order three
            if 'L' in o3:
                #counts a leaf
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][0] += 1
                #check if parent is in dictionary if not creates a dict for the grandparent
                if o1 not in MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1]:
                     #creates organ dictionary for grandparent and parent  + adding the organ
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1] = {}
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][o2] = []
                    MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][o2] += ["XL01"]
                else:
                    if internode_stored_o2 not in MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1]:
                        MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][o2] = []
                        leaf_number = len(MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][o2])+1
                        if leaf_number == 1:
                            leaf_number = f'0{leaf_number}'
                        MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Leaf Side Branch"][1][o1][internode_stored_o2] += [f'XL{leaf_number}']
            elif 'S' in o3:
                MTG_dict[date][f"CELL{cell}"][plant]["Plant_Statistic"]["Shoot"][0] += 1
        else:
            print(f"On the index {i} occurred a problem.\n"
                  f"Plant {cell} {plant} has the following organ {o1, o2, o3}.\n")


    if not out_array:
        return MTG_dict
    else:
        return MTG_dict, mtg_array



output_array = clean(mtg, out_array= False)

with open("C:/Users/jacob/pythonProject/General_raw_data/MTG_Files/MTG_ALL_Data_UNCHANGED.json", "w") as writer:
    json.dump(output_array, writer, indent=4)

