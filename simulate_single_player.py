#Simulate a single player playing Catan
#Optimize to reduce the number of turns it takes to get 10 VP's
import random
import numpy.random


def generate_board():
    global turns_taken
    turns_taken = 0

    global victory_points
    victory_points = 2

    global dev_deck
    dev_deck = ["monopoly", "monopoly", "road_building", "road_building", "year_of_plenty", "year_of_plenty", "vp", "vp", "vp", "vp", "vp",
                "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight"]
    numpy.random.shuffle(dev_deck)

    #tiles correspond to numbers
    tiles = {
        0: "dessert",
        1: "wood",
        2: "wheat",
        3: "wool",
        4: "ore",
        5: "brick"
    }

    #Create arrays for hand
    global resource_cards
    resource_cards = {
        "wood": 0,
        "wheat": 0,
        "wool": 0,
        "ore": 0,
        "brick": 0
    }
    global dev_cards
    dev_cards = {
        "vp": 0,
        "knight": 0,
        "monopoly": 0,
        "road_building": 0,
        "year_of_plenty": 0
    }

    #Hex tiles used - 19 total - in the order of [dessert, wood, wheat, wool, ore, brick]
    num_tiles_used = [1, 4, 4, 4, 3, 3]

    #Set up board arrays
    global hex_tiles_arr
    hex_tiles_arr = [] #[[wood, 3], [ore, 11], etc...]
    global settlement_locations_arr
    settlement_locations_arr = []  # vertices
    global road_locations_arr
    road_locations_arr = [] #edges
    global settlements_owned_arr
    settlements_owned_arr = []
    for i in range(72):
        road_locations_arr.append('.') #Change to X when Road is built
    for i in range(54):
        settlement_locations_arr.append([[], [], []]) #Used to determine bordering edges, vertices, and hexes
    for i in range(54):
        settlements_owned_arr.append(0) #Change to 1 if settlement present, 2 if city present, 9 if nothing can be built here

    #Generate Board:
    #Randomly place hex tiles
    total_tiles = 0
    for i in num_tiles_used:
        total_tiles += i
    for j in range(total_tiles):
        picked_valid_num = False
        while picked_valid_num == False:
            x = random.randint(0,5)
            if num_tiles_used[x] > 0:
                hex_tiles_arr.append([tiles[x]])
                num_tiles_used[x] -= 1
                picked_valid_num = True

    #Randomly place circle values on hexes
    num_circle_tiles = [0, 0, 1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1]
    total_circle_tiles = 0
    for j in num_circle_tiles:
        total_circle_tiles += j
    for i in range(total_circle_tiles+1):
        picked_valid_num = False
        if(hex_tiles_arr[i] == ["dessert"]):
            picked_valid_num = True;
        while picked_valid_num == False:
            x = random.randint(2, 12)
            if num_circle_tiles[x] > 0:
                hex_tiles_arr[i].append(x)
                num_circle_tiles[x] -= 1
                picked_valid_num = True
    #Does not account for red circles being next to each other

    #Generate settlements array
    #each vertex: [[bordering hexes], [bordering vertices/settlements], [bordering roads/edges]]
    #settlement_locations_arr["vertex #"]
    settlement_locations_arr[0] = [[0], [1,8], [0,6]]
    settlement_locations_arr[1] = [[0], [0,2], [0,1]]
    settlement_locations_arr[2] = [[0,1], [1,3,10], [1,2,7]]
    settlement_locations_arr[3] = [[1], [2,4], [2,3]]
    settlement_locations_arr[4] = [[1,2], [3,5,12], [3,4,8]]
    settlement_locations_arr[5] = [[2], [4,6], [4,5]]
    settlement_locations_arr[6] = [[2], [5,14], [5,9]]
    settlement_locations_arr[7] = [[3], [8,17], [10,18]]
    settlement_locations_arr[8] = [[0,3], [0,7,9], [6,10,11]]
    settlement_locations_arr[9] = [[0,3,4], [8,10,19], [11,12,19]]
    settlement_locations_arr[10] = [[0,1,4], [2,9,11], [7,12,13]]
    settlement_locations_arr[11] = [[1,4,5], [10,12,21], [13,14,20]]
    settlement_locations_arr[12] = [[1,2,5], [4,11,13], [8,14,15]]
    settlement_locations_arr[13] = [[2,5,6], [12,14,23], [15,16,21]]
    settlement_locations_arr[14] = [[2,6], [6,13,15], [9,16,17]]
    settlement_locations_arr[15] = [[6], [14,25], [17,22]]
    settlement_locations_arr[16] = [[7], [17,27], [23,33]]
    settlement_locations_arr[17] = [[3,7], [7,16,18], [18,23,24]]
    settlement_locations_arr[18] = [[3,7,8], [17,19,29], [24,25,34]]
    settlement_locations_arr[19] = [[3,4,8], [9,18,20], [19,25,26]]
    settlement_locations_arr[20] = [[4,8,9], [19,21,31], [26,27,35]]
    settlement_locations_arr[21] = [[4,5,9], [11,20,22], [20,27,28]]
    settlement_locations_arr[22] = [[5,9,10], [21,23,33], [28,29,36]]
    settlement_locations_arr[23] = [[5,6,10], [13,22,24], [21,29,30]]
    settlement_locations_arr[24] = [[6,10,11], [23,25,35], [30,31,37]]
    settlement_locations_arr[25] = [[6,11], [15,24,26], [22,31,32]]
    settlement_locations_arr[26] = [[11], [25,37], [32,38]]
    settlement_locations_arr[27] = [[7], [16,28], [33,39]]
    settlement_locations_arr[28] = [[7,12], [27,29,38], [39,40,49]]
    settlement_locations_arr[29] = [[7,8,12], [18,28,30], [34,40,41]]
    settlement_locations_arr[30] = [[8,12,13], [29,31,40], [41,42,50]]
    settlement_locations_arr[31] = [[8,9,13], [20,30,32], [35,42,43]]
    settlement_locations_arr[32] = [[9,13,14], [31,33,42], [43,44,51]]
    settlement_locations_arr[33] = [[9,10,14], [22,32,34], [36,44,45]]
    settlement_locations_arr[34] = [[10,14,15], [33,35,44], [45,46,52]]
    settlement_locations_arr[35] = [[10,11,15], [24,34,36], [37,46,47]]
    settlement_locations_arr[36] = [[11,15], [35,37,46], [47,48,53]]
    settlement_locations_arr[37] = [[11], [26,36], [38,48]]
    settlement_locations_arr[38] = [[12], [28,39], [49,54]]
    settlement_locations_arr[39] = [[12,16], [38,40,47], [54,55,62]]
    settlement_locations_arr[40] = [[12,13,16], [30,39,41], [50,55,56]]
    settlement_locations_arr[41] = [[13,16,17], [40,42,49], [56,57,63]]
    settlement_locations_arr[42] = [[13,14,17], [32,41,43], [51,57,58]]
    settlement_locations_arr[43] = [[14,17,18], [42,44,51], [58,59,64]]
    settlement_locations_arr[44] = [[14,15,18], [34,43,45], [52,59,60]]
    settlement_locations_arr[45] = [[15,18], [44,46,53], [60,61,65]]
    settlement_locations_arr[46] = [[15], [36,45], [53,61]]
    settlement_locations_arr[47] = [[16], [39,48], [62,66]]
    settlement_locations_arr[48] = [[16], [47,49], [66,67]]
    settlement_locations_arr[49] = [[16,17], [41,48,50], [63,67,68]]
    settlement_locations_arr[50] = [[17], [49,51], [68,69]]
    settlement_locations_arr[51] = [[17,18], [43,50,52], [64,69,70]]
    settlement_locations_arr[52] = [[18], [51,53], [70,71]]
    settlement_locations_arr[53] = [[18], [45,52], [65,71]]

#When printing hexes on the board, wd means wood, wl means wool, wt means wheats, oe means ore, bk means brick, 0 means 10, 1 means 11 and 7 means 12
def print_board():
    print("         " + str(settlements_owned_arr[1]) + "     " + str(settlements_owned_arr[3]) + "     " + str(settlements_owned_arr[5]))
    print("       " + road_locations_arr[0] + "   " + road_locations_arr[1] + " " + road_locations_arr[2] + "   " + road_locations_arr[3] + " " + road_locations_arr[4] + "   " + road_locations_arr[5])
    print("      " + str(settlements_owned_arr[0]) + "     " + str(settlements_owned_arr[2]) + "     " + str(settlements_owned_arr[4]) + "     " + str(settlements_owned_arr[6]))
    print("      " + road_locations_arr[6] + " " + get_acronym(0) + " " + road_locations_arr[7] + " " + get_acronym(1) + " " + road_locations_arr[8] + " " + get_acronym(2) + " " + road_locations_arr[9])
    print("      " + str(settlements_owned_arr[8]) + "     " + str(settlements_owned_arr[10]) + "     " + str(settlements_owned_arr[12]) + "     " + str(settlements_owned_arr[14]))
    print("    " + road_locations_arr[10] + "   " + road_locations_arr[11] + " " + road_locations_arr[12] + "   " + road_locations_arr[13] + " " + road_locations_arr[14] + "   " + road_locations_arr[15] + " " + road_locations_arr[16] + "   " + road_locations_arr[17])
    print("   " + str(settlements_owned_arr[7]) + "     " + str(settlements_owned_arr[9]) + "     " + str(settlements_owned_arr[11]) + "     " + str(settlements_owned_arr[13]) + "     " + str(settlements_owned_arr[15]))
    print("   " + road_locations_arr[18] + " " + get_acronym(3) + " " + road_locations_arr[19] + " " + get_acronym(4) + " " + road_locations_arr[20] + " " + get_acronym(5) + " " + road_locations_arr[21] + " " + get_acronym(6) + " " + road_locations_arr[22])
    print("   " + str(settlements_owned_arr[17]) + "     " + str(settlements_owned_arr[19]) + "     " + str(settlements_owned_arr[21]) + "     " + str(settlements_owned_arr[23]) + "     " + str(settlements_owned_arr[25]))
    print(" " + road_locations_arr[23] + "   " + road_locations_arr[24] + " " + road_locations_arr[25] + "   " + road_locations_arr[26] + " " + road_locations_arr[27] + "   " + road_locations_arr[28] + " " + road_locations_arr[29] + "   " + road_locations_arr[30] + " " + road_locations_arr[31] + "   " + road_locations_arr[32])
    print(str(settlements_owned_arr[16]) + "     " + str(settlements_owned_arr[18]) + "     " + str(settlements_owned_arr[20]) + "     " + str(settlements_owned_arr[22]) + "     " + str(settlements_owned_arr[24]) + "     " + str(settlements_owned_arr[26]))
    print(road_locations_arr[33] + " " + get_acronym(7) + " " + road_locations_arr[34] + " " + get_acronym(8) + " " + road_locations_arr[35] + " " + get_acronym(9) + " " + road_locations_arr[36] + " " + get_acronym(10) + " " + road_locations_arr[37] + " " + get_acronym(11) + " " + road_locations_arr[38])
    print(str(settlements_owned_arr[27]) + "     " + str(settlements_owned_arr[29]) + "     " + str(settlements_owned_arr[31]) + "     " + str(settlements_owned_arr[33]) + "     " + str(settlements_owned_arr[35]) + "     " + str(settlements_owned_arr[37]))
    print(" " + road_locations_arr[39] + "   " + road_locations_arr[40] + " " + road_locations_arr[41] + "   " + road_locations_arr[42] + " " + road_locations_arr[43] + "   " + road_locations_arr[44] + " " + road_locations_arr[45] + "   " + road_locations_arr[46] + " " + road_locations_arr[47] + "   " + road_locations_arr[48])
    print("   " + str(settlements_owned_arr[28]) + "     " + str(settlements_owned_arr[30]) + "     " + str(settlements_owned_arr[32]) + "     " + str(settlements_owned_arr[34]) + "     " + str(settlements_owned_arr[36]))
    print("   " + road_locations_arr[49] + " " + get_acronym(12) + " " + road_locations_arr[50] + " " + get_acronym(13) + " " + road_locations_arr[51] + " " + get_acronym(14) + " " + road_locations_arr[52] + " " + get_acronym(15) + " " + road_locations_arr[53])
    print("   " + str(settlements_owned_arr[38]) + "     " + str(settlements_owned_arr[40]) + "     " + str(settlements_owned_arr[42]) + "     " + str(settlements_owned_arr[44]) + "     " + str(settlements_owned_arr[46]))
    print("    " + road_locations_arr[54] + "   " + road_locations_arr[55] + " " + road_locations_arr[56] + "   " + road_locations_arr[57] + " " + road_locations_arr[58] + "   " + road_locations_arr[59] + " " + road_locations_arr[60] + "   " + road_locations_arr[61])
    print("      " + str(settlements_owned_arr[39]) + "     " + str(settlements_owned_arr[41]) + "     " + str(settlements_owned_arr[43]) + "     " + str(settlements_owned_arr[45]))
    print("      " + road_locations_arr[62] + " " + get_acronym(16) + " " + road_locations_arr[63] + " " + get_acronym(17) + " " + road_locations_arr[64] + " " + get_acronym(18) + " " + road_locations_arr[65])
    print("      " + str(settlements_owned_arr[47]) + "     " + str(settlements_owned_arr[49]) + "     " + str(settlements_owned_arr[51]) + "     " + str(settlements_owned_arr[53]))
    print("       " + road_locations_arr[66] + "   " + road_locations_arr[67] + " " + road_locations_arr[68] + "   " + road_locations_arr[69] + " " + road_locations_arr[70] + "   " + road_locations_arr[71])
    print("         " + str(settlements_owned_arr[48]) + "     " + str(settlements_owned_arr[50]) + "     " + str(settlements_owned_arr[52]))

def get_acronym(hex_number):
    if hex_tiles_arr[hex_number][0] == "dessert":
        acronym = "des"
    else:
        tuple = hex_tiles_arr[hex_number]
        letter1 = tuple[0][0]
        word_length = len(tuple[0]) - 1
        letter2 = tuple[0][word_length]
        letter3 = str(tuple[1])
        if(letter3 == "10"):
            letter3 = "0"
        if(letter3 == "11"):
            letter3 = "1"
        if(letter3 == "12"):
            letter3 = "7"
        acronym = letter1 + letter2 + letter3
    return acronym

def print_hand():
    print(resource_cards)
    print(dev_cards)

def place_settlement(settle1):
    if settlements_owned_arr[settle1] == 0:
        settlements_owned_arr[settle1] = 1
        for i in settlement_locations_arr[settle1][1]:
            settlements_owned_arr[i] = 9

def place_initial_settlements():
    settle1 = int(input("Place first settlement (enter number from 0-53)"))
    while(settle1 < 0 or settle1 > 53):
        print("That number was not a valid settlement location")
        settle1 = int(input("Place first settlement (enter number from 0-53)"))
    place_settlement(settle1)
    possible_roads = settlement_locations_arr[settle1][2]
    road1 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    while(road1 not in possible_roads):
        print("That was not a valid road location")
        road1 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    road_locations_arr[road1] = "X"
    print_board()
    settle2 = int(input("Place second settlement (enter number from 0-53)"))
    valid_settlement = False
    if (settle2 >= 0 and settle2 <= 53):
        if (settlements_owned_arr[settle2] == 0):
            valid_settlement = True
    while (valid_settlement == False):
        print("That number was not a valid settlement location")
        settle2 = int(input("Place second settlement (enter number from 0-53)"))
        if(settle2 >= 0 and settle2 <= 53):
            if(settlements_owned_arr[settle2] == 0):
                valid_settlement = True
            else: print("That settlement is too close to an existing settlement")
    place_settlement(settle2)
    possible_roads = settlement_locations_arr[settle2][2]
    road2 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    while (road2 not in possible_roads):
        print("That was not a valid road location")
        road2 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    road_locations_arr[road2] = "X"
    for i in settlement_locations_arr[settle2][0]:
        if(hex_tiles_arr[i][0] != "dessert"):
            resource_cards[hex_tiles_arr[i][0]] += 1
    print_board()
    print_hand()

def roll_dice():
    global turns_taken
    turns_taken += 1
    print("Turn: " + str(turns_taken))
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    sum = die1 + die2
    print("Rolled a " + str(die1) + " and a " + str(die2) + " for a sum of " + str(sum))
    return sum

def get_resources():
    sum = roll_dice()
    if sum == 7:
        print("rolled a 7")
    else:
        for settlement in range(len(settlements_owned_arr)): #loop through every possible settlement
            if int(settlements_owned_arr[settlement]) == 1 or int(settlements_owned_arr[settlement]) == 2: #only consider settlements and cities
                neighboringhexes = settlement_locations_arr[settlement][0] #get neighboring hexes
                for hex in neighboringhexes:
                    if int(hex_tiles_arr[hex][1]) == sum: #check if hexes match die roll
                        resource_cards[hex_tiles_arr[hex][0]] += int(settlements_owned_arr[settlement])
                        print("Added " + str(settlements_owned_arr[settlement]) + " " + hex_tiles_arr[hex][0] + " to hand.")

def ask_to_play_dev_cards():
    total_cards = 0
    for card in dev_cards:
        if card != "vp":
            total_cards += dev_cards[card]
    if(total_cards > 0):
        play_card = input("Do you want to play a development card? (type 'yes' to play card)")
        if 'yes' in play_card:
            num = 1
            for card in dev_cards:
                if card != "vp":
                    if dev_cards[card] > 0:
                        print("Type '" + str(num) + "' to play " + str(card))
                        num += 1
            card_played = input("Or type anything else to cancel")
            if int(card_played) > 0 and int(card_played) < num:
                for card in dev_cards:
                    if card != "vp":
                        if dev_cards[card] > 0:
                            if num == 1:
                                card_played = card
                                return card
                            else:
                                num = num - 1
    return None

def play_card(card_type):
    print("Playing " + card_type)
    dev_cards[card_type] -= 1

def ask_to_buy():
    possible_buys = []
    road_resource_cards = {
        "wood": 1,
        "wheat": 0,
        "wool": 0,
        "ore": 0,
        "brick": 1
    }
    settlement_resource_cards = {
        "wood": 1,
        "wheat": 1,
        "wool": 1,
        "ore": 0,
        "brick": 1
    }
    city_resource_cards = {
        "wood": 0,
        "wheat": 2,
        "wool": 0,
        "ore": 3,
        "brick": 0
    }
    dev_resource_cards = {
        "wood": 0,
        "wheat": 1,
        "wool": 1,
        "ore": 1,
        "brick": 0
    }
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < road_resource_cards[resource]:
            can_buy = False
    if can_buy == True:
        possible_buys.append("road")
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < settlement_resource_cards[resource]:
            can_buy = False
    if can_buy == True:
        possible_buys.append("settlement")
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < city_resource_cards[resource]:
            can_buy = False
    if can_buy == True:
        possible_buys.append("city")
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < dev_resource_cards[resource]:
            can_buy = False
    if can_buy == True:
        possible_buys.append("development card")
    num = 1
    for resources in possible_buys:
        print("Type " + str(num) + " to buy " + resources)
        num += 1
    if num != 1:
        buy = input("Or type anything else to not buy anything")
        if int(buy) > 0 and int(buy) < num:
            bought = possible_buys[int(buy)-1]
            print("You bought a " + bought)
            return bought
    return None

def determine_longest_continuous_road():
    max_road_length = 1
    curr_roads = []
    curr_strip = []
    for road in range(len(road_locations_arr)):
        if road_locations_arr[road] == 'X':
            curr_roads.append(road)
    for road in curr_roads: #try every starting point
        curr_strip = [road]
        reset = False
        cant_use = []
        while reset == False:
            added_road = False
            for i in range(len(settlement_locations_arr)):
                if curr_strip[len(curr_strip)-1] in settlement_locations_arr[i][2]:
                    for next_road in settlement_locations_arr[i][2]:
                        if next_road in curr_roads and next_road not in curr_strip and next_road not in cant_use:
                            curr_strip.append(next_road)
                            if len(curr_strip) > max_road_length:
                                max_road_length = len(curr_strip)
                                added_road = True
            if added_road == False:
                cant_use.append(curr_strip[len(curr_strip)-1])
                curr_strip.pop()
                if len(curr_strip) < 1:
                    reset = True
    return max_road_length


def get_possible_road_placements(): #Assuming initial roads are already placed
    curr_roads = []
    for road in range(len(road_locations_arr)):
        if road_locations_arr[road] == 'X':
            curr_roads.append(road)
    buildable_roads = []
    for road in curr_roads:
        for i in range(len(settlement_locations_arr)):
            if road in settlement_locations_arr[i][2]:
                for x in settlement_locations_arr[i][2]:
                    buildable_roads.append(x)
    buildable_roads2 = []
    for road in buildable_roads:
        if road not in curr_roads and road not in buildable_roads2:
            buildable_roads2.append(road)
    return buildable_roads2

def get_possible_settlement_locations():
    possible_settlements = []
    possible_settlements2 = []
    for settlement in range(len(settlements_owned_arr)):
        if settlements_owned_arr[settlement] == 0:
            possible_settlements.append(settlement)
    for settlement in possible_settlements:
        connecting_roads = settlement_locations_arr[settlement][2]
        for road in connecting_roads:
            if road_locations_arr[road] == "X":
                possible_settlements2.append(settlement)
    return possible_settlements2

def get_possible_city_locations():
    possible_cities = []
    for settlement in range(len(settlements_owned_arr)):
        if settlements_owned_arr[settlement] == 1:
            possible_cities.append(settlement)
    return possible_cities

def buy_road():
    possible_roads = get_possible_road_placements()
    road1 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    while (road1 not in possible_roads):
        print("That was not a valid road location")
        road1 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    road_locations_arr[road1] = "X"
    resource_cards["wood"] -= 1
    resource_cards["brick"] -= 1

def buy_settlement():
    possible_settlement_locations = get_possible_settlement_locations()
    settlement = int(input("Place a settlement (enter one of the following numbers: " + str(possible_settlement_locations) + ")"))
    while (settlement not in possible_settlement_locations):
        print("That was not a valid settlement location")
        settlement = int(input("Place a settlement (enter one of the following numbers: " + str(possible_settlement_locations) + ")"))
    settlements_owned_arr[settlement] = 1
    resource_cards["wood"] -= 1
    resource_cards["brick"] -= 1
    resource_cards["wool"] -= 1
    resource_cards["wheat"] -= 1

def buy_city():
    possible_city = get_possible_city_locations()
    city = int(input("Place a city (enter one of the following numbers: " + str(possible_city) + ")"))
    while (city not in possible_city):
        print("That was not a valid city location")
        city = int(input("Place a city (enter one of the following numbers: " + str(possible_city) + ")"))
    settlements_owned_arr[city] = 2
    resource_cards["ore"] -= 3
    resource_cards["wheat"] -= 2

def buy_dev_card():
    drawn_card = dev_deck.pop()
    resource_cards["ore"] -= 1
    resource_cards["wool"] -= 1
    resource_cards["wheat"] -= 1
    dev_cards[drawn_card] += 1

def play_game_manually():
    generate_board()
    print_board()
    place_initial_settlements()
    game_won = False
    while game_won == False:
        get_resources()
        print_hand()
        d_card = ask_to_play_dev_cards()
        if d_card != None:
            play_card(d_card)
        bought = ask_to_buy()
        while bought != None:
            if bought == "road":
                buy_road()
            if bought == "settlement":
                buy_settlement()
            if bought == "city":
                buy_city()
            if bought == "development card":
                buy_dev_card()
            bought = ask_to_buy()


play_game_manually()
