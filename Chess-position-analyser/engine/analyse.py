from engine.greedy import analyse_position_greedy
from engine.iddfs import analyse_position_iddfs
from engine.minimax import analyse_position_minimax
from engine.alphabeta import analyse_position_alphabeta
from engine.negascout import analyse_position_negascout
from engine.pvs import analyse_position_pvs

def analyse_position(ui_board, turn):

    print("\n---- ANALYSIS ----\n")

    g_move, g_score, g_nodes, g_time = analyse_position_greedy(ui_board, turn)

    m_move, m_score, m_nodes, m_time = analyse_position_minimax(ui_board, turn)

    a_move, a_score, a_nodes, a_time = analyse_position_alphabeta(ui_board, turn)

    i_move, i_score, i_nodes, i_time = analyse_position_iddfs(ui_board, turn)

    n_move, n_score, n_nodes, n_time = analyse_position_negascout(ui_board, turn)

    p_move, p_score, p_nodes, p_time = analyse_position_pvs(ui_board, turn)

    print("\n---- COMPARISON ----")

    print("\nGREEDY:")
    print("Move:", g_move, "| Score:", g_score)
    print("Nodes:", g_nodes, "| Time:", round(g_time, 5))

    print("\nMINIMAX:")
    print("Move:", m_move, "| Score:", m_score)
    print("Nodes:", m_nodes, "| Time:", round(m_time, 5))

    print("\nALPHA-BETA:")
    print("Move:", a_move, "| Score:", a_score)
    print("Nodes:", a_nodes, "| Time:", round(a_time, 5))

    print("\nIDDFS:")
    print("Move:", i_move, "| Score:", i_score)
    print("Nodes:", i_nodes, "| Time:", round(i_time, 5))

    print("\nNEGASCOUT:")
    print("Move:", n_move, "| Score:", n_score)
    print("Nodes:", n_nodes, "| Time:", round(n_time, 5))

    print("\nPVS:")
    print("Move:", p_move, "| Score:", p_score)
    print("Nodes:", p_nodes, "| Time:", round(p_time, 5))
    print("\n-----------------\n")

    # RETURN (for UI)
    return {
        "greedy": {
            "move": g_move,
            "score": g_score,
            "nodes": g_nodes,
            "time": g_time
        },
        "minimax": {
            "move": m_move,
            "score": m_score,
            "nodes": m_nodes,
            "time": m_time
        },
        "alphabeta": {
            "move": a_move,
            "score": a_score,
            "nodes": a_nodes,
            "time": a_time
        },
        "iddfs": {
            "move": i_move,
            "score": i_score,
            "nodes": i_nodes,
            "time": i_time
        },
        "negascout": {
            "move": n_move,
            "score": n_score,
            "nodes": n_nodes,
            "time": n_time
        },
        "pvs": {
            "move": p_move,
            "score": p_score,
            "nodes": p_nodes,
            "time": p_time
        }
    }