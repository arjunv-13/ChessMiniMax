# Chess Engine
## Overview
I created a Chess Engine using a Minimax algorithm and the Python-Chess library along with alpha-beta pruning, move ordering, capture quiescence search, and a custom evaluation function for each stage of the game. It permits both engine vs. engine and player vs. engine games.

During this project, I explored data structures like trees, hash maps, and numpy arrays along with algorithmic techniques like recursion, DFS, and minimax. I really enjoyed starting with a basic minimax algorithm and implementing various modifications to improve speed and performance.

## Usage
To play a game against the engine, run game.py.

To watch the engine play against itself in real time, run selfPlay.py.

To wait for the engine to play a whole game against itself before watching it at a reasonable speed, use selfPlayDelay.py.

For all of these, the board will show up in a Pygame window. However, at this time, inputting moves when playing against the engine requires using the Terminal. Use standard algebraic notation, like Nf3 or Rad1 if there are multiple rooks that can access d1. In the future, I hope to add drag-and-drop functionality to the game window so that the game can be played completely in a GUI.

## Components

### Game, SelfPlay, and SelfPlayDelay

All of these just synthesize the functions from various other files into a cohesive program to be run. They also create the Pygame window and get user input.

### Engine

The important function is the search function. This is what implements the alpha-beta pruning minimax algorithm.

It creates a tree using the move object/children class and a recursive DFS search. It does this until it gets to the normal depth max. 

Once there, it implements a "capture quiescence search" to ensure that the position is not being misevaluated.

Otherwise, the horizon effect may occur, where the search at a normal depth might end at a position which is highly unstable. For example, if the queens are in the middle of being traded, and the search stops, then that position would be incorrectly evaluated. As a result, until the max capture search depth is released, the search continues only for capture moves.

One important note is that the engine evaluates the position with the capture and without the capture to ensure that it does not misevaluate positions where all captures are bad.

Then once max capture search depth is reached, the leaf nodes have their board state evaluation calculated directly via the evaluation functions. The parent nodes then use the minimax function to set their own evaluation.

The alpha beta pruning method is also augmented by a move ordering function. This searches captures and checks first to fully capitalize on the alpha beta search optimization. These "special moves" are more likely to result in better positions and thus can maximize the pruning that occurs.

The findBestMove function combines all of this to take the evaluation of every legal move in the position and select the best move (depending on color, the min or max evaluation). However, to ensure that the same game is not played again and again when the engine plays itself, it tolerates a set variance, where it selects randomly from moves that have an evaluation within a difference of the chosen variance.

### evalOpening, evalMiddlegame, and evalOpening

These files implement the evaluation of leaf node board states depending on how many pieces are on the board and how many moves have occurred.

They take in a board, isolate where pieces are, and then use a numpy array to determine piece value based on location.

In the opening, importance is placed on central pawn play and development of minor pieces.

In the middlegame, importance is placed on positioning pieces on strong squares and king safety.

In the endgame, pawn advancement becomes extremely important while king safety is lessened in importance. One trouble is how to implement values in the endgame when piece locations are unpredictable. This is why search depth is increased because less moves are possible (and so higher depth is more feasible) and to enable longer-term planning.

### Board

This is where the pygame display is implemented with two key functions: drawWindow and drawPieces.

drawWindow is the same every time: a 64 square tiled board is shown to fit most of the window.

drawPieces takes in a board state and uses the chessPieces photos to place pieces in the correct position.

### chessPieces

Here, we have a library of all the pieces for both colors and a library of sounds to be played during moves like captures, casles, checks, and normal moves.

### noTreeEngine (Work In Progress)

Here, I try to see if a purely recursive approach as opposed to a tree class is more efficient. However, this is still a work in progress and does not work completely yet.

## Future Work

I am proud of what the engine is able to do so far, but I would still like to implement the following features/updates in future iterations.

1. Endgame Tablebase - since chess is solved for positions with 7 pieces or less, importing such a library (or a reduced version with less pieces to save space) and using those suggested moves would drastically improve endgame play. For example, the current engine is simply unable to mate with a bishop and a knight while the tablebase would enable that without drastic search time costs.

2. One inefficiency is that the engine may evaluate the same position twice in different branches of the tree via different move orderings. Repeating evaluation is wasteful. As a result, storing evaluations so far in some sort of hash table might improve speed.

3. As mentioned before, I would like to create an interactive board with drag-and-drop functionality instead of using the terminal to implement player moves. This is a quality-of-life improvement.

4. In order to test my bot against a wider audience and get an actual rating, concecting to lichess.com's bot feature and receiving an ELO would be very cool.

5. I would like to practice other languages and see how to implement a similar engine in a lower-level language like C++ to improve speed and performance.

6. Right now, the evaluation functions are hand-crafted by me and rudimentary. Implementing some sort of neural network evaluation function could be a great improvement so that the evaluation is more flexible and accurate. I could train it on Stockfish's evaluations to mirror the best chess engine in the world.

## Thank You

Thank you for reading all the way! I hope you enjoyed!