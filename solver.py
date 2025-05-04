class ChessBoard:
    """Class that abstracts the inner workings of a chess board and a knight's movement"""

    # board coordinate information
    COLS = tuple("abcdefgh")
    ROWS = tuple("12345678")

    def __init__(self, knight_loc: str=None, occupied: list[str]=None):
        """Initialize chessboard object
        Args:
            knight_loc (str): starting location of knight (chess notation)
            occupied (list[str]): cells the knight cannot visit on it's tour
        """

        # intialize board
        self.board = {}
        for row in ChessBoard.ROWS:
            for col in ChessBoard.COLS:
                self.board[f"{col}{row}"] = 0
        self.knight = ""
        self.move_list = []

        # add occupied spaces if applicable
        if occupied is not None:
            for loc in occupied:
                loc = loc.lower()
                assert loc[0] not in ChessBoard.ROWS, f"loc: '{loc}'. {loc[0]} out of column bounds (from occupied)"
                assert loc[1] not in ChessBoard.COLS, f"loc: '{loc}'. {loc[1]} out of row bounds (from occupied)"
                self.board[loc] = 1

        # set knight location
        if knight_loc is not None:
            if not self.visit(knight_loc, legal_check=False):
                raise ValueError(f"Inital location and occupied conflict: {knight_loc}")
            
        self.start_loc = self.knight
            
    def complete(self) -> bool:
        """Checks if the knight has completed a tour"""

        # check all cells, return false if not visited
        for cell in self.board.keys():
            if self.board[cell] == 0 and self.knight != cell: # checks if cell has been visited, or if knight is there
                return False
            
        # return true if all cells have been visited
        return True

    def visited(self, loc: str) -> bool:
        """Checks if a cell has been visited yet
        Args:
            loc (str): cell to check, formatted 'e4'
        """

        # cleaning and error checking
        loc = loc.lower()
        assert loc[0] not in ChessBoard.ROWS, f"loc: '{loc}'. {loc[0]} out of column bounds (from visited)"
        assert loc[1] not in ChessBoard.COLS, f"loc: '{loc}'. {loc[1]} out of row bounds (from visited)"

        # actual comparison
        return self.board[loc] == 1
    
    def visit(self, loc: str, legal_check: bool=True) -> bool:
        """Moves the knight to cell, updates visits
        Args:
            loc (str): cell to move to (chess notation)
            legal_check (bool): Whether or not to check if the move is legal, turned off during initialization
        Returns:
            bool: if the move was successful / legal
        """
        # cleaning and error checking
        loc = loc.lower()
        assert loc[0] not in ChessBoard.ROWS, f"loc: '{loc}'. {loc[0]} out of column bounds (from visit)"
        assert loc[1] not in ChessBoard.COLS, f"loc: '{loc}'. {loc[1]} out of row bounds (from visit)"
        if legal_check:
            assert loc in self.moves(), f"'{self.knight}' -> '{loc}' is not a legal move"

        # if spot unvisited
        if self.board[loc] == 0:
            if self.knight != "":
                self.board[self.knight] = 1 # set to visited, unless knight is not initialized
            self.knight = loc
            self.move_list.append(loc)
            return True
        
        # if spot visited return false
        return False
    
    def moves(self) -> tuple[str]:
        """Retrieve knight's possible moves
        Returns:
            tuple[str]: list of cells the knight can move to
        """
        ret_val = []

        # (delta_col, delta_row): directional deltas for all knight moves
        movement_pattern = (
            (-2, -1), (-2, 1),
            (2, -1), (2, 1),
            (-1, -2), (1, -2),
            (-1, 2), (1, 2)
        )
        
        # find knight location in decimal
        k_loc = (ChessBoard.COLS.index(self.knight[0]), ChessBoard.ROWS.index(self.knight[1]))

        # for all possible movement deltas
        for move in movement_pattern:

            # calculate move
            dest = (k_loc[0]+move[0], k_loc[1]+move[1])

            # check if move is in bounds
            if (0 <= dest[0] < 8) and (0 <= dest[1] < 8):

                # convert move to chess notation
                move_loc = f"{ChessBoard.COLS[dest[0]]}{ChessBoard.ROWS[dest[1]]}"

                # if new cell is not visited, is valid move
                if not self.visited(move_loc):
                    ret_val.append(move_loc)

        return tuple(ret_val)

    def clone(self) -> 'ChessBoard':
        """Clones ChessBoard to a new object
        Returns:
            ChessBoard: duplicate of object 
        """
        ret_board = ChessBoard() # init blank instance
        ret_board.board = self.board.copy() # copy board dict
        ret_board.knight = self.knight # transfer knight location
        ret_board.start_loc = self.start_loc # transfer start location
        ret_board.move_list = self.move_list.copy() # copy move list
        return ret_board
    
    def __str__(self) -> str:
        ret_val = ""

        def color(s: str, fg: str=None, bg: str=None):
            """Recolors string using ANSI escape codes"""
            # color options
            bgs = {"grey": 100, "white": 47, "black": 40, "yellow": 103, "green": 42}
            fgs = {"knight": 30}

            if fg is not None and bg is not None: # both fg and bg
                color_code = f"\033[{fgs[fg]};{bgs[bg]}m"
            elif fg is not None: # just fg
                color_code = f"\033[{fgs[fg]}m"
            elif bg is not None: # just bg
                color_code = f"\033[;{bgs[bg]}m"

            return f"{color_code}{s}\033[0m"

        alternator = 0 # used to alternate cell colors for a checkered pattern
        for col in reversed(ChessBoard.ROWS): # add rows starting at top
            ret_val += f"{col} " # row marker
            for row in ChessBoard.COLS: # get each cell in the row
                c = "  " # default char for empty cell
                fg = None # default colors
                bg = None
                loc = f"{row}{col}" # create chess notated location

                if self.visited(loc): # if visited cell, color black
                    bg = "black"
                else: 
                    # if unvisited cell apply checkered pattern
                    if alternator % 2 == 0:
                        bg = "white"
                    else:
                        bg = "grey"
                    # if knight is on tile, mark that
                    if self.knight == loc:
                        fg = "knight"
                        bg = "yellow"
                        c = "Kn"
                if self.start_loc == loc: # show starting loc as green
                    bg = "green"

                ret_val += color(c, bg=bg, fg=fg) # actually add the cell to output
                alternator += 1

            ret_val += "\n"
            alternator -= 1 # creates checkers isntead of columns

        ret_val += "  " + " ".join(ChessBoard.COLS) # column markers
        return ret_val

def solve_knight_tour(board: ChessBoard) -> tuple[str]:
    """Recursively searches for a tour path
    Args:
        board (ChessBoard): initial board to search
    Returns:
        (tuple[str], int): List of all moves taken to complete tour, total number of recursive calls
    """

    class Throbber:
        """Class used for updates while search is completed"""

        def __init__(self):
            self.iter = 0

        def print(self) -> None:
            self.iter += 1
            print(f"\rProcessing. Recursive call #\033[96m{self.iter}\033[0m", end="")

    
    def solve_recur(board: ChessBoard) -> ChessBoard:
        """Recursive search function
        Args:
            board (ChessBoard): board to search
        Returns:
            ChessBoard: solved board, or None if there are no solutions from this board
        """

        # progress visual
        nonlocal throbber
        throbber.print()

        # early exit
        if board.complete():
            return board
                
        # create boards from possible moves
        boards = []
        for move in board.moves():
            temp: ChessBoard = board.clone()
            temp.visit(move)
            boards.append(temp)

        # sort those boards by which has the least future moves (see Warnsdorff's heuristic)
        boards.sort(key=lambda x: len(x.moves()))

        # recurr
        for b in boards:
            temp = solve_recur(b)
            if temp is not None:
                return temp
        
        # return none if not solution found
        return None
    
    throbber = Throbber() # init throbber
    solved = solve_recur(board) # find solution
    return tuple(solved.move_list), throbber.iter # return solution and stats

def visualize_tour(tour_path: tuple[str], init_board: ChessBoard, speed: float=0.25) -> None:
    """Show the knights path visually using printouts
    Args:
        tour_path (tuple[str]): a list of all the moves in the tour
        init_board (ChessBoard): the initial board (before the search began)
        speed (float): time in between moves (seconds)
    """
    from time import sleep

    # create and print board from initial position
    vis_board = init_board.clone()
    print("\033c", end="")  # ANSI escape sequence to clear screen
    print("Initial state")
    print(vis_board)
    sleep(speed+0.5)

    # for each move print out it's board
    for i, move in enumerate(tour_path[1:]):
        print("\033c", end="")
        print(f"Move #\033[96m{i+1}\033[0m")
        vis_board.visit(move)
        print(vis_board)
        sleep(speed)

    # final update to fully black out board
    print("\033c", end="")
    print(f"Tour complete in \033[96m{len(tour_path)-1}\033[0m moves")
    print(vis_board)