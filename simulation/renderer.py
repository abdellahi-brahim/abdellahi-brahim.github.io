import pygame
import asyncio

class Renderer:
    def __init__(self, board_width=500, board_height=500, cell_size=50):
        self.board_width = board_width
        self.board_height = board_height
        self.cell_size = cell_size

    def calculate_row_col(self, position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        return row, col

    def init_window(self, board):
        pygame.init()
        screen = pygame.display.set_mode((self.board_width, self.board_height + 50))
        pygame.display.set_caption('Snakes and Ladders')
        return screen

    def draw_legend(self, screen, move_info):
        font = pygame.font.Font(None, 24)

        player_name = move_info["player"]
        dice_rolls = move_info["dice"]
        position = move_info["position"]

        event_strings = []
        if move_info["snake"]:
            event_strings.append("Snake!")
        if move_info["ladder"]:
            event_strings.append("Ladder!")
        if move_info["overshoot"]:
            event_strings.append("Overshoot!")
        if move_info["winner"]:
            event_strings.append("Winner!")

        legend = f"{player_name} - Dice: {dice_rolls[0]}, {dice_rolls[1]} - Position: {position}"
        if event_strings:
            legend += " - " + ", ".join(event_strings)

        legend_surface = font.render(legend, True, (0, 0, 0))
        screen.blit(legend_surface, (20, self.board_height + 20))

    def draw_board(self, screen, board):
        for i in range(1, 101):
            row, col = self.calculate_row_col(i)
            x, y = col * self.cell_size, self.board_height - row * self.cell_size - self.cell_size

            if i in board.snakes_and_ladders:
                start = i
                end = board.snakes_and_ladders[i]
                start_row, start_col = self.calculate_row_col(start)
                end_row, end_col = self.calculate_row_col(end)

                x_start, y_start = start_col * self.cell_size + self.cell_size // 2, self.board_height - start_row * self.cell_size - self.cell_size // 2
                x_end, y_end = end_col * self.cell_size + self.cell_size // 2, self.board_height - end_row * self.cell_size - self.cell_size // 2

                pygame.draw.line(screen, (0, 255, 0) if end > start else (255, 0, 0), (x_start, y_start), (x_end, y_end), 5)

            font = pygame.font.Font(None, 24)
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (x + 20, y + self.cell_size // 2))

    def draw_players(self, screen, players_positions):
        cell_size = 50
        for player_color, position in players_positions.values():
            row, col = self.calculate_row_col(position)
            x, y = col * cell_size, 500 - row * cell_size
            pygame.draw.circle(screen, player_color, (x + cell_size // 2, y - cell_size // 2), 10)

    async def render_game(self, board, history):
        screen = self.init_window(board)
        clock = pygame.time.Clock()

        for frame in range(len(history)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.fill((255, 255, 255))
            self.draw_board(screen, board)

            players_positions = {}
            for move_info in history[:frame + 1]:
                player_name = move_info['player']
                player_color = move_info['color']
                position = move_info['position']
                players_positions[player_name] = (player_color, position)

            self.draw_players(screen, players_positions)

            self.draw_legend(screen, history[frame])

            pygame.display.flip()
            
            await asyncio.sleep(1)  # Set frame rate to 1 FPS
        

        pygame.quit()
