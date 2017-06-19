"""
@author: Sam Ragusa

IMPORTANT NOTE:
-Since I am currently executing the AI checkers games from the file AI.py,
the code at the end of that file needs to be commented out before execution of these tests.  This includes all code that is not defining functions, or classes. 
"""


from Board import Board
from AI import Alpha_beta


def switch_board_players(board):
    """
    Switches the player associated with each piece on the board,
    and the player who's move it currently is.
    """
    board.player_turn = not board.player_turn
    for row_index in len(board.spots):
        for col_index in len(board.spots[row_index]):
            if board.spots[row_index][col_index] == 1:
                board.spots[row_index][col_index] = 2
            elif board.spots[row_index][col_index] == 2:
                board.spots[row_index][col_index] = 1
            elif board.spots[row_index][col_index] == 3:
                board.spots[row_index][col_index] = 4
            elif board.spots[row_index][col_index] == 4:
                board.spots[row_index][col_index] = 3
    


def print_test_results(computed_outputs, desired_outputs, correctness_function=lambda a,b : a==b):
    """
    Prints the results of a test given the computed outputs, and the desired outputs (and
    if desired a correctness function comparing the outputs as equal or not).  It displays
    failed tests in an easy to understand way, and won't bother you with all the passed tests.
    """
    output_correctness = list(map(correctness_function, desired_outputs, computed_outputs))
    
    has_failed_test = False
    for j in range(len(output_correctness)):
        if not output_correctness[j]:
            print("Test number " + str(j+1) + " failed.")
            print("Calculated output: " + str(computed_outputs[j]))
            print("Desired output:  " + str(desired_outputs[j]))
            print("")
            has_failed_test = True
    
    if has_failed_test == False:
        print("All tests passed.")

def test_possible_next_moves(test_inputs, desired_outputs):
    """
    Checks that the Board classes get_possible_next_moves method works properly
    by testing it against a specifically chosen set of test cases.  It reverses the players
    in each test case and then tests that the move outputs are the same.
    """
    
    test_boards = [Board(the_player_turn=False) for j in range(len(test_inputs))]
    
    for j in range(len(test_boards)):
        test_boards[j].empty_board()
        test_boards[j].insert_pieces(test_inputs[j])
    
    computed_outputs = [test_board.get_possible_next_moves() for test_board in test_boards]
    
    print_test_results(computed_outputs, desired_outputs)
    
    map(switch_board_players, test_boards)
    
    computed_outputs = [test_board.get_possible_next_moves() for test_board in test_boards]
     
    print_test_results(computed_outputs, desired_outputs)
     
def test_alpha_beta_ai(test_inputs, desired_outputs):
    """
    Checks that the alpha-beta pruning AI is functioning properly by computing
    the desired move for a few different implementations of alpha-beta pruning (different depths),
    and comparing it to the desired move to be outputted. 
    
    
    $$$$$$$$$$$MAYBE TEST BACKWARDS$$$$$$$$$$$$$$$$$$$$$
    """
    
    test_boards = [Board(the_player_turn=False) for j in range(len(test_inputs))]

    for j in range(len(test_boards)):
        test_boards[j].empty_board()
        test_boards[j].insert_pieces(test_inputs[j])
    
    alpha_betas = {
    1 : Alpha_beta(False, 1),
    2 : Alpha_beta(False, 2),
    4 : Alpha_beta(False, 4)
    }

    move_getter_instructions = [[1,2],[2],[2],[4],[1,2],[2,4],[2]]

    computed_outputs = []
    for board, instructions in zip(test_boards,move_getter_instructions):
        for instruction in instructions:
            alpha_betas.get(instruction).set_board(board)
            computed_outputs.append(alpha_betas.get(instruction).get_next_move())

    print_test_results(computed_outputs, desired_outputs)


def test_board_functions_not_next_move():
    """
    Tests the methods in the Board class excluding the possible_next_moves method.
    Makes moves and sees if the final board configuration is correct.
    Has an alpha-beta pruning AI look for it's next move throughout to make
    sure some methods of Board would not alter the Board configuration.
    
    $$$$$$$$$$$$$$$$$DO IN REVERSE$$$$$$$$$$$$$$$$$$
    """
    
    old_spots = [[1,4,1,1],[1,0,1,1],[1,1,0,1],[0,0,0,0],[0,0,0,0],[0,1,2,2],[2,2,2,2],[2,2,2,2]]
    

    
    board = Board()
    
    #Make sure some Board methods don't alter the board
    alpha_beta_ai = Alpha_beta(False, 6)
    alpha_beta_ai.set_board(board)
    
    alpha_beta_ai.get_next_move()
    board.make_move([[2,0],[3,0]])
    board.make_move([[5,0],[4,1]])
    alpha_beta_ai.get_next_move()
    board.make_move([[2,2],[3,1]])
    board.make_move([[1,0],[2,0]])
    alpha_beta_ai.get_next_move()
    board.make_move([[0,1],[1,0]])
    board.make_move([[4,1],[2,2],[0,1]])
    alpha_beta_ai.get_next_move()
    board.make_move([[5,1],[4,1]])
    board.make_move([[3,0],[5,1]])
    alpha_beta_ai.get_next_move()

    if board.spots == old_spots:
        print("All tests passed.")
    else:
        print("Test failed.")
        print_test_results([board.spots],[old_spots])


next_move_inputs = []
next_move_inputs.append([[4,1,1],[4,2,1],[5,1,2]])
next_move_inputs.append([[3,2,1],[5,2,1],[6,1,2]])
next_move_inputs.append([[4,2,1],[5,3,2],[6,0,2]])
next_move_inputs.append([[2,3,1],[4,1,1],[4,3,1],[5,0,2],[5,3,2]])
next_move_inputs.append([[2,1,1],[4,2,2],[6,1,2]])
next_move_inputs.append([[3,0,2],[4,0,4],[5,0,2]])
next_move_inputs.append([[3,3,1],[5,1,2],[6,1,2]])
next_move_inputs.append([[2,1,1],[5,0,2],[5,1,2],[6,1,2]])
next_move_inputs.append([[1,0,1],[1,1,1],[3,0,1],[3,1,3],[3,2,3],[5,0,1],[5,1,1],[5,2,1],[6,0,2]])
next_move_inputs.append([[2,1,1],[2,2,3],[3,1,4],[4,1,1],[4,2,3],[7,1,1]])
next_move_inputs.append([[2,1,1],[2,2,3],[3,1,2],[4,1,1],[4,2,3],[7,1,1]])
#next_move_inputs.append([[1,0,1],[1,1,1],[3,0,1],[3,1,3],[3,2,3],[5,0,1],[5,1,1],[5,2,1],[6,0,4]])   commented this out because calculating it's desired output by hand takes more time than I have right now
next_move_inputs.append([[2,2,1],[4,0,4]])
    
next_move_outputs = []
next_move_outputs.append([[[5,1],[3,2]],[[5,1],[3,0]]])
next_move_outputs.append([[[6,1],[5,1]],[[6,1],[5,0]]])
next_move_outputs.append([[[5,3],[4,3]],[[6,0],[5,0]]])
next_move_outputs.append([[[5,0],[3,1]],[[5,3],[3,2],[1,3]]])
next_move_outputs.append([[[4,2],[3,2]],[[4,2],[3,1]],[[6,1],[5,1]],[[6,1],[5,0]]])
next_move_outputs.append([[[3,0],[2,1]],[[3,0],[2,0]],[[5,0],[4,1]]])
next_move_outputs.append([[[5,1],[4,2]],[[5,1],[4,1]],[[6,1],[5,0]]])
next_move_outputs.append([[[5,0],[4,1]],[[5,0],[4,0]],[[5,1],[4,2]],[[5,1],[4,1]]])
next_move_outputs.append([[[6,0],[4,1],[2,2],[0,1]],[[6,0],[4,1],[2,0],[0,1]]])  
next_move_outputs.append([[[3,1],[5,2]],[[3,1],[5,0]],[[3,1],[1,2]],[[3,1],[1,0]]])
next_move_outputs.append([[[3,1],[1,2]],[[3,1],[1,0]]])
#next_move_outputs.append(TOO LONG TO DO RIGHT NOW)
next_move_outputs.append([[[4,0],[5,0]],[[4,0],[3,0]]])


alpha_beta_inputs = []
alpha_beta_inputs.append([[1,1,4],[1,3,1],[2,3,3],[3,1,4],[4,3,1],[6,1,1],[6,3,1],[7,1,2],[7,2,4]])
alpha_beta_inputs.append([[2,0,1],[2,1,1],[2,2,3],[2,3,1],[4,1,2],[4,2,2],[4,3,2]])
alpha_beta_inputs.append([[2,1,1],[2,2,3],[2,3,1],[4,0,2],[4,1,2],[4,2,2]])
alpha_beta_inputs.append([[1,2,3],[1,3,3],[5,2,2]])
alpha_beta_inputs.append([[1,1,1],[2,1,2],[4,3,1],[5,2,2]])
alpha_beta_inputs.append([[2,2,1],[4,1,2]])
alpha_beta_inputs.append([[1,0,1],[1,2,1],[3,0,1],[3,3,1],[4,2,1],[5,0,1],[6,0,1],[7,2,3],[7,3,2]])

alpha_beta_outputs = []
alpha_beta_outputs.append([[7,2],[5,3],[3,2]])
alpha_beta_outputs.append([[7,1],[5,0]])
alpha_beta_outputs.append([[4,3],[3,3]])
alpha_beta_outputs.append([[4,1],[3,0]])
alpha_beta_outputs.append([[5,2],[4,3]])
alpha_beta_outputs.append([[2,1],[0,2]])
alpha_beta_outputs.append([[2,1],[0,2]])
alpha_beta_outputs.append([[4,1],[3,0]])
alpha_beta_outputs.append([[4,1],[3,0]])
alpha_beta_outputs.append([[7,3],[6,3]])


print("Board tests:")
test_board_functions_not_next_move() 
print("") 
print("Possible next move tests:")
test_possible_next_moves(next_move_inputs, next_move_outputs)
print("")
print("Alpha-beta Pruning tests:")
test_alpha_beta_ai(alpha_beta_inputs, alpha_beta_outputs)    

  

