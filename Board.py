"""
@author: Sam Ragusa

NOTES:
-Should store moves as array of locations e.g.: [[x1,y1],[x2,y2],[x3,y3]]
which is showing the piece at [x1,x2] goes to [x2,y2] then [x3,y3] as one move
-0 is empty spot, 1 is p1, 2 is p2, 3 is p1 king, 4 is p2 king
-if self.player_turn == True then it is player 1's turn
"""


import math, random, copy, time



"""
The class for the game board for 8x8 checkers
"""
class Board:
    
    BACKWARDS_PLAYER = 2
    EMPTY_SPOT = 0
    P1 = 1
    P2 = 2
    P1_K = 3
    P2_K = 4
    
    
    def __init__(self, old_spots=None, the_player_turn=True): #maybe have default parameter so board is 8x8 by default but nxn if wanted
        self.player_turn = the_player_turn 
        if old_spots is None:   
            self.spots = [[j,j,j,j] for j in [1,1,1,0,0,2,2,2]]
        else:
            self.spots = old_spots


    def wipe_board(self):
        self = Board()

    
    def is_game_over(self):
        p1_piece = False
        p2_piece = False
        for row in self.spots:
            for element in row:
                if not p1_piece and (element == 1 or element == 3):
                    p1_piece = True
                    if p2_piece:
                        return False
                if not p2_piece and (element == 2 or element == 4):
                    p2_piece = True
                    if p1_piece:
                        return False
        return True


    def not_spot(self, loc):
        if len(loc) == 0 or loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 3:
            return True
        return False
    
    
    def get_spot_info(self, loc):
        return self.spots[int(loc[0])][int(loc[1])] #not sure about the int()'s
    
    
    """
    see's if there is a piece at that spot who's turn it is
    
    NOTE:
    DON'T THINK I NEED ANYMORE, NOT CURRENTLY USED
    """
    def is_players_turn(self, spot_data):  #might want to make not need this function
        if self.player_turn == True:
            if spot_data == self.P1 or spot_data == self.P1_K:
                return True
            else:
                return False
        else:
            if spot_data == self.P2 or spot_data == self.P2_K:
                return True
            else:
                return False
    
    
    """
    NOTE: REALLY DON'T THINK I NEED, NOT CURRENTLY USED
    """
    def are_same_players(self, location1, location2):
        if self.spots[location1[0]][location1[1]] == self.spots[location2[0]][location2[1]]:
            return True
        return False
    
    
    def forward_n_locations(self, start_loc, n, backwards=False):
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
    

    """
    NOTES:
    -NEED TO MAKE SURE WORKS
    
    PRE-CONDITION:
    -start_loc is a location with a players piece
    """
    def get_simple_moves(self, start_loc):
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
                if self.spots[int(location[0])][int(location[1])] == self.EMPTY_SPOT:   ##DO NOT KNOW IF int() ARE NEEDED
                    possible_next_locations.append(location)
            
        return [[start_loc, end_spot] for end_spot in possible_next_locations]      
                
    def get_capture_moves(self, start_loc, move_beginnings=None):
        if move_beginnings is None:
            move_beginnings = [start_loc]

        answer = []
        
        if self.spots[int(start_loc[0])][int(start_loc[1])] > 2:  #not sure about the int()'s
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc,2)
            next1.extend(self.forward_n_locations(start_loc, 1, True))
            next2.extend(self.forward_n_locations(start_loc, 2, True))
        elif self.spots[int(start_loc[0])][int(start_loc[1])] == self.BACKWARDS_PLAYER:#not sure about the int()'s
            next1 = self.forward_n_locations(start_loc, 1, True)
            next2 = self.forward_n_locations(start_loc,2, True)
        else:
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc,2)
            
        for j in range(len(next1)):
            if (not self.not_spot(next2[j])) and (not self.not_spot(next1[j])) : #if both spots exist
                if self.get_spot_info(next1[j]) != 0 and self.get_spot_info(next1[j])%2 != self.get_spot_info(start_loc)%2:  #if next spot is opponent
                    if self.get_spot_info(next2[j]) == 0:  #if next next spot is empty
                        temp_move1 = move_beginnings
                        temp_move1.append(next2[j])
                        temp_move2 = [start_loc, next2[j]]

                        answer.append(temp_move1)

                        if self.get_spot_info(start_loc)!=1 or next2[j][0] != 7:
                            if self.get_spot_info(start_loc)!=2 or next2[j][0] != 0: 
                                temp_board = Board(copy.deepcopy(self.spots), copy.deepcopy(self.player_turn))
                                temp_board.make_move(temp_move2, False)
                                answer.extend(temp_board.get_capture_moves(temp_move2[1], temp_move1))
        return answer
    
    
    def get_possible_next_moves(self):        
        answer = []
        for j in range(8):
            for i in range(4):
                if (self.player_turn == True and (self.spots[j][i]== self.P1 or self.spots[j][i]== self.P1_K)) or (self.player_turn == False and (self.spots[j][i]== self.P2 or self.spots[j][i]== self.P2_K)):
                    answer.extend(self.get_simple_moves([j, i]))
                    answer.extend(self.get_capture_moves([j, i]))
        
        return answer
    
    
    def make_move(self, move, switch_player_turn=True):
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
                        
                self.spots[int((move[j][0] + move[j+1][0])/2)][int(middle_y)] = self.EMPTY_SPOT #not sure about the int()'s 
                
                
        self.spots[int(move[len(move)-1][0])][int(move[len(move)-1][1])] = int(self.spots[int(move[0][0])][int(move[0][1])])   #not sure about the int()'s
        if int(move[len(move)-1][0]) == 7 and self.spots[int(move[len(move)-1][0])][int(move[len(move)-1][1])] == self.P1:
            self.spots[int(move[len(move)-1][0])][int(move[len(move)-1][1])] = self.P1_K
        elif int(move[len(move)-1][0]) == 0 and self.spots[int(move[len(move)-1][0])][int(move[len(move)-1][1])] == self.P2:
            self.spots[int(move[len(move)-1][0])][int(move[len(move)-1][1])] = self.P2_K
        else:
            self.spots[int(move[len(move)-1][0])][int(move[len(move)-1][1])] = self.spots[int(move[0][0])][int(move[0][1])]   #not sure about the int()'s
        self.spots[int(move[0][0])][int(move[0][1])] = self.EMPTY_SPOT   #not sure about the int()'s
                
        if switch_player_turn:
            self.player_turn = not self.player_turn
       
        
    """
    Get's the potential spots of the board if it makes the move given.
    """
    def get_potential_spots_from_move(self, move):
        original_spots = copy.deepcopy(self.spots)
        self.make_move(move, switch_player_turn=False)
        answer = copy.deepcopy(self.spots)
        self.spots = original_spots
        return answer
        
    
    """
    Gets the symbol for what should be at a board location.
    
    NOTE:
    -Should probably make this into a switch statement
    """
    def get_symbol(self, location):
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
        slist = ["".join(map(str,self.spots[j])) for j in range(8)]
        return str(self.player_turn) + ":" + "".join(slist)
    
    
    def print_board(self):
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

        
    """
    OPTOMIZATION:
    -this looks like it should be high priority in optomization
    """
def get_board_from_string(string):
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



def make_random_move(board):

    possible_moves = board.get_possible_next_moves()
    if len(possible_moves) == 0:
        return False
    rand_move = possible_moves[random.randint(0,len(possible_moves)-1)]
    board.make_move(rand_move)
    return True





test = Board()

all_states = get_possible_states(test.get_small_string_for_board())
print(len(all_states))


