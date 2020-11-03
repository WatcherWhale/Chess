#!/usr/bin/python3
import chess
import os.path

#from searchagent.search_agent import SearchAgent
from qlearningagent.QAgent import QAgent, loadAgentFromFile
from qlearningagent.State import State
from qlearningagent.Reward import calculateReward

def run_episode(player: QAgent):
    board = chess.Board()


    running = True
    turn_white_player = True
    counter = 0

    while running:
        counter += 1
        action = None
        state = State(board.copy(), turn_white_player)

        action = player.computeAction(state)
        turn_white_player = not turn_white_player

        board.push(chess.Move.from_uci(action))
        #print(board)
        #print("###########################")
        #print(board.piece_at(chess.QUEEN))
        #print("###########################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("Black wins!")
            else:
                print("White wins!")

        if board.is_stalemate() or counter > 1000:
            running = False
            print("Stalemate")

        reward = calculateReward(state, action)
        player.update(state, action, reward, state.newStateFromAction(action))

    player.save()


def main():
    if os.path.isfile('chess.sav'):
        player = loadAgentFromFile('chess.sav')
    else:
        player = QAgent('chess.sav', 0.5, 0.7, 0.6)

    for _ in range(20):
        run_episode(player)


if __name__ == "__main__":
    main()
