## Synopsis

This code defines a checkers board, and the ability to officiate a game of checkers between two AI which are playing using the rules I played with as a child, which are the same as traditional American Checkers (English Droughts), except that a win can only be achieved by capturing all of the opponents pieces.  Two AI are defined to compete in checkers, one based in reinforcement learning and one in alpha-beta pruning.  


## Alpha-Beta Pruning AI

This AI uses a traditional alpha-beta pruning algorithm (with specified depth), where the value of a potential future board configuration is infinity for a winning game, -infinity for a losing game, and given by the following equation for any other board configuration:

<!---
value=\Delta\hspace{1pt}U_s-\Delta\hspace{1pt}U_o+2(\Delta\hspace{1pt}K_s-\Delta\hspace{1pt}K_o)
-->

![equation](http://latex.codecogs.com/svg.latex?value%3D%5CDelta%5Chspace%7B1pt%7DU_s-%5CDelta%5Chspace%7B1pt%7DU_o%2B2%28%5CDelta%5Chspace%7B1pt%7DK_s-%5CDelta%5Chspace%7B1pt%7DK_o%29)

In the above equation, U and K represent the number of uncrowned pieces and number of kings a player has, and their subscripts s and o indicate if the player is itself or it's opponent respectively.  The delta refers to the change in the value following it between the current board configuration and the potential board configuration the AI is considering.   


## Reinforcement Learning AI

The reinforcement learning AI is based in the ideas of Q-learning.  Since creating and training a Q-table for every possible board configuration takes immense computational power, a set of characteristics defining a set of states was created such that each board configuration exists in one and only one of these states.


#### State Characteristics

The characteristics of the states are as follows:

1. Number of own uncrowned pieces
2. Number of opponent uncrowned pieces
3. Number of own kings
4. Number of opponent kings
5. Number of own pieces (crowned and uncrowned) on left and right edges of board
6. Integer value of own vertical center of mass
7. Integer value of opponent vertical center of mass

For characteristics 6 and 7, the center of mass is calculated with an uncrowned piece having the same mass as a king.


#### Dynamically Discovering Transitions

Since knowing the state of a board is not enough information to figure out it's possible transitions to other states, initializing a traditional Q-Table is not possible, and if it were, would require a very large amount of memory.  With this in mind I instead dynamically create/discover a set of possible transitions between states during training, which I store as keys in a dictionary.

<!---
NOTE:
May want to specify what the values corresponding to the keys represent.
-->   

#### Updating Transition Values

<!---
STUFF FOR EQUATATIONS
http://www.url-encode-decode.com/
http://dillinger.io/
-->

There are two formulas used to update the value of a transition between two states.  In these formulas T(state1, state2) is the learned scalar value for transitioning from state1 to state2, R is the scalar rewards function between two states (same as described for the alpha-beta pruning AI), alpha is the learning rate, and lambda is the discount rate.  

<!---
T(s_n,s_{n+1})\leftarrow\hspace{1pt}T(s_n,s_{n+1})+\alpha(R(s_n,s_{n+2})+\lambda\max\limits_m(T(s_{n+2},s_m))-T(s_n,s_{n+1}))
-->

Directly preceding the AI's turn, if it has already moved at least once this game and the game board is not terminal, then the following value update is used:

![equation](http://latex.codecogs.com/svg.latex?T%28s_n%2Cs_%7Bn%2B1%7D%29%5Cleftarrow%5Chspace%7B1pt%7DT%28s_n%2Cs_%7Bn%2B1%7D%29%2B%5Calpha%28R%28s_n%2Cs_%7Bn%2B2%7D%29%2B%5Clambda%5Cmax%5Climits_m%28T%28s_%7Bn%2B2%7D%2Cs_m%29%29-T%28s_n%2Cs_%7Bn%2B1%7D%29%29)

<!---
T(s_n,s_{n+1})\leftarrow\hspace{1pt}T(s_n,s_{n+1})+\alpha(R(s_n,s_{n+2}))
-->

If the game board is terminal, then the AI will be notified and will apply the following value update:

![equation](http://latex.codecogs.com/svg.latex?T%28s_n%2Cs_%7Bn%2B1%7D%29%5Cleftarrow%5Chspace%7B1pt%7DT%28s_n%2Cs_%7Bn%2B1%7D%29%2B%5Calpha%28R%28s_n%2Cs_%7Bn%2B2%7D%29%29)


#### Picking Moves

When it is the reinforcement learning AI's turn, it looks at a list of possible moves it could make, and if their respective state transitions are not yet known, it adds them to the dictionary of transitions.  Then it will chose to do one of two things, based on a specified probability.  The first is that it could chose a move at random, this is used during training so that transitions other then the current highest valued transition will still be trained.  If the learning AI does not move randomly, it will chose the move who's state transition has the highest value associated with it.
