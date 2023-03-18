import requests
import json

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

if response.status_code == 200:
    unParsedObject = json.loads(response.content)
    #Getting games pgn format
    testGame = unParsedObject['games'][0]['pgn']
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
    inputPositions = []
    outputPositions = []
    for move in movesInPgn:
        #todo
        pass
else:
    print('Failed to fetch the URL')