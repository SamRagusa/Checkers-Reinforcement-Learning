'''
Created on Dec 3, 2016

@author: Sam Ragusa
'''
from game import Board




"""
As of now:
Characteristics = [own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_bottem]
"""
def follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges, own_base):
    if own_pieces + own_kings > 12 or own_pieces + own_kings < 1:
        return False
    if opp_pieces + opp_kings > 12 or opp_pieces + opp_kings < 1:
        return False
    if own_side_edges + own_base > own_pieces + own_kings:
        return False
    return True


"""
IMPORTANT NOTES:
-Make sure to change the if True: to if piece belongs to player_id
"""  
def get_states_from_boards_spots(state_array, boards_spots,player_id):
    piece_counters = [[0,0,0,0,0,0]*len(boards_spots)] #[[own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_bottem], ...]
    
    for k in range(len(boards_spots)):
        for j in range(len(boards_spots[k])):
            for i in range(len(boards_spots[k][j])):
                if boards_spots[k][j][i] != 0:
                    piece_counters[k][boards_spots[k][j][i]-1] = piece_counters[k][boards_spots[k][j][i]-1] + 1
                    
                    if True: ##################MUST MAKE IT IF THE PIECE BELONGS TO THE PLAYER MATHCHING PLAYER_ID
                        if i==0 and j%2==0:
                            piece_counters[k][4] = piece_counters[k][4] + 1
                        elif i==3 and j%2==1:
                            piece_counters[k][4] = piece_counters[k][4] + 1
                
                        if j==0:
                            piece_counters[k][5] = piece_counters[k][5] + 1
                            
    return [state_array.index(counters) for counters in piece_counters]
                                 
                
def get_desired_transition_from_states(q_array, q_array_states, cur_state, state_array):
    best_state = -1
    best_state_value = -1
    for state in state_array:
        if state not in q_array_states[cur_state]:
            q_array_states[cur_state].append(state)
            q_array[cur_state].append(-999999999)  #APPEND ACTUAL INITIAL VALUE
    
    #IF SOME LOW PROBABILITY THAN PICK A STATE AT RANDOM
    
    #PICK STATE OUT OF STATE_ARRAY OPTIONS (BASED ON Q ARRAY)
            




state_array = []

for own_pieces in range(13):
    for own_kings in range(13):
        for opp_pieces in range(13):
            for opp_kings in range(13):
                for own_side_edges in range(9):
                    for own_base in range(5):
                        if follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges, own_base):
                            state_array.append([own_pieces,opp_pieces, own_kings, opp_kings, own_side_edges, own_base])


NUM_STATES = len(state_array)
NUM_GAMES_TO_PLAY = -1 #put in number of games to play


q_array = [[]*NUM_STATES]
q_array_states = [[]*NUM_STATES]

game_board = Board()
opponent = None   #put in opponent

for j in range(NUM_GAMES_TO_PLAY):
    while not game_board.is_game_over():
        #AI makes move
        
        if not game_board.is_game_over():
            #opponent makes move
            #maybe want to train the q-array here
            pass
    
    
    #maybe want to train the q-array here
    
    game_board.wipe_board()
    
    