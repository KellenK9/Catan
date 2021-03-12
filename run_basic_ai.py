import simulate_single_player as sim

base_ai = {
    "propensity_to_buy_settlement": 1, #If 1, AI will always buy settlement when able. If 0, AI will never buy settlement
    "propensity_to_buy_city": 1,
    "propensity_to_buy_road": 1,
    "propensity_to_buy_dev": 1,
    "propensity_to_play_knight": 1,
    "propensity_to_play_year_of_plenty": 1,
    "propensity_to_play_road_building": 1,
    "propensity_to_trade": 2, #Multiplier for how willing AI is to trade. If 1, ai will conduct even trades (value-wise). If 0.5, ai requires at least twice the value to conduct trade
    "weight_no_diff": 1, #Weighted value that can be adjusted by Machine Learning model for how resource values are adjusted
    "weight_small_diff": 1,
    "weight_big_diff": 1,
    "max_resource_value": 4, #Another variable to be tuned my a ML model, this controls the maximum value for the below dict
    "value_of_resources": { #This is the value placed upon each resource card by the ai, must be greater than 0 (not equal to 0)
        "wood": 1,
        "wheat": 1,
        "wool": 1,
        "ore": 1,
        "brick": 1
    },
    "best_robber_hexes": { #{hex number : value} The AI will place the robber on the highest valued hex available
        0: 0.5,
        1: 0.5,
        2: 0.5,
        3: 0.5,
        4: 3,
        5: 3,
        6: 0.5,
        7: 0.5,
        8: 3,
        9: 5,
        10: 3,
        11: 0.5,
        12: 0.5,
        13: 3,
        14: 3,
        15: 0.5,
        16: 0.5,
        17: 0.5,
        18: 0.5
    },
    "best_vertices": { #{hex number : value} The AI will buy settlements on the highest value open vertex.
        # The AI will buy cities on the settlement with the highest valued vertex
        0: 2,
        1: 2,
        2: 1,
        3: 2,
        4: 2,
        5: 1,
        6: 1,
        7: 2,
        8: 1,
        9: 1,
        10: 1,
        11: 1,
        12: 1,
        13: 1,
        14: 2,
        15: 2,
        16: 1,
        17: 2,
        18: 1,
        19: 1,
        20: 1,
        21: 1,
        22: 1,
        23: 1,
        24: 1,
        25: 1,
        26: 2,
        27: 1,
        28: 2,
        29: 1,
        30: 1,
        31: 1,
        32: 1,
        33: 1,
        34: 1,
        35: 1,
        36: 1,
        37: 2,
        38: 2,
        39: 1,
        40: 1,
        41: 1,
        42: 1,
        43: 1,
        44: 1,
        45: 1,
        46: 2,
        47: 2,
        48: 2,
        49: 1,
        50: 2,
        51: 2,
        52: 1,
        53: 1
    },
    "best_edges": { #{hex number : value} The AI will place roads on the highest valued edge
        0: 1,
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 1,
        16: 1,
        17: 1,
        18: 1,
        19: 1,
        20: 1,
        21: 1,
        22: 1,
        23: 1,
        24: 1,
        25: 1,
        26: 1,
        27: 1,
        28: 1,
        29: 1,
        30: 1,
        31: 1,
        32: 1,
        33: 1,
        34: 1,
        35: 1,
        36: 1,
        37: 1,
        38: 1,
        39: 1,
        40: 1,
        41: 1,
        42: 1,
        43: 1,
        44: 1,
        45: 1,
        46: 1,
        47: 1,
        48: 1,
        49: 1,
        50: 1,
        51: 1,
        52: 1,
        53: 1,
        54: 1,
        55: 1,
        56: 1,
        57: 1,
        58: 1,
        59: 1,
        60: 1,
        61: 1,
        62: 1,
        63: 1,
        64: 1,
        65: 1,
        66: 1,
        67: 1,
        68: 1,
        69: 1,
        70: 1,
        71: 1
    }
} #Whenever these values need to be updated put 'Update AI values' as comment in code
#This should be pretty often as the AI should update how it values certain hexes whenever the board_state changes

#Teddy only buys dev cards
Teddy = base_ai
Teddy["propensity_to_buy_city"] = 0
Teddy["propensity_to_buy_settlement"] = 0
Teddy["propensity_to_buy_road"] = 0
Teddy["propensity_to_trade"] = 4
Teddy["value_of_resources"]["wood"] = 0.1
Teddy["value_of_resources"]["brick"] = 0.1

sim.sim_game(base_ai)