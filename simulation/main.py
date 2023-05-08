from player import Player
from board import Board
from game import Game
from renderer import Renderer
import asyncio

def main():
    player1 = Player("Player 1", "Red")
    player2 = Player("Player 2", "Blue")
    player3 = Player("Player 3", "Green")
    player4 = Player("Player 4", "Yellow")

    players = [player1, player2, player3, player4]

    snakes_and_ladders = {
        16: 6, 
        46: 25, 
        49: 11, 
        62: 19,
        64: 60,
        74: 53,
        89: 68,
        92: 88,
        95: 75,
        99: 80,
        2: 38,
        7: 14,
        8: 31,
        15: 26,
        21: 42,
        28: 84,
        51: 67,
        71: 91,
        78: 98
    }

    board = Board(snakes_and_ladders)

    game = Game(players, board)
    game.play()
    anim = asyncio.run(Renderer.render_game(board, game.history))  # Store the FuncAnimation object

main()
