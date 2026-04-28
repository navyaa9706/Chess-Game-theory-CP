def board_to_fen(board, turn="w"):
    piece_map = {
        "wP":"P","wR":"R","wN":"N","wB":"B","wQ":"Q","wK":"K",
        "bP":"p","bR":"r","bN":"n","bB":"b","bQ":"q","bK":"k"
    }

    fen = ""

    for row in board:
        empty = 0
        for cell in row:
            if cell is None:
                empty += 1
            else:
                if empty:
                    fen += str(empty)
                    empty = 0
                fen += piece_map[cell]
        if empty:
            fen += str(empty)
        fen += "/"

    fen = fen[:-1]
    fen += f" {turn} - - 0 1"

    return fen