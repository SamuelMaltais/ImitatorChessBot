import requests
import json
import chess

url = 'https://api.chess.com/pub/player/zibruh1/games/2023/03'
response = requests.get(url)
#K - King, Q - Queen, B - Bishop, N - Knight, R - Rook, P - Pawn.
nothing = 0
king = 1
queen = 2
bishop = 3
knignt = 4
rook = 5
pawn = 6
white = 1
black = 0
initialBoard = [
    [[black,rook],[black,knignt],[black,bishop],[black,queen],[black, king], [black, bishop], [black, knignt],[black, rook]],
    [[black, pawn],[black, pawn],[black, pawn],[black, pawn],[black, pawn],[black, pawn],[black, pawn],[black, pawn]],
    [nothing,nothing,nothing,nothing,nothing,nothing,nothing,nothing],
    [nothing,nothing,nothing,nothing,nothing,nothing,nothing,nothing],
    [nothing,nothing,nothing,nothing,nothing,nothing,nothing,nothing],
    [nothing,nothing,nothing,nothing,nothing,nothing,nothing,nothing],
    [[white, pawn],[white, pawn],[white, pawn],[white, pawn],[white, pawn],[white, pawn],[white, pawn],[white, pawn]],
    [[white,rook],[white,knignt],[white,bishop],[white,queen],[white, king], [white, bishop], [white, knignt],[white, rook]]
]

def makeBoardFromFen(str):
    row = []
    boardArray = []
    color = 1
    for char in str:
        if(char == " "):
            break
        elif(char == "/"):
            boardArray.append(row)
            row = []
        elif(char.isdigit()):
            num = int(char)
            for x in range(num):
                row.append(nothing)
        else:
            if(char.isupper()):
                color = 1
            else:
                color = 0
            if(char in ['r', 'R']):
                row.append([color, rook])
            elif(char in ['b', 'B']):
                row.append([color, bishop])
            elif(char in ['q', 'Q']):
                row.append([color, queen])
            elif(char in ['N','n']):
                row.append([color, knignt])
            elif(char in ['K','k']):
                row.append([color, king])
            else:
                row.append([color, pawn])   
    boardArray.append(row)
    return boardArray

if response.status_code == 200:
    unParsedObject = json.loads(response.content)
    
    inputPositions = []
    outputPositions = []

    for game in range(len(unParsedObject['games'])):
        #Getting games pgn format
        testGame = unParsedObject['games'][game]['pgn']
        arr = testGame.split('\n')
        whitePlayer = arr[4].split('"')[1]
        playingAsWhite = True
        if(whitePlayer != 'Zibruh1'):
            playingAsWhite = False
        #We isolate the moves, black moves will aways be the odd ones.
        gameData = arr[22].split(" ")
        count = 3
        temp = []
        #Extracts the moves without clock information ect
        for data in gameData:
            if(count % 2 == 0):
                temp.append(data)
            count += 1
        count = 2
        movesInPgn = []
        for data in temp:
            if(count % 2 == 0):
                movesInPgn.append(data)
            count += 1
        
        offset = 0
        if(not playingAsWhite):
                offset = 1

        board = chess.Board()
        initialBoardGenerated = makeBoardFromFen(board.fen())
        
        boardArray = []
        for move in movesInPgn:
            #If playing as white, the first board is input position, and every following move is just blacks response
            if(offset % 2 == 0):
                boardArray = makeBoardFromFen(board.fen())
                inputPositions.append(boardArray)
            #This is me move we chose to make given the position, so it is our output.
            board.push_san(move)

            if(offset % 2 == 0):
                boardArray = makeBoardFromFen(board.fen())
                outputPositions.append(boardArray)
            offset += 1
        if(len(inputPositions) != len(outputPositions)):
            if(len(inputPositions) > len(outputPositions)):
                inputPositions.pop()
            else:
                outputPositions.pop()
        ####
    print(inputPositions)
else:
    print('Failed to fetch the URL')