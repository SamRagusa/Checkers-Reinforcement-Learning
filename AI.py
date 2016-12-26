'''
Created on Dec 3, 2016

@author: Sam Ragusa
'''


import random, copy, time
from game import Board
from math import floor, ceil
#import matplotlib.pyplot as plt


def follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges):
    """
    As of now: 
    Characteristics = [own_pieces, opp_pieces, own_kings, opp_kings, own_edges]
    """
    if own_pieces + own_kings > 12 or own_pieces + own_kings < 0:
        return False
    if opp_pieces + opp_kings > 12 or opp_pieces + opp_kings < 0:
        return False
    if own_side_edges > own_pieces + own_kings + 2:
        return False
    return True


def get_states_from_boards_spots(state_array, boards_spots,player_id):
    """
    Format for a states piece_counter:
    [[own_pieces, opp_pieces, own_kings, opp_kings, own_edges], ...]
    """
    piece_counters = [[0,0,0,0,0] for j in range(len(boards_spots))] 
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
                
#                         if j==0:
#                             piece_counters[k][5] = piece_counters[k][5] + 1
                        
    return [state_array.index(counters) for counters in piece_counters]
                                 

def get_desired_transition_between_states(q_array, q_array_states, cur_state, possible_state_array,random_move_probability=0):
    """
    Notes:
    -Currently using "optimistic initial conditions"
    -should be done but haven't checked carefully
    """
    done_transitions = []
    for state in possible_state_array:
        if state not in done_transitions:
            if state not in q_array_states[cur_state]:
                q_array_states[cur_state].append(state)
                q_array[cur_state].append(1)  
            done_transitions.append(state)
    
    if random != 0 and random.random() < random_move_probability:
        try:
            return done_transitions[random.randint(0, len(done_transitions)-1)]
        except:
            return []
    
    try:
        return done_transitions[done_transitions.index(max(done_transitions))]
    except ValueError:
        return []    


def get_next_desired_move(board, state_array, q_array, q_array_states, player_id, random_move_probability = 0):
    """
    """
    possible_next_moves = board.get_possible_next_moves()
    #possible_next_board_spots = board.get_potential_spots_from_moves(possible_next_moves)
    possible_next_states = get_states_from_boards_spots(state_array, board.get_potential_spots_from_moves(possible_next_moves), player_id)
    
    #cur_state = get_states_from_boards_spots(state_array, [board.spots], player_id)[0]
    desired_next_state = get_desired_transition_between_states(q_array, q_array_states, get_states_from_boards_spots(state_array, [board.spots], player_id)[0], possible_next_states, random_move_probability)
    
    considered_moves = []
    for j in range(len(possible_next_states)):
        if possible_next_states[j] == desired_next_state:
            considered_moves.append(possible_next_moves[j])
    try:
        return considered_moves[random.randint(0,len(considered_moves)-1)]
    except ValueError:
        return []

def get_number_of_pieces_and_kings(spots, player_id):
    """
    Gets the number of pieces and the number of kings that a given user has on the board configuration
    represented in the given spots.
    """
    if player_id:
        piece = 1
        king = 3
    else:
        piece = 2 
        king = 4
        
    piece_counter = 0
    king_counter = 0
    for row in spots:
        for element in row:
            if element == piece:
                piece_counter = piece_counter + 1
            elif element == king:
                king_counter = king_counter + 1
    return [piece_counter,king_counter]


def reward_function(state_info1, state_info2):
    """
    Reward for transitioning from state with state_info1 to state with state_info2.
    """
    if state_info2[1] == 0 and state_info2[3] == 0:
        return 5
    if state_info2[0] == 0 and state_info2[2] == 0:
        return -5
    return .1*(state_info2[0]-state_info1[0] + 3*(state_info2[2]-state_info1[2])-(state_info2[1]-state_info1[1])-3*(state_info2[3]-state_info1[3]))


def get_random_move(board):
    """
    Gets a random next move that can be taken from the current configuration of the Board given.
    """
    possible_moves = board.get_possible_next_moves()
    if possible_moves:
        return possible_moves[random.randint(0,len(possible_moves)-1)]
    else:
        return []


def is_terminal(board):
    """
    """
    if not board.get_possible_next_moves():
        return True
    return False


def alphabeta(board, depth, alpha, beta, maximizing_player, player_id):
    """
    """
    if depth == 0:
        if is_terminal(board):
            if get_number_of_pieces_and_kings(board.spots, player_id) == [0,0]:
                return float('inf'), None
            elif get_number_of_pieces_and_kings(board.spots, not player_id) == [0,0]: 
                return float('-inf'), None
            else:
                return 0, None
        self_info = get_number_of_pieces_and_kings(board.spots, player_id)
        opp_info = get_number_of_pieces_and_kings(board.spots, not player_id)
        return self_info[0] + 3*self_info[1] - (opp_info[0] + 3*opp_info[1]) , None
                
    possible_moves = board.get_possible_next_moves()
    potential_spots = board.get_potential_spots_from_moves(possible_moves)
    desired_move_index = None
    if maximizing_player:
        v = float('-inf')
        for j in range(len(potential_spots)):
            cur_board = Board.Board(potential_spots[j], not board.player_turn)
            alpha_beta_results = alphabeta(cur_board, depth - 1, alpha, beta, False, player_id)
            
            if v != max(v, alpha_beta_results[0]):
                v = max(v, alpha_beta_results[0])
                alpha = max(alpha, v)
                desired_move_index = j
            if beta <= alpha:
                break
        if desired_move_index is None:
            return v, None
        return v, possible_moves[desired_move_index]
    else:
        v = float('inf')
        for j in range(len(potential_spots)):
            cur_board = Board.Board(potential_spots[j], not board.player_turn)
            alpha_beta_results = alphabeta(cur_board, depth - 1, alpha, beta, True, player_id)

            if v != min(v, alpha_beta_results[0]):
                v = min(v, alpha_beta_results[0])
                desired_move_index = j
                beta = min(beta, v)
            if beta <= alpha:
                break
        if desired_move_index is None:
            return v, None
        return v, possible_moves[desired_move_index]


state_array = []

for own_pieces in range(13):
    for own_kings in range(13):
        for opp_pieces in range(13):
            for opp_kings in range(13):
                for own_side_edges in range(9):
                    if follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges):
                        state_array.append([own_pieces,opp_pieces, own_kings, opp_kings, own_side_edges])


#print(len(state_array))

LEARNING_RATE = .0000001  #properly pick this
DISCOUNT_FACTOR = .3 #properly pick this (start low  [above 0] then gradually go to 1)
NUM_STATES = len(state_array)
NUM_GAMES_TO_PLAY = 6000
NUM_GAMES_FOR_TESTING = 1000
PLAYER_ID = True
ALPHA_BETA_DEPTH = 1
MOVE_LIMIT = 1000
TEST_MOVE_LIMIT = 2000
TRAINING_RANDOM_MOVE_PROBABILITY = .1
INTERVAL_ANALYSIS_SIZE = 25


q_array = [[]for j in range(NUM_STATES)]
q_array_states = [[] for j in range(NUM_STATES)]

game_board = Board.Board()
#game_board.print_board()
opponent = None   #put in opponent, and have it have function get_next_move(Board, player_id) function

"""
IMPORTANT NOTE:
-must run training step but without training the Q_array a bunch of
times first so that the AI is able to get an estimate of optimal future
value which is defined as max value in new states Q vector for any action
"""


training_win_counter = 0
training_loss_counter = 0
testing_win_counter = 0
testing_loss_counter = 0
move_counter = 0
move_limit_counter = 0
old_move_limit_counter = 0
game_move_counter =[0]*NUM_GAMES_TO_PLAY
game_move_limit_counter = [0]*ceil(NUM_GAMES_TO_PLAY / INTERVAL_ANALYSIS_SIZE)
game_win_counter = [0]*ceil(NUM_GAMES_TO_PLAY/ INTERVAL_ANALYSIS_SIZE)
game_loss_counter = [0]*ceil(NUM_GAMES_TO_PLAY / INTERVAL_ANALYSIS_SIZE)
#game_is_over = False  
start_time = time.time()
for j in range(NUM_GAMES_TO_PLAY):
    if j==NUM_GAMES_TO_PLAY - NUM_GAMES_FOR_TESTING:
        print("COMPLETED TRAINING FOR RANDOM MOVE PROBABILITY: " + str(TRAINING_RANDOM_MOVE_PROBABILITY) + ",  STARTING TESTING!")
        TRAINING_RANDOM_MOVE_PROBABILITY = 0
        training_time = time.time() - start_time
        start_time = time.time()
        #ALPHA_BETA_DEPTH = 2
    testing_counter = 0
    game_is_over = False
    while not game_is_over:
        testing_counter = testing_counter + 1
        #if testing_counter%500 == 0:
            #print("Testing counter: " + str(testing_counter))
            #game_board.print_board()
        #print("test2 game: " + str(j))
        #if j>20:
        
        own_last_state = get_states_from_boards_spots(state_array, [game_board.get_potential_spots_from_moves(None)],PLAYER_ID)[0]
        next_move = get_next_desired_move(game_board, state_array, q_array, q_array_states, PLAYER_ID)
        #next_move = get_random_move(game_board)
        if next_move:
#             if j%10 == 0:
#                 game_board.print_board()
#                 print("")
            game_board.make_move(get_next_desired_move(game_board, state_array, q_array, q_array_states, PLAYER_ID, TRAINING_RANDOM_MOVE_PROBABILITY))
            state_moved_to = get_states_from_boards_spots(state_array, [game_board.get_potential_spots_from_moves(None)],PLAYER_ID)[0]
            game_move_counter[j] = game_move_counter[j] + 1
            move_counter = move_counter + 1
            if not game_board.is_game_over():
                next_move = alphabeta(game_board, ALPHA_BETA_DEPTH, float('-inf'), float('inf'), True, False)[1]
                #next_move = get_random_move(game_board)
                if next_move and (TRAINING_RANDOM_MOVE_PROBABILITY == 0 or game_move_counter[j] < MOVE_LIMIT):
#                     if j%10 == 0:
#                         game_board.print_board()
                    game_board.make_move(next_move)
                    game_move_counter[j] = game_move_counter[j] + 1
                    move_counter = move_counter + 1
                    game_is_over = game_board.is_game_over()
                    if (TRAINING_RANDOM_MOVE_PROBABILITY == 0) and (TEST_MOVE_LIMIT <= game_move_counter[j]):
                        game_is_over = True
                        move_limit_counter = move_limit_counter + 1
                        
                else:
                    game_is_over = True
                    if game_move_counter[j] >= MOVE_LIMIT and TRAINING_RANDOM_MOVE_PROBABILITY != 0:
                        move_limit_counter = move_limit_counter + 1

                #game_board.make_move(opponent.get_next_move(game_board, not PLAYER_ID))
                #if j > 20: 
                #new_state = get_states_from_boards_spots(state_array, [game_board.get_potential_spots_from_moves(None)],PLAYER_ID)[0]
#                 if q_array[new_state]:
#                     #estimate_of_optimal_future_value = max(q_array[new_state])
#                     #print(estimate_of_optimal_future_value)
#                     index_in_q_array = q_array_states[own_last_state].index(new_state)
#                     q_array[own_last_state][index_in_q_array] = q_array[own_last_state][index_in_q_array] + LEARNING_RATE*(reward_function(state_array[own_last_state],state_array[new_state]) + DISCOUNT_FACTOR*max(q_array[new_state]) - q_array[own_last_state][q_array_states[own_last_state].index(new_state)])
                
            else:
                game_is_over = True
                
            new_state = get_states_from_boards_spots(state_array, [game_board.get_potential_spots_from_moves(None)],PLAYER_ID)[0]
            if q_array[new_state]:
                #estimate_of_optimal_future_value = max(q_array[new_state])
                #print(estimate_of_optimal_future_value)
                index_in_q_array = q_array_states[own_last_state].index(state_moved_to)
                q_array[own_last_state][index_in_q_array] = q_array[own_last_state][index_in_q_array] + LEARNING_RATE*(reward_function(state_array[own_last_state],state_array[new_state]) + DISCOUNT_FACTOR*max(q_array[new_state]) - q_array[own_last_state][index_in_q_array])
            elif is_terminal(game_board):
                index_in_q_array = q_array_states[own_last_state].index(state_moved_to)
                q_array[own_last_state][index_in_q_array] = q_array[own_last_state][index_in_q_array] + LEARNING_RATE*(reward_function(state_array[own_last_state],state_array[new_state]) - q_array[own_last_state][index_in_q_array])
        else:
            game_is_over = True
    else:
        #game_board.print_board()
        #print(get_number_of_pieces_and_kings(game_board.spots, PLAYER_ID))
        #print(get_number_of_pieces_and_kings(game_board.spots, not PLAYER_ID))
        if get_number_of_pieces_and_kings(game_board.spots, PLAYER_ID) == [0,0]:
            print("Game lost!  Has been " + str(j+1) +  " games played in "  + str(time.time()-start_time) + " seconds ")
            game_loss_counter[floor(j/INTERVAL_ANALYSIS_SIZE)] = game_loss_counter[floor(j/INTERVAL_ANALYSIS_SIZE)] + 1
            if TRAINING_RANDOM_MOVE_PROBABILITY != 0:
                training_loss_counter = training_loss_counter + 1
            else:
                testing_loss_counter = testing_loss_counter + 1
        elif get_number_of_pieces_and_kings(game_board.spots, not PLAYER_ID) == [0,0]:
            print("Game won!  Has been " + str(j+1) +  " games played in "  + str(time.time()-start_time) + " seconds ")
            game_win_counter[floor(j/INTERVAL_ANALYSIS_SIZE)] = game_win_counter[floor(j/INTERVAL_ANALYSIS_SIZE)] + 1
            if TRAINING_RANDOM_MOVE_PROBABILITY != 0:
                training_win_counter = training_win_counter + 1
            else:
                testing_win_counter = testing_win_counter + 1            
        elif old_move_limit_counter != move_limit_counter:
            print("Game exceeded move limit!  Has been " + str(j+1) +  " games played in "  + str(time.time()-start_time) + " seconds ")
            old_move_limit_counter = move_limit_counter
            game_move_limit_counter[floor(j/INTERVAL_ANALYSIS_SIZE)] = game_move_limit_counter[floor(j/INTERVAL_ANALYSIS_SIZE)] + 1
        else:
            print("Game tied!  Has been " + str(j+1) +  " games played in "  + str(time.time()-start_time) + " seconds ")
        game_board.wipe_board()
        

  
        

the_sum = 0
num_states_used = 0
max_transitions = 0
for temp in q_array:
    if len(temp)!=0:
        if len(temp) > max_transitions:
            max_transitions = len(temp)
        the_sum = the_sum + len(temp)
        num_states_used = num_states_used + 1
        
avg = float(the_sum)/num_states_used
    

game_tie_counter = [int(INTERVAL_ANALYSIS_SIZE-game_loss_counter[j]-game_win_counter[j] - game_move_limit_counter[j]) for j in range(int(NUM_GAMES_TO_PLAY/INTERVAL_ANALYSIS_SIZE))]


print("Training Information:")
print("Learning rate: " + str(LEARNING_RATE))
print("Discount factor: " + str(DISCOUNT_FACTOR))
print("Alpha-Beta depth: " + str(ALPHA_BETA_DEPTH))
print("Random move probability: " + str(TRAINING_RANDOM_MOVE_PROBABILITY))
print("Total time to play " + str(NUM_GAMES_TO_PLAY - NUM_GAMES_FOR_TESTING) + " games: " + str(training_time))
print("Average time to play a game: " + str(training_time / (NUM_GAMES_TO_PLAY - NUM_GAMES_FOR_TESTING)))
print("Games won: " + str(training_win_counter))
print("Games lost: " + str(training_loss_counter))
print("Games tied: " + str(NUM_GAMES_TO_PLAY-NUM_GAMES_FOR_TESTING-training_win_counter-training_loss_counter))
print("Games exceeding move limit: " + str(move_limit_counter))
#print("Total number of moves made: " + str(move_counter))
#print("Average moves per game: " + str(float(move_counter)/NUM_GAMES_TO_PLAY))
print("Maximum transitions for a state: " + str(max_transitions))
print("Total transitions: " + str(the_sum))
print("Average Transitions per state used: " + str(avg))




print("")
print("")
print("Testing Information:")
print("Total time to play " + str(NUM_GAMES_FOR_TESTING) + " games: " + str(time.time() - start_time))
print("Average time to play a game: " + str((float(time.time())- start_time)/ NUM_GAMES_FOR_TESTING))
print("Games won: " + str(testing_win_counter))
print("Games lost: " + str(testing_loss_counter))
print("Games tied: " + str(NUM_GAMES_FOR_TESTING-testing_win_counter - testing_loss_counter))
print("Wins over " + str(INTERVAL_ANALYSIS_SIZE) + " game intervals: " + str(game_win_counter))
print("Losses over " + str(INTERVAL_ANALYSIS_SIZE) + " game intervals: " + str(game_loss_counter))
print("Ties over " + str(INTERVAL_ANALYSIS_SIZE) + " game intervals: " + str(game_tie_counter))    

sum_delta_moves_init = 0
sum_delta_moves_final = 0
for j in range(NUM_GAMES_FOR_TESTING):
    sum_delta_moves_init = sum_delta_moves_init + game_move_counter[j]
    sum_delta_moves_final = sum_delta_moves_final + game_move_counter[len(game_move_counter)-NUM_GAMES_FOR_TESTING + j]
sum_delta_moves_final = sum_delta_moves_final/NUM_GAMES_FOR_TESTING
sum_delta_moves_init = sum_delta_moves_init/NUM_GAMES_FOR_TESTING

#print("Average number of moves for first 25 games: " + str(sum_delta_moves_init))
print("Average number of moves for each testing game: " + str(sum_delta_moves_final))