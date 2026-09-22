import streamlit as st

st.set_page_config(page_title="틱택토", page_icon="⭕", layout="centered")

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 가로
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 세로
    (0, 4, 8), (2, 4, 6),             # 대각선
]


def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return "draw"
    return None


def minimax(board, player, human, computer):
    winner = check_winner(board)
    if winner == computer:
        return 1, None
    if winner == human:
        return -1, None
    if winner == "draw":
        return 0, None

    moves = [i for i, v in enumerate(board) if v is None]
    best_move = moves[0]
    if player == computer:
        best_score = -2
        for move in moves:
            board[move] = player
            score, _ = minimax(board, human, human, computer)
            board[move] = None
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = 2
        for move in moves:
            board[move] = player
            score, _ = minimax(board, computer, human, computer)
            board[move] = None
            if score < best_score:
                best_score = score
                best_move = move
    return best_score, best_move


def init_state():
    if "board" not in st.session_state:
        st.session_state.board = [None] * 9
    if "human" not in st.session_state:
        st.session_state.human = "X"
    if "turn" not in st.session_state:
        st.session_state.turn = "X"
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "scores" not in st.session_state:
        st.session_state.scores = {"승": 0, "패": 0, "무": 0}


def new_game(human_mark):
    st.session_state.board = [None] * 9
    st.session_state.human = human_mark
    st.session_state.turn = "X"
    st.session_state.winner = None


def computer_mark():
    return "O" if st.session_state.human == "X" else "X"


def make_move(index):
    board = st.session_state.board
    if board[index] is not None or st.session_state.winner:
        return
    board[index] = st.session_state.human
    st.session_state.turn = computer_mark()

    result = check_winner(board)
    if result:
        finish_game(result)
        return

    _, move = minimax(board, computer_mark(), st.session_state.human, computer_mark())
    if move is not None:
        board[move] = computer_mark()

    result = check_winner(board)
    if result:
        finish_game(result)
    else:
        st.session_state.turn = st.session_state.human


def finish_game(result):
    st.session_state.winner = result
    if result == "draw":
        st.session_state.scores["무"] += 1
    elif result == st.session_state.human:
        st.session_state.scores["승"] += 1
    else:
        st.session_state.scores["패"] += 1


init_state()

st.title("⭕ 틱택토 (Tic-Tac-Toe)")
st.caption("컴퓨터는 절대 지지 않는 미니맥스 AI를 사용해요. 이길 수 없다면 최소한 비겨보세요!")

with st.sidebar:
    st.header("설정")
    mark_choice = st.radio("내 말 선택", ["X", "O"], index=0 if st.session_state.human == "X" else 1)
    if mark_choice != st.session_state.human:
        new_game(mark_choice)
        st.rerun()

    st.header("전적")
    scores = st.session_state.scores
    st.metric("승", scores["승"])
    st.metric("패", scores["패"])
    st.metric("무", scores["무"])

    if st.button("전적 초기화"):
        st.session_state.scores = {"승": 0, "패": 0, "무": 0}
        st.rerun()

if st.session_state.human == "O" and all(v is None for v in st.session_state.board):
    _, move = minimax(
        st.session_state.board, computer_mark(), st.session_state.human, computer_mark()
    )
    if move is not None:
        st.session_state.board[move] = computer_mark()
        st.session_state.turn = st.session_state.human

board = st.session_state.board

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        i = row * 3 + col
        with cols[col]:
            label = board[i] if board[i] else " "
            disabled = board[i] is not None or st.session_state.winner is not None
            if st.button(label, key=f"cell_{i}", use_container_width=True, disabled=disabled):
                make_move(i)
                st.rerun()

st.divider()

if st.session_state.winner:
    if st.session_state.winner == "draw":
        st.info("무승부예요!")
    elif st.session_state.winner == st.session_state.human:
        st.success("축하해요, 이겼어요! 🎉")
    else:
        st.error("컴퓨터가 이겼어요. 다시 도전해보세요!")
    if st.button("새 게임 시작"):
        new_game(st.session_state.human)
        st.rerun()
else:
    turn_label = "당신" if st.session_state.turn == st.session_state.human else "컴퓨터"
    st.write(f"현재 차례: **{turn_label}**")
