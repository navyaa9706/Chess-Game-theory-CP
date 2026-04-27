def coord_to_square(pos, BOARD_TOP_Y, BOARD_LEFT_X, BOARD_HEIGHT, SQUARE_SIZE):
    x, y = pos

    if BOARD_TOP_Y <= y < BOARD_TOP_Y + BOARD_HEIGHT and BOARD_LEFT_X <= x < BOARD_LEFT_X + BOARD_HEIGHT:
        row = (y - BOARD_TOP_Y) // SQUARE_SIZE
        col = (x - BOARD_LEFT_X) // SQUARE_SIZE
        return row, col

    return None