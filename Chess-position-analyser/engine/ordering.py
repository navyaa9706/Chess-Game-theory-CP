import heapq
from engine.evaluation import evaluate_board

def order_moves(board, moves):
    pq = []

    for move in moves:
        board.push(move)
        score = evaluate_board(board)
        board.pop()

        # max heap→use negative score
        heapq.heappush(pq, (-score, move))

    ordered = []
    while pq:
        score, move = heapq.heappop(pq)
        ordered.append(move)

    return ordered