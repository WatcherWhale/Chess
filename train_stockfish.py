#!/usr/bin/python3
import chess
import chess.engine
from qlearningagent.QAgent import QAgent, loadAgentFromFile
from chessUtil.State import State
from chessUtil.Reward import calculateReward
import os.path

STOCKFISH_BIN = '/usr/bin/stockfish'
QUIET = False

def main():
    player = loadPlayer()
    for _ in range(2):
        runEpisode(player)

def runEpisode(player: QAgent):
    board = chess.Board()
    black_player = chess.engine.SimpleEngine.popen_uci(STOCKFISH_BIN)
    limit = chess.engine.Limit(time=5.0)

    running = True
    turn_white_player = True

    prevState = (None, None)

    while running:
        move = None

        state = State(board.copy(), turn_white_player)

        if turn_white_player:
            move = chess.Move.from_uci(player.makeMove(state))
            turn_white_player = False

        else:
            move = black_player.play(board, limit).move
            turn_white_player = True

        board.push(move)
        
        if not QUIET:
            print(board)
            print("###########################")

        if board.is_checkmate():
            running = False

            if turn_white_player:
                print("Stockfish wins!")
            else:
                print("GrandQ wins!")

        if board.is_stalemate():
            running = False
            print("Stalemate")

        action = move.uci()
        if not turn_white_player:
            if prevState[0] is not None:
                reward = calculateReward(prevState[0], prevState[1], state.newStateFromAction(action))
                player.update(prevState[0], prevState[1], reward, state.newStateFromAction(action))
        else:
            prevState = (state, action)


    black_player.quit()
    player.save()

def loadPlayer():
    if os.path.isfile('chess.sav'):
        return loadAgentFromFile('chess.sav')
    else:
        return QAgent('chess.sav', 0.5, 0.7, 0.6)

if __name__ == "__main__":
    main()
