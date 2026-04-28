import chess


def evaluate_board(board):
    values = {"P":1, "N":3, "B":3.25, "R":5, "Q":9, "K":0}    #material values
    score = 0

    for square, piece in board.piece_map().items():
        val = values[piece.symbol().upper()]
        score += val if piece.color == chess.WHITE else -val
    score += evaluate_king_safety(board)
    score += evaluate_pawn_structure(board)
    score += evaluate_piece_activity(board)
    return score



def evaluate_king_safety(board):
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        if king_square is None:
            continue

        attackers = board.attackers(not color, king_square)
        defender_pawns = 0
        for sq in chess.SQUARES:
            if board.piece_at(sq) and board.piece_at(sq).piece_type == chess.PAWN:
                if board.piece_at(sq).color == color:
                    if chess.square_distance(sq, king_square) <= 2:
                        defender_pawns += 1
        king_score = -0.5 * len(attackers) + 0.3 * defender_pawns
        score += king_score if color == chess.WHITE else -king_score

    return score



def evaluate_pawn_structure(board):
    score = 0

    for color in [chess.WHITE, chess.BLACK]:
        pawns = board.pieces(chess.PAWN, color)
        files = [chess.square_file(p) for p in pawns]
        pawn_score = 0

        for pawn in pawns:
            file = chess.square_file(pawn)
            # Doubled pawn penalty
            if files.count(file) > 1:
                pawn_score -= 0.25
            # Isolated pawn penalty
            if file-1 not in files and file+1 not in files:
                pawn_score -= 0.3

        score += pawn_score if color == chess.WHITE else -pawn_score

    return score



def evaluate_piece_activity(board):
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        mobility = 0
        for move in board.legal_moves:
            if board.color_at(move.from_square) == color:
                mobility += 1
        activity_score = 0.05 * mobility
        score += activity_score if color == chess.WHITE else -activity_score
    return score
