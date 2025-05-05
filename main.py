if __name__ == '__main__':
    from solver import ChessBoard, solve_knight_tour, visualize_tour
    from sys import argv
    from time import time

    VIS_SPEED = 0.25
    OCCUPIED_CELLS = None
    OUTPUT_PATH = "./stats.txt"

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
    t = time()
    solution, num_calls = solve_knight_tour(board)
    t = time() - t
    
    # if chosen, visualize knight's path via printouts
    choice = input("\nShow visualization? (y/n): ")
    if choice.lower() != 'n':
        visualize_tour(solution, board, VIS_SPEED)
        print()

    # build stats and write to file
    stats = ""
    stats += f"Knight starting location: {solution[0]}\n"
    stats += f"Knight ending location: {solution[-1]}\n"
    stats += f"Cells avoided: {OCCUPIED_CELLS}\n"
    stats += f"Time taken: {t} seconds\n"
    stats += f"Recursive calls made: {num_calls}\n"
    stats += f"Tour path: {solution}\n"

    with open(OUTPUT_PATH, 'w') as file:
        file.write(stats)

    print(f"Stats saved to '{OUTPUT_PATH}'\n")
    