import pygame
import random
from mazetile import mazetile

pygame.font.init()

WIDTH = 820
HEIGHT = 820
FPS = 10

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

BORDER = 10
WALL_SIZE = 1

MAZE_WIDTH = 25
MAZE_HEIGHT = 25

tracker = False
multiplayer = True

# COLORMAP
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGD_COL = (153, 178, 221)
PALE_COL = (255, 252, 249)
DARK_COL = (38, 84, 124)
ACCENT_COL1 = (239, 71, 111)
ACCENT_COL2 = (255, 209, 102)
NEUTRAL_COL = (153, 178, 221)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WINNER_FONT = pygame.font.SysFont('Arial', 100)


def build_tiles(maze_width, maze_height):
    # Determine size of square
    s = min((WIDTH - 2 * BORDER) // MAZE_WIDTH, (HEIGHT - 2 * BORDER) // MAZE_HEIGHT)
    tiles = []

    for i in range(maze_width):
        tile_col = []
        for j in range(maze_height):
            tile_col.append(mazetile(i, j, s))
        tiles.append(tile_col)

    return s, tiles


def build_maze(tiles):
    stack = []
    visited = []

    # init
    cur_cell = tiles[0][0]
    stack.append(cur_cell)
    visited.append(cur_cell)

    while len(stack) > 0:
        cell = []
        # Add complexity:
        #   - add small chance to revisit a cell
        revisit = random.random() > 0.95

        # is TOP available?
        top_cell = None
        if cur_cell.y - 1 >= 0:
            top_cell = tiles[cur_cell.x][cur_cell.y - 1]
            if top_cell not in visited or revisit:
                cell.append("top")

        # is BOTTOM available?
        bottom_cell = None
        if cur_cell.y + 1 < MAZE_HEIGHT:
            bottom_cell = tiles[cur_cell.x][cur_cell.y + 1]
            if bottom_cell and (bottom_cell not in visited or revisit):
                cell.append("bottom")

        # is RIGHT available?
        right_cell = None
        if cur_cell.x + 1 < MAZE_WIDTH:
            right_cell = tiles[cur_cell.x + 1][cur_cell.y]
            if right_cell and (right_cell not in visited or revisit):
                cell.append("right")

        # is LEFT available?
        left_cell = None
        if cur_cell.x - 1 >= 0:
            left_cell = tiles[cur_cell.x - 1][cur_cell.y]
            if left_cell and (left_cell not in visited or revisit):
                cell.append("left")

        if len(cell) > 0:
            cell_chosen = random.choice(cell)

            if cell_chosen == "top":
                cur_cell.top = top_cell
                top_cell.bottom = cur_cell
                cur_cell = top_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

            if cell_chosen == "bottom":
                cur_cell.bottom = bottom_cell
                bottom_cell.top = cur_cell
                cur_cell = bottom_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

            if cell_chosen == "right":
                cur_cell.right = right_cell
                right_cell.left = cur_cell
                cur_cell = right_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

            if cell_chosen == "left":
                cur_cell.left = left_cell
                left_cell.right = cur_cell
                cur_cell = left_cell
                visited.append(cur_cell)
                stack.append(cur_cell)

        else:
            cur_cell = stack.pop()

    return tiles


def draw_maze(tiles, size):  # Draw maze at the start as white rectangle + tiles on top
    WIN.fill(BGD_COL)
    s = size - WALL_SIZE
    board = pygame.Rect(BORDER, BORDER, WIDTH - 2 * BORDER + 1, HEIGHT - 2 * BORDER + 1)
    pygame.draw.rect(WIN, PALE_COL, board)

    for tile_row in tiles:
        for t in tile_row:
            right_passage = 0
            bottom_passage = 0
            if t.right:
                right_passage = WALL_SIZE
            if t.bottom:
                bottom_passage = WALL_SIZE
            tile = pygame.Rect(t.posx + BORDER + WALL_SIZE,
                               t.posy + BORDER + WALL_SIZE,
                               s + right_passage, s + bottom_passage)
            pygame.draw.rect(WIN, DARK_COL, tile)

    last_tile = pygame.Rect(tiles[-1][-1].posx + BORDER + WALL_SIZE + 5,
                            tiles[-1][-1].posy + BORDER + WALL_SIZE + 5,
                            s - 10, s - 10)
    pygame.draw.rect(WIN, PALE_COL, last_tile)

    pygame.display.update()


def move_player(player1, cur_tile1, next_tile1, player2, cur_tile2, next_tile2, s):
    tile1 = pygame.Rect(cur_tile1.posx + BORDER + WALL_SIZE, cur_tile1.posy + BORDER + WALL_SIZE,
                        s - WALL_SIZE, s - WALL_SIZE)
    tile2 = pygame.Rect(cur_tile2.posx + BORDER + WALL_SIZE, cur_tile2.posy + BORDER + WALL_SIZE,
                        s - WALL_SIZE, s - WALL_SIZE)

    pygame.draw.rect(WIN, DARK_COL, tile1)
    pygame.draw.rect(WIN, DARK_COL, tile2)

    # move players to next tile
    player1.x = next_tile1.posx + 5 + BORDER + WALL_SIZE
    player1.y = next_tile1.posy + 5 + BORDER + WALL_SIZE

    player2.x = next_tile2.posx + 5 + BORDER + WALL_SIZE
    player2.y = next_tile2.posy + 5 + BORDER + WALL_SIZE

    # In case of overlap
    player1xtra = pygame.Rect(next_tile1.posx + 5 + BORDER + WALL_SIZE,
                              next_tile1.posy + 5 + BORDER + WALL_SIZE,
                              (s - 10) / 2, (s - 10))

    # draw_player
    pygame.draw.rect(WIN, ACCENT_COL1, player1)
    pygame.draw.rect(WIN, ACCENT_COL2, player2)
    pygame.draw.rect(WIN, ACCENT_COL1, player1xtra)

    # track path
    if tracker:
        tracker_ind = pygame.Rect(cur_tile1.posx + BORDER + WALL_SIZE + (s / 2 - 2),
                                  cur_tile1.posy + BORDER + WALL_SIZE + (s / 2 - 2),
                                  4, 4)
        pygame.draw.rect(WIN, NEUTRAL_COL, tracker_ind)

    # update image
    pygame.display.update()
    return player1, player2, next_tile1, next_tile2


def draw_winner(text="Bravo!", color=WHITE):
    draw_text = WINNER_FONT.render(text, True, color)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def handle_player_movement(keys_pressed, player1, player2, cur_tile1, cur_tile2, step):
    # PLAYER 1
    if keys_pressed[pygame.K_UP] and cur_tile1.top:
        player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1.top,
                                                             player2, cur_tile2, cur_tile2, step)

    if keys_pressed[pygame.K_DOWN] and cur_tile1.bottom:
        player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1.bottom,
                                                             player2, cur_tile2, cur_tile2, step)

    if keys_pressed[pygame.K_LEFT] and cur_tile1.left:
        player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1.left,
                                                             player2, cur_tile2, cur_tile2, step)

    if keys_pressed[pygame.K_RIGHT] and cur_tile1.right:
        player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1.right,
                                                             player2, cur_tile2, cur_tile2, step)

    # PLAYER 2
    if multiplayer:
        if keys_pressed[pygame.K_w] and cur_tile2.top:
            player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1,
                                                                 player2, cur_tile2, cur_tile2.top, step)

        if keys_pressed[pygame.K_s] and cur_tile2.bottom:
            player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1,
                                                                 player2, cur_tile2, cur_tile2.bottom, step)

        if keys_pressed[pygame.K_a] and cur_tile2.left:
            player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1,
                                                                 player2, cur_tile2, cur_tile2.left, step)

        if keys_pressed[pygame.K_d] and cur_tile2.right:
            player1, player2, cur_tile1, cur_tile2 = move_player(player1, cur_tile1, cur_tile1,
                                                                 player2, cur_tile2, cur_tile2.right, step)

    return player1, player2, cur_tile1, cur_tile2


def main():
    step, tiles = build_tiles(MAZE_WIDTH, MAZE_HEIGHT)
    tiles = build_maze(tiles)
    draw_maze(tiles, step)

    cur_tile1 = cur_tile2 = tiles[0][0]
    player1 = pygame.Rect(cur_tile1.posx + 5 + BORDER + WALL_SIZE,
                          cur_tile1.posy + 5 + BORDER + WALL_SIZE,
                          step - 10, step - 10)

    player2 = pygame.Rect(cur_tile2.posx + 5 + BORDER + WALL_SIZE,
                          cur_tile2.posy + 5 + BORDER + WALL_SIZE,
                          step - 10, step - 10)

    player1xtra = pygame.Rect(cur_tile1.posx + 5 + BORDER + WALL_SIZE,
                              cur_tile1.posy + 5 + BORDER + WALL_SIZE,
                              (step - 10) / 2, (step - 10))

    pygame.draw.rect(WIN, ACCENT_COL1, player1)
    pygame.draw.rect(WIN, ACCENT_COL2, player2)
    pygame.draw.rect(WIN, ACCENT_COL1, player1xtra)

    pygame.display.update()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        keys_pressed = pygame.key.get_pressed()
        player1, player2, cur_tile1, cur_tile2 = handle_player_movement(keys_pressed, player1, player2,
                                                                        cur_tile1, cur_tile2, step)

        if cur_tile1 == tiles[-1][-1]:
            draw_winner("PINK WINS!", ACCENT_COL1)
            break

        if cur_tile2 == tiles[-1][-1]:
            draw_winner("YELLOW WINS!", ACCENT_COL2)
            break

    main()


if __name__ == '__main__':
    main()
