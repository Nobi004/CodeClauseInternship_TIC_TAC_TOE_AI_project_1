import streamlit as st
import numpy as np

# Initialize board
def init_board():
    return np.zeros((3, 3), dtype=int)

# Check for winner
def check_winner(board):
    for i in range(3):
        if np.all(board[i, :] == 1) or np.all(board[:, i] == 1):
            return 1  # Player wins
        if np.all(board[i, :] == -1) or np.all(board[:, i] == -1):
            return -1  # AI wins
    if board[0, 0] == board[1, 1] == board[2, 2] != 0 or board[0, 2] == board[1, 1] == board[2, 0] != 0:
        return board[1, 1]
    if not np.any(board == 0):  # Draw
        return 0
    return None

# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner is not None:
        return winner
    if is_maximizing:
        max_eval = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board[i, j] = -1
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i, j] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = np.inf
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board[i, j] = 1
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i, j] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# AI move (optimized with corner and center priority)
def ai_move(board):
    # Check for immediate win or block
    for i in range(3):
        for j in range(3):
            if board[i, j] == 0:
                board[i, j] = -1
                if check_winner(board) == -1:
                    return (i, j)
                board[i, j] = 0
                board[i, j] = 1
                if check_winner(board) == 1:
                    board[i, j] = 0
                    return (i, j)
                board[i, j] = 0

    # Otherwise, use minimax
    best_score = -np.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i, j] == 0:
                board[i, j] = -1
                score = minimax(board, 0, False, -np.inf, np.inf)
                board[i, j] = 0
                if score > best_score:
                    best_score = score
                    move = (i, j)

    return move

# Streamlit App
st.title("🎮 Tic Tac Toe AI: Hard Mode")

# Persistent variables
if "board" not in st.session_state:
    st.session_state.board = init_board()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None

# Reset game
if st.button("🔄 Reset Game"):
    st.session_state.board = init_board()
    st.session_state.game_over = False
    st.session_state.winner = None

# Display board with animations
board = st.session_state.board
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        if board[i, j] == 1:
            cols[j].button("❌", disabled=True, key=f"btn-{i}-{j}")
        elif board[i, j] == -1:
            cols[j].button("⭕", disabled=True, key=f"btn-{i}-{j}")
        else:
            if not st.session_state.game_over:
                if cols[j].button(" ", key=f"btn-{i}-{j}"):
                    board[i, j] = 1
                    st.session_state.winner = check_winner(board)
                    if st.session_state.winner is None:
                        move = ai_move(board)
                        if move:
                            board[move] = -1
                            st.session_state.winner = check_winner(board)

# Check for winner
if st.session_state.winner is not None:
    st.session_state.game_over = True
    if st.session_state.winner == 1:
        st.success("🎉 You win!")
    elif st.session_state.winner == -1:
        st.error("💻 AI wins! Better luck next time!")
    else:
        st.warning("🤝 It's a draw!")
