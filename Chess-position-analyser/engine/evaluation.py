def evaluate_board(board):
    values = {"P":1,"N":3,"B":3,"R":5,"Q":9,"K":100}
    score = 0

    for piece in board.piece_map().values():
        val = values[piece.symbol().upper()]
        if piece.color:
            score += val
        else:
            score -= val

    return score