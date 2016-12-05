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


def get_states_from_boards_spots(state_array, boards_spots,player_id):
    piece_counters = [[0,0,0,0,0,0]*len(boards_spots)] #[[own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_bottem], ...]
    
    for k in range(len(boards_spots)):
        for j in range(len(boards_spots[k])):
            for i in range(len(boards_spots[k][j])):
                if boards_spots[k][j][i] != 0:
                    piece_counters[k][boards_spots[k][j][i]-1] = piece_counters[k][boards_spots[k][j][i]-1] + 1
                    
                    if (player_id and (boards_spots[k][j][i] == 1 or boards_spots[k][j][i] == 3)) or (not player_id and (boards_spots[k][j][i] == 2 or boards_spots[k][j][i] == 4)):
                        if i==0 and j%2==0:
                            piece_counters[k][4] = piece_counters[k][4] + 1
                        elif i==3 and j%2==1:
                            piece_counters[k][4] = piece_counters[k][4] + 1
                
                        if j==0:
                            piece_counters[k][5] = piece_counters[k][5] + 1
                            
    return [state_array.index(counters) for counters in piece_counters]
                                 
                
def get_desired_transition_between_states(q_array, q_array_states, cur_state, state_array):
    best_state = -1
    best_state_value = -1
    done_transitions = []
    for state in state_array:
        if not state in done_transitions:
            if state not in q_array_states[cur_state]:
                q_array_states[cur_state].append(state)
                q_array[cur_state].append(-999999999)  #APPEND ACTUAL INITIAL VALUE
            done_transitions.append(state)
    
    #IF SOME LOW PROBABILITY THAN PICK A STATE AT RANDOM
    
    #PICK STATE OUT OF STATE_ARRAY OPTIONS (BASED ON Q ARRAY)
            

def get_next_desired_move(board, state_array, q_array, q_array_states, player_id):
    
    possible_next_moves = board.get_possible_next_moves()
    possible_next_board_spots = board.get_potential_spots_from_moves(possible_next_moves)
    possible_next_states = get_states_from_boards_spots(state_array, possible_next_board_spots, player_id)
    
    cur_state = get_states_from_boards_spots(state_array, [board.spots], player_id)[0]
    
    desired_transition = get_desired_transition_between_states(q_array, q_array_states, cur_state, state_array)
    
    #if more than one move that goes does desired transition return one randomly,
    #if not return the only one that does
    
    pass




state_array = []

for own_pieces in range(13):
    for own_kings in range(13):
        for opp_pieces in range(13):
            for opp_kings in range(13):
                for own_side_edges in range(9):
                    for own_base in range(5):
                        if follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges, own_base):
                            state_array.append([own_pieces,opp_pieces, own_kings, opp_kings, own_side_edges, own_base])


LEARNING_RATE = -1  #put in learning rate
NUM_STATES = len(state_array)
NUM_GAMES_TO_PLAY = -1 #put in number of games to play
PLAYER_ID = True

q_array = [[]*NUM_STATES]
q_array_states = [[]*NUM_STATES]

game_board = Board()
opponent = None   #put in opponent

move_counter = [0]*NUM_GAMES_TO_PLAY
for j in range(NUM_GAMES_TO_PLAY):
    while not game_board.is_game_over():
        #AI makes move
        #game_board.make_move(get_next_desired_move(game_board, state_array, q_array, q_array_states, PLAYER_ID))
        move_counter[j] = move_counter[j] + 1
        
        if not game_board.is_game_over():
            #opponent makes move
            #maybe want to train the q-array here
            move_counter[j] = move_counter[j] + 1
            pass
    
    
    #maybe want to train the q-array here
    
    game_board.wipe_board()
    
    