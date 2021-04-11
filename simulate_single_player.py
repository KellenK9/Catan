#Simulate a single player playing Catan
#Optimize to reduce the number of turns it takes to get 10 VP's
import random
#import numpy.random


def generate_board():
    global gamestate
    global game_won
    game_won = False
    global total_cities
    total_cities = 0
    global total_settlements
    total_settlements = 0
    global total_roads
    total_roads = 0
    global longest_road_length
    longest_road_length = 0
    global has_longest_road
    has_longest_road = False
    global has_largest_army
    has_largest_army = False

    global max_settlements
    max_settlements = 5
    global max_cities
    max_cities = 4
    global max_roads
    max_roads = 15

    global knights_played
    knights_played = 0

    global turns_taken
    turns_taken = 0

    global victory_points
    victory_points = 2

    global robber_location

    global dev_deck
    global resource_cards
    global dev_cards
    global hex_tiles_arr
    global settlement_locations_arr
    global road_locations_arr
    global settlements_owned_arr
    global port_locations_arr

    global road_resource_cards
    global settlement_resource_cards
    global city_resource_cards
    global dev_resource_cards
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

    #settlement location: port type
    port_locations_arr = {
        0: "3to1",
        1: "3to1",
        3: "wheat",
        4: "wheat",
        7: "wood",
        14: "ore",
        15: "ore",
        17: "wood",
        26: "3to1",
        28: "brick",
        37: "3to1",
        38: "brick",
        45: "wool",
        46: "wool",
        47: "3to1",
        48: "3to1",
        50: "3to1",
        51: "3to1"
    }

    dev_deck = ["road_building", "road_building", "year_of_plenty", "year_of_plenty", "vp", "vp", "vp", "vp", "vp", #"monopoly", "monopoly",
                "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight", "knight"]
    random.shuffle(dev_deck)

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
    resource_cards = {
        "wood": 0,
        "wheat": 0,
        "wool": 0,
        "ore": 0,
        "brick": 0
    }

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
    hex_tiles_arr = [] #[[wood, 3], [ore, 11], etc...]
    settlement_locations_arr = []  # vertices
    road_locations_arr = [] #edges
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
                if(x == 0):
                    robber_location = len(hex_tiles_arr)
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

    gamestate = [turns_taken,
                 victory_points,
                 total_cities,
                 total_settlements,
                 total_roads,
                 longest_road_length,
                 has_longest_road,
                 has_largest_army,
                 dev_deck,
                 resource_cards,
                 dev_cards,
                 hex_tiles_arr,
                 road_locations_arr,
                 settlement_locations_arr,
                 settlements_owned_arr,
                 road_resource_cards,
                 settlement_resource_cards,
                 city_resource_cards,
                 dev_resource_cards,
                 max_settlements,
                 max_cities,
                 max_roads,
                 knights_played,
                 port_locations_arr
                 ]

def update_gamestate(ai):
    global game_won #
    global total_cities #
    global total_settlements #
    global total_roads #
    global victory_points
    global turns_taken #
    global longest_road_length #
    global has_longest_road #
    global has_largest_army #
    global knights_played #
    global settlements_owned_arr #
    global road_locations_arr #
    global dev_cards #
    global simming
    turns_taken += 1
    longest_road_length = determine_longest_continuous_road()
    if(longest_road_length > 4):
        has_longest_road = True
    if(knights_played > 2):
        has_largest_army = True
    temp_total_roads = 0
    temp_total_settlements = 0
    temp_total_cities = 0
    for i in road_locations_arr:
        if i == "X":
            temp_total_roads += 1
    total_roads = temp_total_roads
    for j in settlements_owned_arr:
        if j == 1:
            temp_total_settlements += 1
        if j == 2:
            temp_total_cities += 1
    total_settlements = temp_total_settlements
    total_cities = temp_total_cities
    victory_points = (2*total_cities) + total_settlements + dev_cards["vp"]
    if has_largest_army:
        victory_points += 2
    if has_longest_road:
        victory_points += 2
    if(victory_points > 9):
        print("Congratulations! You won with " + str(victory_points) + " victory points")
        game_won = True
    if(simming):
        ai = update_ai(ai)

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
    global settlements_owned_arr
    if settlements_owned_arr[settle1] == 0:
        settlements_owned_arr[settle1] = 1
        for i in settlement_locations_arr[settle1][1]:
            settlements_owned_arr[i] = 9

def place_initial_settlements():
    global total_settlements
    global total_roads
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
    total_settlements = 2
    total_roads = 2
    print_board()
    print_hand()

def sim_place_initial_settlements(ai):
    global total_settlements
    global total_roads
    global resource_cards
    #Place first settlement
    best_spot = [0, 0] #Where the best spot is, value of best spot
    for spot in ai["best_vertices"]:
        if ai["best_vertices"][spot] >= best_spot[1]:
            best_spot[0] = spot
            best_spot[1] = ai["best_vertices"][spot]
    place_settlement(best_spot[0])
    ai = update_ai(ai)
    #Place first road
    possible_roads = settlement_locations_arr[best_spot[0]][2]
    best_edge = [0, 0]
    for road_spot in ai["best_edges"]:
        if road_spot in possible_roads:
            if ai["best_edges"][road_spot] >= best_edge[1]:
                best_edge[0] = road_spot
                best_edge[1] = ai["best_edges"][road_spot]
    road_locations_arr[best_edge[0]] = "X"
    ai = update_ai(ai)
    #Place second settlement
    best_spot = [0, 0]
    for spot in ai["best_vertices"]:
        if ai["best_vertices"][spot] >= best_spot[1] and settlements_owned_arr[spot] == 0:
            best_spot[0] = spot
            best_spot[1] = ai["best_vertices"][spot]
    place_settlement(best_spot[0])
    ai = update_ai(ai)
    #Place second road
    possible_roads = settlement_locations_arr[best_spot[0]][2]
    best_edge = [0, 0]
    for road_spot in ai["best_edges"]:
        if road_spot in possible_roads:
            if ai["best_edges"][road_spot] >= best_edge[1]:
                best_edge[0] = road_spot
                best_edge[1] = ai["best_edges"][road_spot]
    road_locations_arr[best_edge[0]] = "X"
    for i in settlement_locations_arr[best_spot[0]][0]:
        if (hex_tiles_arr[i][0] != "dessert"):
            resource_cards[hex_tiles_arr[i][0]] += 1
    total_settlements = 2
    total_roads = 2
    ai = update_ai(ai)

def roll_dice():
    global victory_points
    print("Turn: " + str(turns_taken) + "          Victory Points: " + str(victory_points))
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    sum = die1 + die2
    print("Rolled a " + str(die1) + " and a " + str(die2) + " for a sum of " + str(sum))
    return sum

def get_resources(ai):
    global robber_location
    global simming
    sum = roll_dice()
    if sum == 7:
        if(simming == False):
            rolled_seven()
        else:
            sim_rolled_seven(ai)
    else:
        for settlement in range(len(settlements_owned_arr)): #loop through every possible settlement
            if int(settlements_owned_arr[settlement]) == 1 or int(settlements_owned_arr[settlement]) == 2: #only consider settlements and cities
                neighboringhexes = settlement_locations_arr[settlement][0] #get neighboring hexes
                for hex in neighboringhexes:
                    if(hex_tiles_arr[hex][0] != "dessert"):
                        if int(hex_tiles_arr[hex][1]) == sum: #check if hexes match die roll
                            if(robber_location == hex):
                                print("You got jipped out of resources by the robber!")
                            else:
                                resource_cards[hex_tiles_arr[hex][0]] += int(settlements_owned_arr[settlement])
                                print("Added " + str(settlements_owned_arr[settlement]) + " " + hex_tiles_arr[hex][0] + " to hand.")

def rolled_seven():
    global resource_cards
    hand_size = 0
    for i in resource_cards:
        hand_size += resource_cards[i]
    if(hand_size > 7):
        print("A 7 was rolled while your hand was too large. Now you must discard cards.")
        if(hand_size % 2 == 1):
            discard_cards((hand_size-1)/2)
        else:
            discard_cards(hand_size/2)
    move_robber()

def sim_rolled_seven(ai):
    global resource_cards
    hand_size = 0
    for i in resource_cards:
        hand_size += resource_cards[i]
    if(hand_size > 7):
        print("A 7 was rolled while your hand was too large. Now you must discard cards.")
        if(hand_size % 2 == 1):
            for i in range(int((hand_size-1)/2)):
                sim_discard_any_card(ai)
        else:
            for i in range(int(hand_size/2)):
                sim_discard_any_card(ai)
    sim_move_robber(ai)

def move_robber():
    global robber_location
    print("The robber is currently on hex #" + str(robber_location))
    valid_num_chosen = False
    while(valid_num_chosen == False):
        new_robber_hex = input("What hex would you like to move the robber to? (Enter a number from 0-18)")
        if not new_robber_hex.isnumeric():
            print("That was not a valid integer :(")
        elif(int(new_robber_hex) > 18 or int(new_robber_hex) < 0):
            print("That was not a valid integer :(")
        elif(int(new_robber_hex) == robber_location):
            print("The robber was already on that hex. Choose a new hex")
        else:
            valid_num_chosen = True
    robber_location = int(new_robber_hex)
    #Can't steal from anyone when moving robber so instead:
    ask_to_add_any_card()

def sim_move_robber(ai):
    global robber_location
    best_robber = [0, 0] #[hex number, score]
    for hex in ai["best_robber_hexes"]:
        if hex != robber_location:
            if ai["best_robber_hexes"][hex] >= best_robber[1]:
                best_robber[0] = hex
                best_robber[1] = ai["best_robber_hexes"][hex]
    robber_location = best_robber[0]
    # Can't steal from anyone when moving robber so instead: add any card
    sim_add_any_card(ai)

def discard_cards(n):
    while(n > 0):
        ask_to_dicard_card()
        n -= 1

def ask_to_dicard_card():
    global resource_cards
    print_hand()
    card_discarded = False
    while(card_discarded == False):
        card = input("What card would you like to discard? (Type 1 for wood, 2 for wheat, 3 for wool, 4 for ore, and 5 for brick)")
        if not card.isnumeric():
            print("That was not a valid integer :(")
        else:
            if (int(card) == 1):
                if(resource_cards["wood"] > 0):
                    resource_cards["wood"] -= 1
                    card_discarded = True
                else:
                    print("You have no wood to discard")
            elif (int(card) == 2):
                if (resource_cards["wheat"] > 0):
                    resource_cards["wheat"] -= 1
                    card_discarded = True
                else:
                    print("You have no wheat to discard")
            elif (int(card) == 3):
                if (resource_cards["wool"] > 0):
                    resource_cards["wool"] -= 1
                    card_discarded = True
                else:
                    print("You have no wool to discard")
            elif (int(card) == 4):
                if (resource_cards["ore"] > 0):
                    resource_cards["ore"] -= 1
                    card_discarded = True
                else:
                    print("You have no ore to discard")
            elif (int(card) == 5):
                if (resource_cards["brick"] > 0):
                    resource_cards["brick"] -= 1
                    card_discarded = True
                else:
                    print("You have no brick to discard")

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
            if not card_played.isnumeric():
                return None
            if int(card_played) > 0 and int(card_played) < num:
                for card in dev_cards:
                    if card != "vp":
                        if dev_cards[card] > 0:
                            if num == 2:
                                return card
                            else:
                                num = num - 1
    return None

def determine_if_ai_plays_dev_cards(ai):
    total_cards = 0
    for card in dev_cards:
        if card != "vp":
            total_cards += dev_cards[card]
    if (total_cards > 0):
        cards_to_play = []
        for card in dev_cards:
            if card != "vp":
                if dev_cards[card] > 0:
                    cards_to_play.append(card)
        card_played = ""
        card_played_values = [0, 0, 0]
        for card in cards_to_play:
            if(card == "knight"):
                card_played_values[0] = ai["propensity_to_play_knight"]
            if (card == "year_of_plenty"):
                card_played_values[1] = ai["propensity_to_play_year_of_plenty"]
            if (card == "road_building"):
                card_played_values[2] = ai["propensity_to_play_road_building"]
        if(card_played_values[0] == card_played_values[1] and card_played_values[0] == card_played_values[2] and card_played_values[0] == 0):
            return None
        if(card_played_values[0] >= card_played_values[1]):
            if(card_played_values[0] >= card_played_values[2]):
                card_played = "knight"
            else:
                card_played = "road_building"

        else:
            if(card_played_values[1] >= card_played_values[2]):
                card_played = "year_of_plenty"
            else:
                card_played = "road_building"
        return card_played
    return None

def play_card(card_type):
    global knights_played
    global dev_cards
    global resource_cards
    print("Playing " + card_type)
    dev_cards[card_type] -= 1
    if card_type == "knight":
        knights_played += 1
        move_robber()
    elif card_type == "year_of_plenty":
        ask_to_add_any_card()
        ask_to_add_any_card()
    elif card_type == "road_building":
        resource_cards["wood"] += 2
        resource_cards["brick"] += 2
        buy_road()
        buy_road()

def sim_play_card(card_type, ai):
    global knights_played
    global dev_cards
    global resource_cards
    print("Playing " + card_type)
    dev_cards[card_type] -= 1
    if card_type == "knight":
        knights_played += 1
        sim_move_robber(ai)
    elif card_type == "year_of_plenty":
        sim_add_any_card(ai)
        sim_add_any_card(ai)
    elif card_type == "road_building":
        resource_cards["wood"] += 2
        resource_cards["brick"] += 2
        sim_buy_road(ai)
        sim_buy_road(ai)

def ask_to_add_any_card():
    global resource_cards
    added_card = False
    while(added_card == False):
        new_resource = input("What resource would you like? (Type 1 for wood, 2 for wheat, 3 for wool, 4 for ore, and 5 for brick)")
        if not new_resource.isnumeric():
            print("That was not a valid number")
        elif(int(new_resource) < 1 or int(new_resource) > 5):
            print("That number was not between 1 and 5")
        else:
            if (int(new_resource) == 1):
                resource_cards["wood"] += 1
                added_card = True
            elif (int(new_resource) == 2):
                resource_cards["wheat"] += 1
                added_card = True
            elif (int(new_resource) == 3):
                resource_cards["wool"] += 1
                added_card = True
            elif (int(new_resource) == 4):
                resource_cards["ore"] += 1
                added_card = True
            elif (int(new_resource) == 5):
                resource_cards["brick"] += 1
                added_card = True

def sim_add_any_card(ai):
    global resource_cards
    card_to_add = ["wood", 0] #card name, value of card
    for card in ai["value_of_resources"]:
        if(ai["value_of_resources"][card] >= card_to_add[1]):
            card_to_add[0] = card
            card_to_add[1] = ai["value_of_resources"][card]
    resource_cards[card_to_add[0]] += 1

def sim_discard_any_card(ai):
    global resource_cards
    possible_resources = []
    for resource in resource_cards:
        if resource_cards[resource] > 0:
            possible_resources.append(resource)
    if len(possible_resources) != 0:
        resource_to_discard = ["wood", 9999999] #card name, value of card
        for card in ai["value_of_resources"]:
            if(ai["value_of_resources"][card] <= resource_to_discard[1] and card in possible_resources):
                resource_to_discard[0] = card
                resource_to_discard[1] = ai["value_of_resources"][card]
        resource_cards[resource_to_discard[0]] -= 1

def ask_to_buy():
    possible_buys = []
    global road_resource_cards
    global settlement_resource_cards
    global city_resource_cards
    global dev_resource_cards
    global total_settlements
    global settlements_owned_arr
    global road_locations_arr
    global settlement_locations_arr

    #Determine if you can buy roads
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < road_resource_cards[resource]:
            can_buy = False
    if can_buy == True:
        possible_buys.append("road")
    #determine if you can buy settlements
    can_buy = False
    for vertex in range(len(settlement_locations_arr)):
        if settlements_owned_arr[vertex] == 0:
            roads = settlement_locations_arr[vertex][2]
            for road in roads:
                if road_locations_arr[road] == "X":
                    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < settlement_resource_cards[resource]:
            can_buy = False
    if can_buy == True:
        possible_buys.append("settlement")
    #determine if you can buy cities
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < city_resource_cards[resource]:
            can_buy = False
    if(total_settlements == 0):
        can_buy = False
    if can_buy == True:
        possible_buys.append("city")
    #determine if you can buy dev cards
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
        if not buy.isnumeric():
            return None
        if int(buy) > 0 and int(buy) < num:
            bought = possible_buys[int(buy)-1]
            print("You bought a " + bought)
            return bought
    return None

def sim_ask_to_buy(ai):
    possible_buys = []
    global road_resource_cards
    global settlement_resource_cards
    global city_resource_cards
    global dev_resource_cards
    global total_settlements
    global total_roads
    global total_cities
    global max_roads
    global max_cities
    global max_settlements
    global settlements_owned_arr
    global road_locations_arr
    global settlement_locations_arr
    global dev_deck

    # Determine if you can buy roads
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < road_resource_cards[resource]:
            can_buy = False
    if(total_roads >= max_roads):
        can_buy = False
    if can_buy == True:
        possible_buys.append("road")
    # determine if you can buy settlements
    can_buy = False
    for vertex in range(len(settlement_locations_arr)):
        if settlements_owned_arr[vertex] == 0:
            roads = settlement_locations_arr[vertex][2]
            for road in roads:
                if road_locations_arr[road] == "X":
                    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < settlement_resource_cards[resource]:
            can_buy = False
    if(total_settlements >= max_settlements):
        can_buy = False
    if can_buy == True:
        possible_buys.append("settlement")
    # determine if you can buy cities
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < city_resource_cards[resource]:
            can_buy = False
    if (total_settlements == 0):
        can_buy = False
    if(total_cities >= max_cities):
        can_buy = False
    if can_buy == True:
        possible_buys.append("city")
    # determine if you can buy dev cards
    can_buy = True
    for resource in resource_cards:
        if resource_cards[resource] < dev_resource_cards[resource]:
            can_buy = False
    if can_buy == True:
        if(len(dev_deck) > 0):
            possible_buys.append("development card")

    bought = [road, 0] #What to buy, propensity to buy it
    for i in possible_buys:
        if i == "road":
            if ai["value_of_goals"]["road"] > bought[1]:
                bought[0] = i
                bought[1] = ai["value_of_goals"]["road"]
        if i == "city":
            if ai["value_of_goals"]["city"] > bought[1]:
                bought[0] = i
                bought[1] = ai["value_of_goals"]["city"]
        if i == "settlement":
            if ai["value_of_goals"]["settlement"] > bought[1]:
                bought[0] = i
                bought[1] = ai["value_of_goals"]["settlement"]
        if i == "development card":
            if ai["value_of_goals"]["dev"] > bought[1]:
                bought[0] = i
                bought[1] = ai["value_of_goals"]["dev"]
    if(bought[1] > 0):
        return bought[0]
    else:
        return None

def ask_to_port_trade():
    global port_locations_arr
    global settlements_owned_arr
    global resource_cards
    possible_trade_ins = []
    has_3to1 = False
    resource_ports = []
    for port in port_locations_arr:
        if settlements_owned_arr[port] == 1 or settlements_owned_arr[port] == 2:
            if port_locations_arr[port] == "3to1":
                has_3to1 = True
            else:
                resource_ports.append(port_locations_arr[port])
    for type in resource_cards:
        if resource_cards[type] >= 2:
            if(type in resource_ports):
                possible_trade_ins.append([2, type])
            elif(has_3to1 and resource_cards[type] >= 3):
                possible_trade_ins.append([3, type])
            elif(resource_cards[type] >= 4):
                possible_trade_ins.append([4, type])

    num = 1
    for resources in possible_trade_ins:
        print("Type " + str(num) + " to trade in " + str(resources[0]) + " " + str(resources[1]) + " for 1 of any resource")
        num += 1
    if num != 1:
        buy = input("Or type anything else to not buy anything")
        if not buy.isnumeric():
            return None
        if int(buy) > 0 and int(buy) < num:
            bought = possible_trade_ins[int(buy) - 1]
            print("You traded in " + str(bought[0]) + " " + str(bought[1]))
            new_resource = input("What resource would you like? (Type 1 for wood, 2 for wheat, 3 for wool, 4 for ore, and 5 for brick)")
            if not new_resource.isnumeric():
                return None
            resource_cards[bought[1]] -= bought[0]
            if(int(new_resource) == 1):
                resource_cards["wood"] += 1
            elif(int(new_resource) == 2):
                resource_cards["wheat"] += 1
            elif(int(new_resource) == 3):
                resource_cards["wool"] += 1
            elif(int(new_resource) == 4):
                resource_cards["ore"] += 1
            elif(int(new_resource) == 5):
                resource_cards["brick"] += 1
            return [bought, new_resource]
    return None

def sim_ask_to_port_trade(ai):
    global port_locations_arr
    global settlements_owned_arr
    global resource_cards
    resource_list = ["wood", "wheat", "wool", "ore", "brick"]
    possible_trade_ins = []
    has_3to1 = False
    resource_ports = []
    for port in port_locations_arr:
        if settlements_owned_arr[port] == 1 or settlements_owned_arr[port] == 2:
            if port_locations_arr[port] == "3to1":
                has_3to1 = True
            else:
                resource_ports.append(port_locations_arr[port])
    for type in resource_cards:
        if resource_cards[type] >= 2:
            if (type in resource_ports):
                possible_trade_ins.append([2, type])
            elif (has_3to1 and resource_cards[type] >= 3):
                possible_trade_ins.append([3, type])
            elif (resource_cards[type] >= 4):
                possible_trade_ins.append([4, type])
    port_trade = []
    for trade in possible_trade_ins:
        for resource_wanted in resource_list:
            trade_value = (ai["propensity_to_trade"]*ai["value_of_resources"][trade[1]])/(trade[0]*ai["value_of_resources"][resource_wanted])
            if(1 < trade_value and resource_cards[trade[1]] > trade[0]):
                trade_option = [trade_value, resource_wanted, trade[1], trade[0]]
                port_trade.append(trade_option)
    max_value = 0
    curr_trade_in = []
    for trade_ins in port_trade:
        if max_value < trade_ins[0]:
            max_value = trade_ins[0]
            curr_trade_in = trade_ins
    return curr_trade_in

def sim_port_trade(port_trade):
    global resource_cards
    resource_cards[port_trade[1]] += 1
    resource_cards[port_trade[2]] -= port_trade[3]

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
    global total_roads
    global max_roads
    if(total_roads >= max_roads):
        return []
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
    global total_settlements
    global max_settlements
    possible_settlements = []
    possible_settlements2 = []
    if(total_settlements >= max_settlements):
        return []
    for settlement in range(len(settlements_owned_arr)):
        if settlements_owned_arr[settlement] == 0:
            if(settlement not in possible_settlements):
                possible_settlements.append(settlement)
    for settlement in possible_settlements:
        connecting_roads = settlement_locations_arr[settlement][2]
        for road in connecting_roads:
            if road_locations_arr[road] == "X":
                if(settlement not in possible_settlements2):
                    possible_settlements2.append(settlement)
    return possible_settlements2

def get_possible_city_locations():
    global max_cities
    global total_cities
    if(total_cities >= max_cities):
        return []
    possible_cities = []
    for settlement in range(len(settlements_owned_arr)):
        if settlements_owned_arr[settlement] == 1:
            possible_cities.append(settlement)
    return possible_cities

def buy_road():
    global total_roads
    global road_locations_arr
    global resource_cards
    possible_roads = get_possible_road_placements()
    road1 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    while (road1 not in possible_roads):
        print("That was not a valid road location")
        road1 = int(input("Place a road (enter one of the following numbers: " + str(possible_roads) + ")"))
    road_locations_arr[road1] = "X"
    total_roads += 1
    resource_cards["wood"] -= 1
    resource_cards["brick"] -= 1

def sim_buy_road(ai):
    global total_roads
    global road_locations_arr
    global resource_cards
    possible_roads = get_possible_road_placements()
    road1 = [0, 0] #[road number, value of road]
    for road in possible_roads:
        if(ai["best_edges"][road] >= road1[1]):
            road1[0] = road
            road1[1] = ai["best_edges"][road]
    road_locations_arr[road1[0]] = "X"
    total_roads += 1
    resource_cards["wood"] -= 1
    resource_cards["brick"] -= 1

def buy_settlement():
    global total_settlements
    global resource_cards
    global settlements_owned_arr
    possible_settlement_locations = get_possible_settlement_locations()
    settlement = int(input("Place a settlement (enter one of the following numbers: " + str(possible_settlement_locations) + ")"))
    while (settlement not in possible_settlement_locations):
        print("That was not a valid settlement location")
        settlement = int(input("Place a settlement (enter one of the following numbers: " + str(possible_settlement_locations) + ")"))
    place_settlement(settlement)
    total_settlements += 1
    resource_cards["wood"] -= 1
    resource_cards["brick"] -= 1
    resource_cards["wool"] -= 1
    resource_cards["wheat"] -= 1

def sim_buy_settlement(ai):
    global total_settlements
    global resource_cards
    global settlements_owned_arr
    possible_settlement_locations = get_possible_settlement_locations()
    settlement = [0, 0] #[vertex number, value of spot]
    for settle in possible_settlement_locations:
        if(ai["best_vertices"][settle] >= settlement[1]):
            settlement[0] = settle
            settlement[1] = ai["best_vertices"][settle]
    place_settlement(settlement[0])
    total_settlements += 1
    resource_cards["wood"] -= 1
    resource_cards["brick"] -= 1
    resource_cards["wool"] -= 1
    resource_cards["wheat"] -= 1

def buy_city():
    global total_cities
    global resource_cards
    global settlements_owned_arr
    possible_city = get_possible_city_locations()
    city = int(input("Place a city (enter one of the following numbers: " + str(possible_city) + ")"))
    while (city not in possible_city):
        print("That was not a valid city location")
        city = int(input("Place a city (enter one of the following numbers: " + str(possible_city) + ")"))
    settlements_owned_arr[city] = 2
    resource_cards["ore"] -= 3
    resource_cards["wheat"] -= 2

def sim_buy_city(ai):
    global total_cities
    global resource_cards
    global settlements_owned_arr
    possible_city = get_possible_city_locations()
    city = [0, 0]
    for city_loop in possible_city:
        if(ai["best_vertices"][city_loop] >= city[1]):
            city[0] = city_loop
            city[1] = ai["best_vertices"][city_loop]
    settlements_owned_arr[city[0]] = 2
    resource_cards["ore"] -= 3
    resource_cards["wheat"] -= 2

def buy_dev_card():
    global resource_cards
    global dev_cards
    global dev_deck
    drawn_card = dev_deck.pop()
    resource_cards["ore"] -= 1
    resource_cards["wool"] -= 1
    resource_cards["wheat"] -= 1
    dev_cards[drawn_card] += 1

def update_ai(ai):
    ai = update_value_of_goals(ai)
    ai = update_value_of_resources(ai)
    ai = update_vertex_values(ai)
    ai = update_edge_values(ai)
    ai = update_robber_hex_values(ai)
    return ai

def update_value_of_goals(ai):
    global total_roads
    global total_settlements
    global total_cities
    global max_roads
    global max_cities
    global max_settlements
    if(total_roads >= max_roads):
        ai["value_of_goals"]["road"] = 0
    if (total_cities >= max_cities):
        ai["value_of_goals"]["city"] = 0
    if (total_settlements >= max_settlements):
        ai["value_of_goals"]["settlement"] = 0
    if (total_settlements < max_settlements and ai["value_of_goals"]["settlement"] == 0):
        ai["value_of_goals"]["settlement"] = 1
    return ai

def update_value_of_resources(ai):
    global resource_cards
    global road_resource_cards
    global settlement_resource_cards
    global city_resource_cards
    global dev_resource_cards
    #Loop through what can be bought
        #Loop through each resource required
            #Compare resources in hand to those required
        #If every resource is exact, the value of those resources is higher
        #If a small portion of the materials required are missing, that resource value skyrockets based on the total resources needed
        #If there is an excess of some material, slightly decrease its value
        #Changes during each possible buy should be weighted by the propensity to buy that thing
    #Decrease value of resource for each copy more than 4
    for resource in road_resource_cards:
        reqs = 2
        diff = road_resource_cards[resource] - resource_cards[resource] #requirements - hand
        if(diff == 0):
            ai["value_of_resources"][resource] += ai["weight_no_diff"] * resource_cards[resource] * reqs * ai["value_of_goals"]["road"]
        if(diff == 1):
            ai["value_of_resources"][resource] += ai["weight_small_diff"] * reqs * ai["value_of_goals"]["road"]
        if(diff > 1):
            ai["value_of_resources"][resource] += ai["weight_big_diff"] * diff * ai["value_of_goals"]["road"]
        if (diff < 0):
            ai["value_of_resources"][resource] += ai["weight_neg_diff"] * diff * ai["value_of_goals"]["road"]
    for resource in settlement_resource_cards:
        reqs = 4
        diff = settlement_resource_cards[resource] - resource_cards[resource] #requirements - hand
        if(diff == 0):
            ai["value_of_resources"][resource] += ai["weight_no_diff"] * resource_cards[resource] * reqs * ai["value_of_goals"]["settlement"]
        if(diff == 1):
            ai["value_of_resources"][resource] += ai["weight_small_diff"] * reqs * ai["value_of_goals"]["settlement"]
        if(diff > 1):
            ai["value_of_resources"][resource] += ai["weight_big_diff"] * diff * ai["value_of_goals"]["settlement"]
        if (diff < 0):
            ai["value_of_resources"][resource] += ai["weight_neg_diff"] * diff * ai["value_of_goals"]["settlement"]
    for resource in city_resource_cards:
        reqs = 5
        diff = city_resource_cards[resource] - resource_cards[resource] #requirements - hand
        if(diff == 0):
            ai["value_of_resources"][resource] += ai["weight_no_diff"] * resource_cards[resource] * reqs * ai["value_of_goals"]["city"]
        if(diff == 1):
            ai["value_of_resources"][resource] += ai["weight_small_diff"] * reqs * ai["value_of_goals"]["city"]
        if(diff > 1):
            ai["value_of_resources"][resource] += ai["weight_big_diff"] * diff * ai["value_of_goals"]["city"]
        if (diff < 0):
            ai["value_of_resources"][resource] += ai["weight_neg_diff"] * diff * ai["value_of_goals"]["city"]
    for resource in dev_resource_cards:
        reqs = 3
        diff = dev_resource_cards[resource] - resource_cards[resource] #requirements - hand
        if(diff == 0):
            ai["value_of_resources"][resource] += ai["weight_no_diff"] * resource_cards[resource] * reqs * ai["value_of_goals"]["dev"]
        if(diff == 1):
            ai["value_of_resources"][resource] += ai["weight_small_diff"] * reqs * ai["value_of_goals"]["dev"]
        if(diff > 1):
            ai["value_of_resources"][resource] += ai["weight_big_diff"] * diff * ai["value_of_goals"]["dev"]
        if (diff < 0):
            ai["value_of_resources"][resource] += ai["weight_neg_diff"] * diff * ai["value_of_goals"]["dev"]
    #Make sure no resources are in the negatives
    max = 0
    for resource in resource_cards:
        if (ai["value_of_resources"][resource] <= 0):
            ai["value_of_resources"][resource] = 0.01
        if (ai["value_of_resources"][resource] > max):
            max = ai["value_of_resources"][resource]
    #Scale resources so the maximum is equal to ai["max_resource_value"]
    for resource in resource_cards:
        if (ai["value_of_resources"][resource] > ai["max_resource_value"]):
            ai["value_of_resources"][resource] = ai["max_resource_value"] * ai["value_of_resources"][resource] / max
    return ai

def update_vertex_values(ai):
    global settlement_locations_arr
    global road_locations_arr
    global hex_tiles_arr
    global port_locations_arr
    max_value = 0
    for vertex in ai["best_vertices"]:
        value = 0
        for hex in settlement_locations_arr[vertex][0]:
            if(hex_tiles_arr[hex][0] != "dessert"):
                value += hex_tiles_arr[hex][1] * ai["value_of_resources"][hex_tiles_arr[hex][0]] * ai["weight_hex"]
            else:
                value += ai["weight_dessert"]
        if(vertex in port_locations_arr):#Add port_weight if vertex has a port
            value += ai["weight_has_port"]
        ai["best_vertices"][vertex] += value * ai["weight_hex_change"]
        if (ai["best_vertices"][vertex] > max_value):
            max_value = ai["best_vertices"][vertex]
    for vertex in ai["best_vertices"]:
        if(ai["best_vertices"][vertex] <= 0):
            ai["best_vertices"][vertex] = 0.01
        if(ai["best_vertices"][vertex] > ai["max_vertex_value"]):
            ai["best_vertices"][vertex] = ai["best_vertices"][vertex] * ai["max_vertex_value"] / max_value
    return ai

def update_edge_values(ai):
    global settlement_locations_arr
    global road_locations_arr
    global hex_tiles_arr
    global settlements_owned_arr
    #Each road is connected by two vertices. The value of an edge should just be the average of these two values
    for edge in ai["best_edges"]:
        vertexes = []
        for vertex in settlements_owned_arr:
            if(edge in settlement_locations_arr[vertex][2]):
                vertexes.append(ai["best_vertices"][vertex])
        sum = 0
        for i in vertexes:
            sum += i
            sum = sum / len(vertexes)
        ai["best_edges"][edge] = sum
    return ai

def update_robber_hex_values(ai):
    global settlement_locations_arr
    global settlements_owned_arr
    global hex_tiles_arr
    for hex in hex_tiles_arr:
        for vertex in settlements_owned_arr:
            if(hex in settlement_locations_arr[vertex][0]):
                if(settlements_owned_arr[vertex] == 1 or settlements_owned_arr[vertex] == 2):
                    ai["best_robber_hexes"][hex] = 0 #Don't place robber where you have settlements
    return ai

def play_game_manually():
    global game_won
    global simming
    simming = False
    generate_board()
    update_gamestate(1)
    print_board()
    place_initial_settlements()
    game_won = False
    while game_won == False:
        update_gamestate(1)
        get_resources(0)#Function takes in ai, if playing manually, use anything
        print_hand()
        d_card = ask_to_play_dev_cards()
        if d_card != None:
            play_card(d_card)
        port_trade = ask_to_port_trade()
        while port_trade != None:
            port_trade = ask_to_port_trade()
        bought = ask_to_buy()
        while bought != None:
            print_board()
            if bought == "road":
                buy_road()
            if bought == "settlement":
                buy_settlement()
            if bought == "city":
                buy_city()
            if bought == "development card":
                buy_dev_card()
            update_gamestate(1)
            bought = ask_to_buy()

def sim_game(ai, seed):
    global won_game
    global simming
    global victory_points
    global has_longest_road
    global has_largest_army
    global turns_taken
    global max_turns
    random.seed(seed)
    max_turns = 800
    simming = True
    generate_board()
    update_gamestate(ai)
    game_won = False
    sim_place_initial_settlements(ai)
    while game_won == False and turns_taken < max_turns:
        update_gamestate(ai)
        get_resources(ai)
        print_hand()
        print(ai["value_of_goals"])
        debug_negative_hand()
        d_card = determine_if_ai_plays_dev_cards(ai)
        if d_card != None:
            sim_play_card(d_card, ai)
        port_trade = sim_ask_to_port_trade(ai)
        while len(port_trade) > 0:
            sim_port_trade(port_trade)
            port_trade = sim_ask_to_port_trade(ai)
        bought = sim_ask_to_buy(ai)
        while bought != None:
            if bought == "road":
                sim_buy_road(ai)
            if bought == "settlement":
                sim_buy_settlement(ai)
            if bought == "city":
                sim_buy_city(ai)
            if bought == "development card":
                buy_dev_card()
            update_gamestate(ai)
            bought = sim_ask_to_buy(ai)
        if(victory_points > 9):
            game_won = True
    print("You won!!!")
    print_hand()
    print_board()
    print("Did you have longest road? " + str(has_longest_road))
    print("Did you have largest army? " + str(has_largest_army))
    return turns_taken


def debug_negative_hand():
    global resource_cards
    for resource in resource_cards:
        if resource_cards[resource] < 0:
            print("resource cards negative")
            temp_var = input("lol")

#play_game_manually()