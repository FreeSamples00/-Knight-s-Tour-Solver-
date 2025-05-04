from solver import ChessBoard, solve_knight_tour, visualize_tour

if __name__ == '__main__':
    from sys import argv

    VIS_SPEED = 0.25
    OCCUPIED_CELLS = None

    # validate input
    if len(argv) < 2:
        raise ValueError(f"Needs at least one argument. {argv}")

    if (len(argv[1]) != 2) or (not argv[1][0].isalpha()) or (not argv[1][1].isdigit()):
        raise ValueError(f"Improperly formatted initial coordinate '{argv[1]}'")

    if (len(argv) > 2):
        OCCUPIED_CELLS = []
        for coord in argv[2:]:
            if (len(coord) != 2) or (not coord[0].isalpha()) or (not coord[1].isdigit()):
                raise ValueError(f"Improperly formatted coordinate: {coord}")
            else:
                OCCUPIED_CELLS.append(coord)


    # setup chess board
    board = ChessBoard(argv[1], OCCUPIED_CELLS)

    # solve knight's tour
    solution, num_calls = solve_knight_tour(board)
    
    # if chosen, visualize knight's path via printouts
    choice = input("\nShow visualization? (y/n): ")
    if choice.lower() != 'n':
        visualize_tour(solution, board, VIS_SPEED)
    