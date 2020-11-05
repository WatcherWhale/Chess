#!/usr/bin/python3
import chess
import os.path

#from searchagent.search_agent import SearchAgent
from qlearningagent.QAgent import QAgent, loadAgentFromFile
from qlearningagent.State import State
from qlearningagent.Reward import calculateReward

prevWhiteState = (None, None)
prevBlackState = (None, None)

def run_episode(player: QAgent):

    global prevWhiteState
    global prevBlackState

    board = chess.Board()

    running = True
    turn_white_player = True
    counter = 0

    while running and not board.is_game_over():
        counter += 1
        action = None
        state = State(board.copy(), turn_white_player)

        action = player.makeMove(state)
        if action == None:
            print(board)
            exit(1)

        turn_white_player = not turn_white_player

        board.push(chess.Move.from_uci(action))

        if board.is_checkmate():
            running = False

            reward = calculateReward(state, action, state.newStateFromAction(action))
            player.update(state, action, reward, state.newStateFromAction(action))

            if turn_white_player:
                print("Black wins!")
            else:
                print("White wins!")

        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():

            running = False
            print("Stalemate")

            reward = calculateReward(state, action, state.newStateFromAction(action))
            player.update(state, action, reward, state.newStateFromAction(action))

        if turn_white_player:
            if prevBlackState[0] is not None:
                reward = calculateReward(prevBlackState[0], prevBlackState[1], state.newStateFromAction(action))
                player.update(prevBlackState[0], prevBlackState[1], reward, state.newStateFromAction(action))

            prevWhiteState = (state, action)
        else:
            if prevWhiteState[0] is not None:
                reward = calculateReward(prevWhiteState[0], prevWhiteState[1], state.newStateFromAction(action))
                player.update(prevWhiteState[0], prevWhiteState[1], reward, state.newStateFromAction(action))

            prevBlackState = (state, action)

    player.save()
    print(board.result())
    print(board)
    print("###################")


def main():
    if os.path.isfile('chess.sav'):
        player = loadAgentFromFile('chess.sav')
    else:
        player = QAgent('chess.sav', 0.5, 0.7, 0.6)

    for _ in range(20):
        run_episode(player)


if __name__ == "__main__":
    main()
