'''
Created on Dec 3, 2016

@author: Sam Ragusa
'''


import random, copy, time
from game import Board



"""
As of now:
Characteristics = [own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_bottem]
"""
def follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges, own_base):
    if own_pieces + own_kings > 12 or own_pieces + own_kings < 0:
        return False
    if opp_pieces + opp_kings > 12 or opp_pieces + opp_kings < 0:
        return False
    if own_side_edges + own_base > own_pieces + own_kings + 2:
        return False
    return True


"""
Format for a states piece_counter:
[[own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_bottem], ...]
"""
def get_states_from_boards_spots(state_array, boards_spots,player_id):
    piece_counters = [[0,0,0,0,0,0] for j in range(len(boards_spots))] 
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
                                 

"""
Notes:
-Currently using "optomistic initial conditions"
-should be done but haven't checked carefully
"""
def get_desired_transition_between_states(q_array, q_array_states, cur_state, possible_state_array,random_move_probability=.1):
    done_transitions = []
    for state in possible_state_array:
        if state not in done_transitions:
            if state not in q_array_states[cur_state]:
                q_array_states[cur_state].append(state)
                q_array[cur_state].append(1)  
            done_transitions.append(state)
    
    if(random.random() < random_move_probability):
        try:
            return done_transitions[random.randint(0, len(done_transitions)-1)]
        except:
            return []
    
    try:
        return done_transitions[done_transitions.index(max(done_transitions))]
    except ValueError:
        return []    


def get_next_desired_move(board, state_array, q_array, q_array_states, player_id):
    
    possible_next_moves = board.get_possible_next_moves()
    possible_next_board_spots = board.get_potential_spots_from_moves(possible_next_moves)
    possible_next_states = get_states_from_boards_spots(state_array, possible_next_board_spots, player_id)
    
    cur_state = get_states_from_boards_spots(state_array, [board.spots], player_id)[0]
    desired_next_state = get_desired_transition_between_states(q_array, q_array_states, cur_state, possible_next_states)
    
    considered_moves = []
    for j in range(len(possible_next_states)):
        if possible_next_states[j] == desired_next_state:
            considered_moves.append(possible_next_moves[j])
    try:
        return considered_moves[random.randint(0,len(considered_moves)-1)]
    except ValueError:
        return []


def reward_function(state1, state2):
    pass    #IMPLEMENT THIS


def get_random_move(board):

    possible_moves = board.get_possible_next_moves()
    if len(possible_moves) == 0:
        return False
    if len(possible_moves) != 0:
        return possible_moves[random.randint(0,len(possible_moves)-1)]
    else:
        return []

start_time = time.time()

state_array = []

for own_pieces in range(13):
    for own_kings in range(13):
        for opp_pieces in range(13):
            for opp_kings in range(13):
                for own_side_edges in range(9):
                    for own_base in range(5):
                        if follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges, own_base):
                            state_array.append([own_pieces,opp_pieces, own_kings, opp_kings, own_side_edges, own_base])


print(len(state_array))

LEARNING_RATE = None  #pick this (maybe .1)
DISCOUNT_FACTOR = None #pick this (start low  [above 0] then gradually go to 1)
NUM_STATES = len(state_array)
NUM_GAMES_TO_PLAY = 1000 
PLAYER_ID = True

q_array = [[]for j in range(NUM_STATES)]
q_array_states = [[] for j in range(NUM_STATES)]

game_board = Board.Board()
opponent = None   #put in opponent, and have it have function get_next_move(Board, player_id) function

"""
IMPORTANT NOTE:
-must run training step but without training the Q_array a bunch of
times first so that the AI is able to get an estimate of optimal future
value which is defined as max value in new states Q vector for any action
"""

move_counter = [0]*NUM_GAMES_TO_PLAY
for j in range(NUM_GAMES_TO_PLAY):
    while not game_board.is_game_over():
        #own_last_state = get_states_from_boards_spots(state_array, [game_board.get_potential_spots_from_moves(None)],PLAYER_ID)[0]
        next_move = get_next_desired_move(game_board, state_array, q_array, q_array_states, PLAYER_ID)
        if next_move:
            game_board.make_move(get_next_desired_move(game_board, state_array, q_array, q_array_states, PLAYER_ID))
            move_counter[j] = move_counter[j] + 1
        else:
            print("No more possible moves!")
            game_board.wipe_board()
            break
        
        if not game_board.is_game_over():
            next_move = get_random_move(game_board)
            if next_move:
                game_board.make_move(get_random_move(game_board))
            else:
                print("No more possible moves!")
                game_board.wipe_board()
                break
            #game_board.make_move(opponent.get_next_move(game_board, not PLAYER_ID)) 
            #new_state = get_states_from_boards_spots(state_array, [game_board.get_potential_spots_from_moves(None)],PLAYER_ID)[0]
            #estimate_of_optimal_future_value = None  #########PUT THIS IN#############
            #q_array[own_last_state][q_array_states[own_last_state].index(new_state)] = q_array[own_last_state][q_array_states[own_last_state].index(new_state)] + LEARNING_RATE*(reward_function(own_last_state,new_state) + DISCOUNT_FACTOR*estimate_of_optimal_future_value - q_array[own_last_state][q_array_states[own_last_state].index(new_state)])
            move_counter[j] = move_counter[j] + 1
    
    
    print(str(j+1) +  " Games played in "  + str(time.time()-start_time) + " seconds ")
    #game_board.print_board()
    game_board.wipe_board()
    
sum = 0
num_states_used = 0
for temp in q_array:
    if len(temp)!=0:
        sum = sum + len(temp)
        num_states_used = num_states_used + 1
print(sum)
avg = float(sum)/num_states_used
print(avg)
    
