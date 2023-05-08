import pygame
import asyncio

class Renderer:
    @staticmethod
    def calculate_row_col(position):
        row = (position - 1) // 10
        col = (position - 1) % 10
        if row % 2 == 1:
            col = 9 - col
        return row, col

    @staticmethod
    def init_window(board):
        pygame.init()
        screen = pygame.display.set_mode((500, 550))
        pygame.display.set_caption('Snakes and Ladders')
        return screen

    @staticmethod
    def draw_legend(screen, move_info):
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
        screen.blit(legend_surface, (20, 520))

    @staticmethod
    def draw_board(screen, board):
        cell_size = 50
        for i in range(1, 101):
            row, col = Renderer.calculate_row_col(i)
            x, y = col * cell_size, 500 - row * cell_size - cell_size

            if i in board.snakes_and_ladders:
                start = i
                end = board.snakes_and_ladders[i]
                start_row, start_col = Renderer.calculate_row_col(start)
                end_row, end_col = Renderer.calculate_row_col(end)

                x_start, y_start = start_col * cell_size + cell_size // 2, 500 - start_row * cell_size - cell_size // 2
                x_end, y_end = end_col * cell_size + cell_size // 2, 500 - end_row * cell_size - cell_size // 2

                pygame.draw.line(screen, (0, 255, 0) if end > start else (255, 0, 0), (x_start, y_start), (x_end, y_end), 5)

            font = pygame.font.Font(None, 24)
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (x + 20, y + cell_size // 2))

    @staticmethod
    def draw_players(screen, players_positions):
        cell_size = 50
        for player_color, position in players_positions.values():
            row, col = Renderer.calculate_row_col(position)
            x, y = col * cell_size, 500 - row * cell_size
            pygame.draw.circle(screen, player_color, (x + cell_size // 2, y - cell_size // 2), 10)

    @staticmethod
    async def render_game(board, history):
        screen = Renderer.init_window(board)
        clock = pygame.time.Clock()

        for frame in range(len(history)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            screen.fill((255, 255, 255))
            Renderer.draw_board(screen, board)

            players_positions = {}
            for move_info in history[:frame + 1]:
                player_name = move_info['player']
                player_color = move_info['color']
                position = move_info['position']
                players_positions[player_name] = (player_color, position)

            Renderer.draw_players(screen, players_positions)

            Renderer.draw_legend(screen, history[frame])

            pygame.display.flip()
            
            await asyncio.sleep(1)  # Set frame rate to 1 FPS
        

        pygame.quit()
