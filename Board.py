"""
@author: Sam Ragusa

NOTES:
-Should store moves as array of locations e.g.: [[x1,y1],[x2,y2],[x3,y3]]
which is showing the piece at [x1,x2] goes to [x2,y2] then [x3,y3] as one move
-0 is empty spot, 1 is p1, 2 is p2, 3 is p1 king, 4 is p2 king
-if self.player_turn == True then it is player 1's turn
"""


import math
import copy
import time


class Board:
    """
    A class to represent and play an 8x8 game of checkers.
    """
    
    EMPTY_SPOT = 0
    P1 = 1
    P2 = 2
    P1_K = 3
    P2_K = 4
    BACKWARDS_PLAYER = P2
    
    
    def __init__(self, old_spots=None, the_player_turn=True):
        """
        Initializes a new instance of the Board class.  Unless specified otherwise, 
        the board will be created with a start board configuration.
        
        NOTE:
        Maybe have default parameter so board is 8x8 by default but nxn if wanted.
        """
        self.player_turn = the_player_turn 
        if old_spots is None:   
            self.spots = [[j,j,j,j] for j in [1,1,1,0,0,2,2,2]]
        else:
            self.spots = old_spots


    def wipe_board(self):
        """
        Resets the current configuration of the game board to the original 
        starting position.
        """
        self.spots = copy.deepcopy(Board().spots)
    
    
    def is_game_over(self):
        """
        Finds out and returns weather the game currently being played is over or
        not.
        """
        if not self.get_possible_next_moves():
            return True
        return False


    def not_spot(self, loc):
        """
        Finds out of the spot at the given location is an actual spot on the game board.
        """
        if len(loc) == 0 or loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 3:
            return True
        return False
    
    
    def get_spot_info(self, loc):
        """
        Gets the information about the spot at the given location.
        
        NOTE:
        Might want to not use this for the sake of computational time.
        """
        return self.spots[loc[0]][loc[1]]
    
    
    def forward_n_locations(self, start_loc, n, backwards=False):
        """
        Gets the locations possible for moving a piece from a given location diagonally
        forward (or backwards if wanted) a given number of times(without directional change midway).  
        """
        if n % 2 == 0:
            temp1 = 0
            temp2 = 0
        elif start_loc[0] % 2 == 0:
            temp1 = 0
            temp2 = 1 
        else:
            temp1 = 1
            temp2 = 0

        answer = [[start_loc[0], start_loc[1] + math.floor(n / 2) + temp1], [start_loc[0], start_loc[1] - math.floor(n / 2) - temp2]]

        if backwards: 
            answer[0][0] = answer[0][0] - n
            answer[1][0] = answer[1][0] - n
        else:
            answer[0][0] = answer[0][0] + n
            answer[1][0] = answer[1][0] + n

        if self.not_spot(answer[0]):
            answer[0] = []
        if self.not_spot(answer[1]):
            answer[1] = []
            
        return answer
    

    def get_simple_moves(self, start_loc):
        """    
        Gets the possible moves a piece can make given that it does not capture any opponents pieces.
        
        PRE-CONDITION:
        -start_loc is a location with a players piece
        """
        if self.spots[start_loc[0]][start_loc[1]] > 2:
            next_locations = self.forward_n_locations(start_loc, 1)
            next_locations.extend(self.forward_n_locations(start_loc, 1, True))
        elif self.spots[start_loc[0]][start_loc[1]] == self.BACKWARDS_PLAYER:
            next_locations = self.forward_n_locations(start_loc, 1, True)  #Switched the true from the statement below
        else:
            next_locations = self.forward_n_locations(start_loc, 1)
        

        possible_next_locations = []

        for location in next_locations:
            if len(location) != 0:
                if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
                    possible_next_locations.append(location)
            
        return [[start_loc, end_spot] for end_spot in possible_next_locations]      
                
    def get_capture_moves(self, start_loc, move_beginnings=None):
        """
        Recursively get all of the possible moves for a piece which involve capturing an opponent's piece.
        """
        if move_beginnings is None:
            move_beginnings = [start_loc]

        answer = []
        if self.spots[start_loc[0]][start_loc[1]] > 2:  
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc,2)
            next1.extend(self.forward_n_locations(start_loc, 1, True))
            next2.extend(self.forward_n_locations(start_loc, 2, True))
        elif self.spots[start_loc[0]][start_loc[1]] == self.BACKWARDS_PLAYER:
            next1 = self.forward_n_locations(start_loc, 1, True)
            next2 = self.forward_n_locations(start_loc,2, True)
        else:
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc,2)
        
        
        answer_length = 0
        for j in range(len(next1)):
            if (not self.not_spot(next2[j])) and (not self.not_spot(next1[j])) : #if both spots exist
                if self.get_spot_info(next1[j]) != 0 and self.get_spot_info(next1[j])%2 != self.get_spot_info(start_loc)%2:  #if next spot is opponent
                    if self.get_spot_info(next2[j]) == 0:  #if next next spot is empty
                        temp_move1 = move_beginnings
                        temp_move1.append(next2[j])
                        temp_move2 = [start_loc, next2[j]]

                        #answer.append(temp_move1)
                        
                        answer_length = len(answer)
                        
                        
                        if self.get_spot_info(start_loc)!=1 or next2[j][0] != 7:
                            if self.get_spot_info(start_loc)!=2 or next2[j][0] != 0: 
                                temp_board = Board(copy.deepcopy(self.spots), copy.deepcopy(self.player_turn))
                                temp_board.make_move(temp_move2, False)
                                answer.extend(temp_board.get_capture_moves(temp_move2[1], temp_move1))
                                
                        if len(answer) == answer_length:
                            answer.append(temp_move1)
                            
        return answer
    
    
    def get_possible_next_moves(self):
        """
        Gets the possible moves that can be made from the current board configuration.
        """
        simple_moves = []        
        capture_moves = []

        for j in range(8):
            for i in range(4):
                if (self.player_turn == True and (self.spots[j][i] == self.P1 or self.spots[j][i] == self.P1_K)) or (self.player_turn == False and (self.spots[j][i] == self.P2 or self.spots[j][i] == self.P2_K)):
                    if len(capture_moves) == 0:
                        simple_moves.extend(self.get_simple_moves([j, i]))
                        
                    capture_moves.extend(self.get_capture_moves([j, i]))
        
        if len(capture_moves) != 0:
            return capture_moves
        return simple_moves
    
    
    def make_move(self, move, switch_player_turn=True):
        """
        Makes a given move on the board, and (as long as is wanted) switches the indicator for
        which players turn it is.
        """
        if abs(move[0][0] - move[1][0]) == 2:
            for j in range(len(move)-1):
                if move[j][0]%2 == 1:
                    if move[j+1][1] < move[j][1]:
                        middle_y = move[j][1]
                    else:
                        middle_y = move[j+1][1]
                else:
                    if move[j+1][1] < move[j][1]:
                        middle_y = move[j+1][1]
                    else:
                        middle_y = move[j][1]
                        
                self.spots[int((move[j][0] + move[j+1][0])/2)][middle_y] = self.EMPTY_SPOT
                
                
        self.spots[move[len(move)-1][0]][move[len(move)-1][1]] = self.spots[move[0][0]][move[0][1]]
        if move[len(move)-1][0] == 7 and self.spots[move[len(move)-1][0]][move[len(move)-1][1]] == self.P1:
            self.spots[move[len(move)-1][0]][move[len(move)-1][1]] = self.P1_K
        elif move[len(move)-1][0] == 0 and self.spots[move[len(move)-1][0]][move[len(move)-1][1]] == self.P2:
            self.spots[move[len(move)-1][0]][move[len(move)-1][1]] = self.P2_K
        else:
            self.spots[move[len(move)-1][0]][move[len(move)-1][1]] = self.spots[move[0][0]][move[0][1]]
        self.spots[move[0][0]][move[0][1]] = self.EMPTY_SPOT
                
        if switch_player_turn:
            self.player_turn = not self.player_turn
       
        
    def get_potential_spots_from_moves(self, moves):
        """
        Get's the potential spots for the board if it makes any of the given moves.
        If moves is None then returns it's own current spots.
        """
        if moves is None:
            return self.spots
        answer = []
        for move in moves:
            original_spots = copy.deepcopy(self.spots)
            self.make_move(move, switch_player_turn=False)
            answer.append(copy.deepcopy(self.spots))  # or this one
            self.spots = copy.deepcopy(original_spots)##########################################DON'T THINK THIS DEEPCOPY IS NEEDED
        return answer
        
    
    def get_symbol(self, location):
        """
        Gets the symbol for what should be at a board location.
        """
        if self.spots[location[0]][location[1]] == 0:
            return " "
        elif self.spots[location[0]][location[1]] == 1:
            return "o"
        elif self.spots[location[0]][location[1]] == 2:
            return "x"
        elif self.spots[location[0]][location[1]] == 3:
            return "O"
        else:
            return "X"
    

    def get_small_string_for_board(self):
        """
        No longer in use.
        """
        slist = ["".join(map(str,self.spots[j])) for j in range(8)]
        return str(self.player_turn) + ":" + "".join(slist)
    
    
    def print_board(self):
        """
        Prints a string representation of the current game board.
        """
        norm_line = "|---|---|---|---|---|---|---|---|"
        print(norm_line)
        for j in range(8):
            if j%2==1:
                temp_line = "|///|"
            else:
                temp_line = "|"
            for i in range(4):
                temp_line = temp_line + " " + self.get_symbol([j,i]) + " |"
                if i!=3 or j%2!=1:
                    temp_line = temp_line + "///|"
            print(temp_line)
            print(norm_line)            

        
def get_board_from_string(string):
    """
    No longer in use.
    """
    answer = []
    if len(string) == 37:
        spot_info = map(int, list(string[5:]))
        for j in range(8):
            answer.append(spot_info[j*4:j*4+4])
        return Board(answer, True)
    else:
        spot_info = map(int, list(string[6:]))
        for j in range(8):
            answer.append(spot_info[j*4:j*4+4])
        return Board(answer, False)


def get_possible_states(start_board_string):
    """
    Starts from a traditional start position for the Checkers board, and gets a full list
    of achievable states (configurations of the board) from the start state.
    
    IMPORTANT NOTE: Computational time is FAR too large, 
    so the use of this function is currently not possible.
    """
    start_time = time.time()
    to_connect = [start_board_string]
    connected = []
    while len(to_connect) != 0: 
        cur_board = get_board_from_string(to_connect.pop())
        connected.append(cur_board.get_small_string_for_board())
        possible_next_moves = cur_board.get_possible_next_moves()
        possible_next_boards = []
        for move in possible_next_moves:
            temp_board = Board(copy.deepcopy(cur_board.spots), copy.deepcopy(cur_board.player_turn))
            temp_board.make_move(move)
            possible_next_boards.append(temp_board.get_small_string_for_board())
            for j in range(len(possible_next_boards)):
                temp_board_string = possible_next_boards[j]
                if temp_board_string not in to_connect:
                    if temp_board_string not in connected:
                        to_connect.append(possible_next_boards[j])
   
        if len(connected)%2500==0:
            print("len(connected): " + str(len(connected)) + "   len(to_connect): " + str(len(to_connect)) + "     time since execution: " + str(time.time() - start_time))
    return connected

