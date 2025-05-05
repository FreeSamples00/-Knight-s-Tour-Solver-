# The Knight's Tour

## Overview
This is a program that finds a viable [Knight's tour](https://en.wikipedia.org/wiki/Knight%27s_tour) given a starting location. A Knight's tour is a series of moves by the knight piece in chess which will allow it to visit every available location on a cess board.



## Implementation

The [solver.py](./solver.py) file contains logic for finding a tour. 

The class `ChessBoard` contains the state of the board and methods to manipulate the knight. All board locations are in chess notation (i.e. `e4` or `a2`).

The `solve_knight_tour()` function recursively searches for a viable tour, using *Warnsdorff’s heuristic* for efficiency. 

Additionally `visualize_tour()` provides a fun visualization given the completed tour.

I have also included the ability to pre-load the chessboard with obstructions (other pieces or danger areas) which the tour will not visit. These are represented as already visited cells within the data structure.



## Use

The [main.py](./main.py) file contains a command line interface for using this program.



`py main.py <init_location> <occupied_spaces>`

- `py` python3 or your preference of python interpreter.
- `main.py` the CLI file we want to use.
- `<init_location>` The location to initially place the knight before the search begins. (ex: `e4`)
- `<occupied_spaces>` The locations you would like the tour to avoid visiting, space separated in chess notation. (ex: `a4` `b3` `c8`)



An example run of this program would look like this: `python3 main.py e4 b2 f6` Where `e4` is the starting location, and `b2`, `f6` will not be visited by the tour.



This CLI will also place various runtime stats into `stats.txt`, including the actual tour path.