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
        47: 26, 
        49: 11, 
        56: 53,
        62: 19,
        64: 60,
        87: 24,
        93: 73,
        95: 75,
        98: 78,
        1: 38,
        4: 14,
        9: 31,
        21: 42,
        28: 84,
        36: 44,
        51: 67,
        71: 91,
        80: 99
    }

    board = Board(snakes_and_ladders)

    game = Game(players, board)
    game.play()
    anim = asyncio.run(Renderer.render_game(board, game.history))  # Store the FuncAnimation object

main()