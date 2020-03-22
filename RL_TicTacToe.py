import numpy as np
import random
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.backend import reshape
from keras.utils.np_utils import to_categorical

#To add tensorflow to configuration, run this on cmd: python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl


def initBoard():
    board = [[0,0,0],[0,0,0],[0,0,0]]
    return board

def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i,j))
    return moves

def getWinner(board):
    candidate = 0
    won = 0

    for i in range(len(board)):
        candidate = 0
        for j in range(len(board[i])):

            if board[i][j] == 0:
                break

            if candidate == 0:
                candidate = board[i][j]

            if candidate != board[i][j]:
                break

            elif j == len(board[i]) - 1:
                won = candidate
    if won > 0:
        return won

    for j in range(len(board[0])):
        candidate = 0
        for i in range(len(board)):

            if board[i][j] == 0:
                break

            if candidate == 0:
                candidate = board[i][j]

            if candidate != board[i][j]:
                break

            elif i == len(board) - 1:
                won = candidate

    if won > 0:
        return won

    candidate = 0
    for i in range(len(board)):

        if board[i][j] == 0:
            break

        if candidate == 0:
            candidate = board[i][i]

        if candidate != board[i][i]:
            break

        elif i == len(board) - 1:
            won = candidate

    if won > 0:
        return won

    candidate = 0
    for i in range(len(board)):

        if board[2-i][2-i] == 0:
            break

        if candidate == 0:
            candidate = board[2-i][2-i]

        if candidate != board[2-i][2-i]:
            break

        elif i == len(board) - 1:
            won = candidate

    if won > 0:
        return won

    if len(getMoves(board)) == 0:
        return 0
    else:
        return -1

def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            mark = ' '
            if board[i][j] == 1:
                mark = 'X'
            elif board[i][j] == 2:
                mark = 'O'
            if j == len(board[i]) - 1:
                print(mark)
            else:
                print(str(mark) + '|', end = '')
        if i < len(board) - 1:
            print('-----')

def bestMove(board, model, player, rnd = 0):
    scores = []
    moves = getMoves(board)

    for i in range(len(moves)):
        future = np.array(board)
        future[moves[i][0]][moves[i][1]] = player
        prediction = model.predict(future.reshape((-1,9)))[0]
        if player == 1:
            winPrediction = prediction[1]
            lossPrediction = prediction[2]
        else:
            winPrediction = prediction[2]
            lossPrediction = prediction[1]
        drawPrediction = prediction[0]
        if winPrediction - lossPrediction > 0:
            scores.append(winPrediction - lossPrediction)
        else:
            scores.append(drawPrediction - lossPrediction)

    bestMoves = np.flip(np.argsort(scores))

    for i in range(len(bestMoves)):
        if random.random() * rnd < 0.5:
            return moves[bestMoves[i]]

    return moves[random.randint(0, len(moves) - 1)]

def simulateGame(p1 = None, p2 = None, rnd = 0):
    history = []
    board = initBoard()
    playerToMove = 1

    while getWinner(board) == -1:
        move = None
        if playerToMove == 1 and p1 != None:
            move = bestMove(board, p1, playerToMove, rnd)
        elif playerToMove == 2 and p2 != None:
            move = bestMove(board, p2, playerToMove, rnd)
        else:
            moves = getMoves(board)
            move = moves[random.randint(0, len(moves) - 1)]
        board[move[0]][move[1]] = playerToMove
        history.append((playerToMove, move))
        playerToMove = 1 if playerToMove == 2 else 2

    return history

def movesToBoard(moves):
    board = initBoard()
    for move in moves:
        player = move[0]
        coords = move[1]
        board[coords[0]][coords[1]] = player
    return board

games = [simulateGame() for _ in range(10000)]

def gameStats(games, player = 1):
    stats = {'win': 0, 'loss': 0, 'draw': 0}
    for game in games:
        result = getWinner(movesToBoard(game))
        if result == -1:
            continue
        elif result == player:
            stats['win'] += 1
        elif result == 0:
            stats['draw'] += 1
        else:
            stats['loss'] += 1

    winPct = stats['win']/len(games) * 100
    lossPct = stats['loss'] / len(games) * 100
    drawPct = stats['draw'] / len(games) * 100

    print("Results for player %d:" % (player))
    print("Wins: %d (%.1f%%)" % (stats["win"], winPct))
    print("Loss: %d (%.1f%%)" % (stats["loss"], lossPct))
    print("Draw: %d (%.1f%%)" % (stats["draw"], drawPct))

gameStats(games)
print()
gameStats(games, player = 2)

def getModel():
    numCells = 9
    outcomes = 3
    model = Sequential()
    model.add(Dense(200, activation='relu', input_shape=(numCells, )))
    model.add(Dropout(0.2))
    model.add(Dense(125, activation='relu'))
    model.add(Dense(75, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(outcomes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    return model


def gamesToWinLossData(games):
    X = []
    y = []
    for game in games:
        winner = getWinner(movesToBoard(game))
        for move in range(len(game)):
            X.append(movesToBoard(game[:(move + 1)]))
            y.append(winner)

    X = np.array(X).reshape((-1, 9))
    y = to_categorical(y)

    # Return an appropriate train/test split
    trainNum = int(len(X) * 0.8)
    return (X[:trainNum], X[trainNum:], y[:trainNum], y[trainNum:])

model = getModel()
X_train, X_test, y_train, y_test = gamesToWinLossData(games)
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=100)

games2 = [simulateGame(p1=model) for _ in range(1000)]
gameStats(games2)


