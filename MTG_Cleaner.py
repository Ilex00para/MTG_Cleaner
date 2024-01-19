import pandas as pd
import pandas as pdb
import json

# This part is only needed if new data need to be read in otherwise use MTG_LOP_data.csv / see below

# important some internodes have no number but they are marked as N
"""
mtg = pd.read_csv("General_raw_data/MTGs_FINAL.csv")

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
data_on_lop_dates.to_csv("General_raw_data/MTG_LOP_Data.csv", index= False)
"""

# IMPORT of the Data
'_________________________________________________________________'
mtg = pd.read_csv("C:/Users/jacob/pythonProject/General_raw_data/MTG_Files/MTGs_FINAL.csv")
# the mtg file needs an ID column which is used otherwise KeyError
try:
    mtg = mtg.loc[:, "ID"].dropna()
except KeyError:
    print("It seems the there is no column called ID. The ID column must to contain IDs of the following order:\n"
          "20231212.CELL32.E4.Order1.Order2.Order3\n"
          "Date = 20231212, Cell = CELL32, Plant ID = E4")
MTG_dict = {}
'_________________________________________________________________'


# FUNCTIONS


def create_plant_statistic(id):
    plant_statistic_template = {
        "Plant base": [0],
        "Internode Main Stem": [0, []],
        "Internode Side Branch": [0, []],
        "Cotyledon": [0, []],
        "Leaf Main Stem": [0, []],
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
        order_one = order_one[0] + '000'
        return order_one.upper()
    else:
        if len(order_one) == 2:
            # adds two zeros if I and num. = I00num
            if order_one[0].upper() == 'I' and order_one[1].isnumeric():
                order_one = order_one[0].upper() + '00' + order_one[1]
                return order_one.upper()
            else:
                if 'A' in order_one.upper():
                    print(f"Index: {row_index} has an A in it")
                else:
                    print(f"Index: {row_index} has an unusual format")
        elif len(order_one) == 3:
            if order_one[0].upper() == 'I' and order_one[1:3].isnumeric():
                order_one = order_one[0].upper() + '0' + order_one[1:3]
                return order_one.upper()
            if order_one[0].upper() == 'I' and 'A' in order_one.upper():
                if order_one[1].upper() == 'A' and order_one[2].isnumeric():
                    order_one = order_one[0].upper() + order_one[1].upper() + '0' + order_one[2]
                    return order_one.upper()
                else:
                    print(f"Index: {row_index} has an unusual format")
        elif len(order_one) == 4:
            if order_one[0].upper() == 'I' and 'A' in order_one.upper():
                if order_one[1].upper() != 'A':
                    print(f"Index: {row_index} has an unusual format")
                else:
                    return order_one.upper()


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
    if order_three == '' or order_three == None:
        order_three = '0000'
    else:
        if order_three[0] == 'X':
            if order_three[1] == 'L':
                order_three = 'XL01'
            elif order_three[1] == 'T':
                order_three = 'XT00'
        else:
            print(f"Index: {row_index} has a unusual branching.")
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
        #o3 = format_order_three(o2, row_index)
    return o1, o2, o3


'_________________________________________________________________'


def clean(mtg):
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
                id = drop_As(id)  # removes As from the id
                o1, o2, o3 = format_the_orders(id, row_index)

                #print(f"{}")

        except KeyError:
            create_plant_statistic(id)


clean(mtg)
