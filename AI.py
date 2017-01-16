'''
Created on Dec 3, 2016

@author: Sam Ragusa
'''


import random, copy, time
from game import Board
from math import floor, ceil

class Player:
    """
    """
    
    def set_board(self, the_board):
        """
        """
        self.board = the_board
    
    def game_completed(self):
        """
        """
        pass
        




def reward_function(state_info1, state_info2):
    """
    Reward for transitioning from state with state_info1 to state with state_info2.

    NOTE:
    1) do something better with where/how this is implemented
    2) should give some kind of negative for tieing
    """
    if state_info2[1] == 0 and state_info2[3] == 0:
        return 10
    if state_info2[0] == 0 and state_info2[2] == 0:
        return -10
    return state_info2[0]-state_info1[0] + 2*(state_info2[2]-state_info1[2])-(state_info2[1]-state_info1[1])-2*(state_info2[3]-state_info1[3])



class Q_Learning_AI(Player):
    """
    TO-DO:
    1) add ability to train or not train when wanted
        A) when not training also don't look for/add currently unknown states
        B) do this by having an instance variable saying if it's testing or training
        C) and let a function set that parameter
    2) 
    3) create set method for random move probability and learning rate
    4) handle the rewards function which is coded as if the function were already defined
    """


    def __init__(self, the_player_id, the_learning_rate, the_discount_factor, the_random_move_probability=0, the_board=None):
        """
        """
        self.state_array = []
        for own_pieces in range(13):
            for own_kings in range(13):
                for opp_pieces in range(13):
                    for opp_kings in range(13):
                        for own_side_edges in range(9):
                            if self.follows_rules(own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges):
                                self.state_array.append([own_pieces,opp_pieces, own_kings, opp_kings, own_side_edges])
        
        self.q_array = [[]for j in range(len(self.state_array))]
        self.q_array_states = [[] for j in range(len(self.state_array))]
        self.num_states = len(self.state_array)
        self.random_move_probability = the_random_move_probability  #May want to rename this
        self.learning_rate = the_learning_rate    
        self.discount_factor = the_discount_factor
        self.player_id = the_player_id
        self.board = the_board
        self.pre_last_move_state = None
        self.post_last_move_state = None 
    

    def set_random_move_probability(self, probability):
        self.random_move_probability = probability
    

    def follows_rules(self, own_pieces, own_kings, opp_pieces, opp_kings, own_side_edges):
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


    def get_states_from_boards_spots(self, boards_spots):
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
                        if (self.player_id and (boards_spots[k][j][i] == 1 or boards_spots[k][j][i] == 3)) or (not self.player_id and (boards_spots[k][j][i] == 2 or boards_spots[k][j][i] == 4)):
                            if i==0 and j%2==0:
                                piece_counters[k][4] = piece_counters[k][4] + 1
                            elif i==3 and j%2==1:
                                piece_counters[k][4] = piece_counters[k][4] + 1
                        
        return [self.state_array.index(counters) for counters in piece_counters]
                                 

    def get_desired_transition_between_states(self, possible_state_array):#%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
        """
        NOTES:
        1) Change looking to see if the transitions are known to use mappings
        """
        cur_state = self.get_states_from_boards_spots([self.board.spots])[0]
        done_transitions = []
        for state in possible_state_array:#%%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
            if state not in done_transitions:
                if state not in self.q_array_states[cur_state]:
                    self.q_array_states[cur_state].append(state)
                    self.q_array[cur_state].append(5)  
                done_transitions.append(state)
    
        if random != 0 and random.random() < self.random_move_probability:
            try:
                return done_transitions[random.randint(0, len(done_transitions)-1)]
            except:
                return []
    
        try:
            return done_transitions[done_transitions.index(max(done_transitions))]
        except ValueError:
            return []    


    def game_completed(self):
        """
        """
        index_in_q_array = self.q_array_states[self.pre_last_move_state].index(self.post_last_move_state)
        cur_state = self.get_states_from_board_spots([self.board.spots])[0]
    
        self.q_array[self.pre_last_move_state][index_in_q_array] = self.q_array[self.pre_last_move_state][index_in_q_array] + self.learning_rate * (reward_function(self.state_array[self.pre_last_move_state], self.state_array[cur_state])- self.q_array[self.pre_last_move_state][index_in_q_array])
        
        self.pre_last_move_state = None
        self.post_last_move_state = None

    def get_q_array_info(self):
        """
        returns in form: [min_trans, max_trans, avg_trans, total_trans, min_val, max_val, avg_val, total_states_used]
        """
        the_sum = 0
        num_states_used = 0
        min_transitions = float("inf")
        max_transitions = float("-inf")
        min_value = float("inf")
        max_value = float("-inf")
        total_value = 0
        for temp1 in self.q_array:
            if len(temp1)!=0:
                if len(temp1) > max_transitions:
                    max_transitions = len(temp1)
                if len(temp1) < min_transitions:
                    min_transitions = len(temp1)
                the_sum = the_sum + len(temp1)
                num_states_used = num_states_used + 1
                for temp2 in temp1:
                    if temp2 > max_value:
                        max_value = temp2
                    if temp2 < min_value:
                        min_value = temp2
                    total_value = total_value + temp2
        return min_transitions, max_transitions, the_sum/num_states_used, the_sum, min_value, max_value, total_value/the_sum, num_states_used

        
        
    def get_optimal_potential_value(self, depth):
        """
        STRATEGY:
        1) Look forward in (actual) own transition states.  
        2) Look at board as self being the opponent and look forward in that situations transition states
        3) If not at depth go back to step (1)
        
        TODO:
        1) Approach this with algorithm similar to how minimax works
            a) look for set of transitions from (I think) current state of length depth by doing minimax
            b) Might also use alpha-beta pruining
            
        NOTES:
        1) depth is not actually looking ahead in possible moves, but actually simulating something similar (hopefully similar)
        """
        pass



    def get_next_move(self):#, new_board):
        """
        NOTES:
        If the variable names are confusing, think about them being named when you just call the method.
        
        PRECONDITIONS:
        1)  The board exists and is legal
        """
        
        if self.pre_last_move_state is not None:#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
            index_in_q_array = self.q_array_states[self.pre_last_move_state].index(self.post_last_move_state)
            cur_state = self.get_states_from_boards_spots([self.board.spots])[0]
    
            if self.q_array[cur_state]:#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
                self.q_array[self.pre_last_move_state][index_in_q_array] = self.q_array[self.pre_last_move_state][index_in_q_array] + self.learning_rate * (reward_function(self.state_array[self.pre_last_move_state],self.state_array[cur_state])+ self.discount_factor* max(self.q_array[cur_state]) - self.q_array[self.pre_last_move_state][index_in_q_array])
            else:#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
                self.q_array[self.pre_last_move_state][index_in_q_array] = self.q_array[self.pre_last_move_state][index_in_q_array] + self.learning_rate * (reward_function(self.state_array[self.pre_last_move_state],self.state_array[cur_state])- self.q_array[self.pre_last_move_state][index_in_q_array])
        
        
        self.pre_last_move_state = self.get_states_from_boards_spots([self.board.spots])[0]#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
        
        possible_next_moves = self.board.get_possible_next_moves()
        possible_next_states = self.get_states_from_boards_spots(self.board.get_potential_spots_from_moves(possible_next_moves))
    
        self.post_last_move_state = self.get_desired_transition_between_states(possible_next_states) 
        
        
        
        considered_moves = []
        for j in range(len(possible_next_states)):   #probably optimize this by using built in python functions
            if possible_next_states[j] == self.post_last_move_state:
                considered_moves.append(possible_next_moves[j])
                
                
        """
        I believe with the updated board.is_game_over() I don't need to use this try statement 
        """
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



def is_terminal(board):
    """
    """
    if not board.get_possible_next_moves():
        return True
    return False
    

class Alpha_beta(Player):
    """
    """
    def __init__(self, the_player_id, the_depth, the_board=None):
        self.board = the_board
        self.depth = the_depth
        self.player_id = the_player_id

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        """
        """
        if depth == 0:
            if is_terminal(self.board):
                if get_number_of_pieces_and_kings(self.board.spots, self.player_id) == [0,0]:
                    return float('inf'), None
                elif get_number_of_pieces_and_kings(self.board.spots, not self.player_id) == [0,0]: 
                    return float('-inf'), None
                else:
                    return 0, None
            self_info = get_number_of_pieces_and_kings(self.board.spots, self.player_id)
            opp_info = get_number_of_pieces_and_kings(self.board.spots, not self.player_id)
            return self_info[0] + 2*self_info[1] - (opp_info[0] + 2*opp_info[1]) , None
                
        possible_moves = self.board.get_possible_next_moves()
        potential_spots = self.board.get_potential_spots_from_moves(possible_moves)
        desired_move_index = None
        if maximizing_player:
            v = float('-inf')
            for j in range(len(potential_spots)):
                cur_board = Board.Board(potential_spots[j], not board.player_turn)
                alpha_beta_results = self.alpha_beta(cur_board, depth - 1, alpha, beta, False)
            
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
                cur_board = Board.Board(potential_spots[j], not self.board.player_turn)
                alpha_beta_results = self.alpha_beta(cur_board, depth - 1, alpha, beta, True)

                if v != min(v, alpha_beta_results[0]):
                    v = min(v, alpha_beta_results[0])
                    desired_move_index = j
                    beta = min(beta, v)
                if beta <= alpha:
                    break
            if desired_move_index is None:
                return v, None
            return v, possible_moves[desired_move_index]
    
    def get_next_move(self):
        """
        """
        return self.alpha_beta(self.board, self.depth, float('-inf'), float('inf'), self.player_id)[1]
        


def play_n_games(player1, player2, num_games, move_limit):
    """
    TO-DO:
    1) Add options for returing data about the games

    PRECONDITIONS:
    1) Both players play legal moves only
    """
    game_board = Board.Board()
    player1.set_board(game_board)
    player2.set_board(game_board)
    
    players_move = player1  #############################MAKE SURE THAT PLAYERS_MOVE IS A POINTER NOT BECOMING A COPY OF THAT OBJECT OR POINTER TO WHAT IT'S POINTING TO#################################################
    for j in range(num_games):
        move_counter = 0
        while not game_board.is_game_over() and move_counter < move_limit:
            #game_board.print_board()
            #print(move_counter)
            game_board.make_move(players_move.get_next_move())
            move_counter = move_counter + 1
            if players_move is player1:
                players_move = player2
            else:
                players_move = player1
        else:
            if get_number_of_pieces_and_kings(game_board.spots, True) == [0,0]:
                print("Player 2 won game #" + str(j + 1) + " in " + str(move_counter) + " turns!")
            elif get_number_of_pieces_and_kings(game_board.spots, False) == [0,0]:
                print("Player 1 won game #" + str(j + 1) + " in " + str(move_counter) + " turns!")
            else:
                print("Tie game for game #" + str(j + 1) + " in " + str(move_counter) + " turns!")
            game_board.print_board()
            game_board.wipe_board()
    




LEARNING_RATE = .05  #properly pick this
DISCOUNT_FACTOR = .3
NUM_GAMES_TO_TRAIN = 10
NUM_GAMES_TO_TEST = 20
TRAINING_RANDOM_MOVE_PROBABILITY = .1
ALPHA_BETA_DEPTH = 1
TRAINING_MOVE_LIMIT = 500
TESTING_MOVE_LIMIT = 1000
PLAYER1 = Q_Learning_AI(True, LEARNING_RATE, DISCOUNT_FACTOR, TRAINING_RANDOM_MOVE_PROBABILITY)
PLAYER2 = Alpha_beta(False, ALPHA_BETA_DEPTH)


play_n_games(PLAYER1, PLAYER2, NUM_GAMES_TO_TRAIN, TRAINING_MOVE_LIMIT)
print(PLAYER1.get_q_array_info())

PLAYER1.set_random_move_probability(0)

play_n_games(PLAYER1, PLAYER2, NUM_GAMES_TO_TEST, TESTING_MOVE_LIMIT)
print(PLAYER1.get_q_array_info())
