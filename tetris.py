import glob
from random import randint

import pygame

#########################################################
left_panel_start_x = 0
left_panel_start_y = 0

board_start_x = 200
board_start_y = 50

stage_start_x = 200
stage_start_y = board_start_y + 1000

right_panel_start_x = board_start_x + 600
right_panel_start_y = 0

held_block_panel_start_x = 25
held_block_panel_start_y = 50

next_block_panel_start_x = right_panel_start_x + 25
next_block_panel_start_y = 50

fps = 30

info_start_x = 25
info_start_y = 100 + 200 * .75
#########################################################

def initialize(gd):
    for filename in glob.glob("*.png"):
        gd[filename] = pygame.image.load(filename)
    gd["game_font"] = pygame.font.Font(None, 40)

    gd["board"] = []
    for i in range(20):
        arr = "x..........x"
        gd["board"].append(arr)
    gd["board"].append("xxxxxxxxxxxx")

    gd["blocks"] = {}
    gd["blocks"]["z"] = []
    gd["blocks"]["z"].append(["zz..",
                              ".zz.",
                              "....",
                              "...."])
    gd["blocks"]["z"].append([".z..",
                              "zz..",
                              "z...",
                              "...."])
    gd["blocks"]["z"].append(["....",
                              "zz..",
                              ".zz.",
                              "...."])
    gd["blocks"]["z"].append([".z..",
                              "zz..",
                              "z...",
                              "...."])

    gd["blocks"]["s"] = []
    gd["blocks"]["s"].append([".ss.",
                              "ss..",
                              "....",
                              "...."])
    gd["blocks"]["s"].append(["s...",
                              "ss..",
                              ".s..",
                              "...."])
    gd["blocks"]["s"].append(["....",
                              ".ss.",
                              "ss..",
                              "...."])
    gd["blocks"]["s"].append(["s...",
                              "ss..",
                              ".s..",
                              "...."])

    gd["blocks"]["i"] = []
    gd["blocks"]["i"].append([".i..",
                              ".i..",
                              ".i..",
                              ".i.."])
    gd["blocks"]["i"].append(["....",
                              "iiii",
                              "....",
                              "...."])
    gd["blocks"]["i"].append(["..i.",
                              "..i.",
                              "..i.",
                              "..i."])
    gd["blocks"]["i"].append(["....",
                              "....",
                              "iiii",
                              "...."])

    gd["blocks"]["o"] = []
    gd["blocks"]["o"].append(["oo..",
                              "oo..",
                              "....",
                              "...."])
    gd["blocks"]["o"].append(["oo..",
                              "oo..",
                              "....",
                              "...."])
    gd["blocks"]["o"].append(["oo..",
                              "oo..",
                              "....",
                              "...."])
    gd["blocks"]["o"].append(["oo..",
                              "oo..",
                              "....",
                              "...."])

    gd["blocks"]["t"] = []
    gd["blocks"]["t"].append([".t..",
                              "ttt.",
                              "....",
                              "...."])
    gd["blocks"]["t"].append([".t..",
                              ".tt.",
                              ".t..",
                              "...."])
    gd["blocks"]["t"].append(["ttt.",
                              ".t..",
                              "....",
                              "...."])
    gd["blocks"]["t"].append([".t..",
                              "tt..",
                              ".t..",
                              "...."])

    gd["blocks"]["l"] = []
    gd["blocks"]["l"].append([".l..",
                              ".l..",
                              ".ll.",
                              "...."])
    gd["blocks"]["l"].append(["....",
                              "lll.",
                              "l...",
                              "...."])
    gd["blocks"]["l"].append(["ll..",
                              ".l..",
                              ".l..",
                              "...."])
    gd["blocks"]["l"].append(["..l.",
                              "lll.",
                              "....",
                              "...."])

    gd["blocks"]["j"] = []
    gd["blocks"]["j"].append([".j..",
                              ".j..",
                              "jj..",
                              "...."])
    gd["blocks"]["j"].append(["j...",
                              "jjj.",
                              "....",
                              "...."])
    gd["blocks"]["j"].append(["jj..",
                              "j...",
                              "j...",
                              "...."])
    gd["blocks"]["j"].append(["jjj.",
                              "..j.",
                              "....",
                              "...."])

    gd["score_table"] = [10,40,100,200]
    gd["score"] = 0

    return gd


def has_conflict(gd, block_x, block_y, direction):
    board = gd["board"]
    block_letter = gd["current_block"][0]
    block = gd["blocks"][block_letter][direction]
    for r in range(0, 4):
        for c in range(4):
            if block_x + c <= 11 and block_y + r <= 20:
                board_stone = board[block_y + r][block_x + c]
                block_stone = block[r][c]
                if board_stone != "." and block_stone != ".":
                    print(f"conflict | block_x = {block_x} | block_y = {block_y} | r = {r} | c = {c}")
                    return True
    return False


def replace_stone(old_row, new_stone_idx, new_stone_letter):
    part1 = old_row[0:new_stone_idx]
    part3 = old_row[new_stone_idx + 1:len(old_row)]
    return part1 + new_stone_letter + part3


def copy_block_to_board(gd):
    board = gd["board"]
    block_letter = gd["current_block"][0]
    direction = gd["current_block"][1]
    block = gd["blocks"][block_letter][direction]
    block_x = gd["x_pos"]
    block_y = gd["y_pos"]
    for r in range(0, 4):
        for c in range(4):
            if block_x + c <= 11 and block_y + r <= 20:
                board_stone = board[block_y + r][block_x + c]
                block_stone = block[r][c]
                if board_stone == "." and block_stone != ".":
                    old_row = board[block_y + r]
                    print(board[block_y + r])
                    board[block_y + r] = replace_stone(old_row, block_x + c, block_stone)
                    print(board[block_y + r])

def move_block_left(gd):
    if not has_conflict(gd, gd["x_pos"] - 1, gd["y_pos"], gd["current_block"][1]):
        gd["x_pos"] -= 1


def move_block_right(gd):
    if not has_conflict(gd, gd["x_pos"] + 1, gd["y_pos"], gd["current_block"][1]):
        gd["x_pos"] += 1


def rotate_block(gd):
    if not has_conflict(gd, gd["x_pos"], gd["y_pos"], (gd["current_block"][1] + 1) % 4):
        new_direction = gd["current_block"][1] + 1
        if new_direction > 3:
            new_direction = 0
        gd["current_block"] = (gd["current_block"][0], new_direction)


def move_block_down(gd):
    if not has_conflict(gd, gd["x_pos"], gd["y_pos"] + 1, gd["current_block"][1]):
        gd["y_pos"] += 1
        return True
    return False


def drop_block(gd):
    while move_block_down(gd):
        pass


def hold_block(gd):
    pass


def draw_background(gd):
    gd["screen"].blit(gd["background.png"], (200, 0))


def draw_side_panels(gd):
    gd["screen"].blit(gd["side_panel.png"], (0, 0))
    gd["screen"].blit(gd["side_panel.png"], (800, 0))


def draw_stage(gd):
    gd["screen"].blit(gd["stage.png"], (200, 0))
    gd["screen"].blit(gd["stage.png"], (200, 1050))


def draw_walls(gd):
    gd["screen"].blit(gd["wall.png"], (200, 50))
    gd["screen"].blit(gd["wall.png"], (750, 50))


def draw_block(gd):
    if "current_block" not in gd or gd["current_block"] is None:
        return
    block_letter = gd["current_block"][0]
    block_direction = gd["current_block"][1]
    current_block = gd["blocks"][block_letter][block_direction]
    block_start_pos_x = 250 + (50 * (gd["x_pos"] - 1))
    block_start_pos_y = 50 + (50 * gd["y_pos"])
    for r in range(0, 4):
        for c in range(0, 4):
            stone = current_block[r][c]
            stone_x = block_start_pos_x + 50 * c
            stone_y = block_start_pos_y + 50 * r
            if stone != ".":
                gd["screen"].blit(gd[f"block_{block_letter}.png"], (stone_x, stone_y))


def draw_next_block(gd):
    if "next_blocks" not in gd or gd["next_blocks"] is None or len(gd["next_blocks"]) == 0:
        return
    next_block_tuple = gd["next_blocks"][0]
    block_letter, direction = next_block_tuple
    next_block_stripe = gd["blocks"][block_letter][direction]

    for r in range(0, 4):
        for c in range(0, 4):
            stone = next_block_stripe[r][c]
            stone_x = next_block_panel_start_x + 50 * c * .75
            stone_y = next_block_panel_start_y + 50 * r * .75
            if stone != ".":
                smaller_stone = pygame.transform.scale(gd[f"block_{block_letter}.png"], (int(50 * .75),int(50 * .75)))
                gd["screen"].blit(smaller_stone, (stone_x, stone_y))


def draw_held_block(gd):
    if "held_block" not in gd or gd["held_block"] is None:
        return
    held_block_tuple = gd["held_block"]
    block_letter, direction = held_block_tuple
    held_block_stripe = gd["blocks"][block_letter][direction]

    for r in range(0, 4):
        for c in range(0, 4):
            stone = held_block_stripe[r][c]
            stone_x = held_block_panel_start_x + 50 * c * .75
            stone_y = held_block_panel_start_y + 50 * r * .75
            if stone != ".":
                smaller_stone = pygame.transform.scale(gd[f"block_{block_letter}.png"], (int(50 * .75), int(50 * .75)))
                gd["screen"].blit(smaller_stone, (stone_x, stone_y))


def draw_board(gd):
    board_start_x = 200
    board_start_y = 50
    board = gd["board"]
    for r in range(20):
        for c in range(12):
            stone_x = board_start_x + c * 50
            stone_y = board_start_y + r * 50
            board_stone = board[r][c]
            if board_stone != "x" and board_stone != ".":
                gd["screen"].blit(gd[f"block_{board_stone}.png"],(stone_x,stone_y))


def draw_score(gd):
    msg_txt = f"Score: {gd['score']}"
    msg = gd["game_font"].render(msg_txt, True, (255, 255, 255))
    msg_rect = msg.get_rect()
    msg_width, msg_height = msg_rect.size
    gd["screen"].blit(msg, (info_start_x, info_start_y))


def draw_all(gd):
    draw_background(gd)
    draw_side_panels(gd)
    draw_stage(gd)
    draw_walls(gd)
    draw_board(gd)
    draw_block(gd)
    draw_next_block(gd)
    draw_held_block(gd)
    draw_score(gd)


def gen_new_block_letter(gd):
    letter_list = list(gd["blocks"].keys())
    return letter_list[randint(0, len(letter_list) - 1)]


def gen_random_block(gd):
    return gen_new_block_letter(gd), randint(0, 3)


def gen_new_blocks(gd):
    if "next_blocks" not in gd:
        gd["next_blocks"] = []
    while len(gd["next_blocks"]) < 2:
        gd["next_blocks"].append(gen_random_block(gd))
    gd["current_block"] = gd["next_blocks"].pop(0)

    gd["x_pos"] = 4
    gd["y_pos"] = 0

    return not has_conflict(gd, gd["x_pos"], gd["y_pos"], gd["current_block"][1])


def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("Tetris 99 - Main Theme.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()


def can_go_down(gd):
    if not has_conflict(gd, gd["x_pos"], gd["y_pos"] + 1, gd["current_block"][1]):
        return True
    return False


def full_row(gd, r):
    row = gd["board"][r]
    for ch in row:
        if ch == '.':
            return False
    else:
        return True


def move_rows_down(gd, r):
    for r2 in range(r,0,-1):
        gd["board"][r2] = gd["board"][r2-1]
    gd["board"][0] = "x..........x"


def delete_row(gd,r):
    if full_row(gd,r):
        move_rows_down(gd,r)
        return 1
    else:
        return 0


def delete_rows(gd):
    num_deleted_rows = 0
    for r in range(20):
        num_deleted_rows += delete_row(gd,r)
    return num_deleted_rows


def play_game(gd):
    clock = pygame.time.Clock()
    running = True


    play_music()
    internal_pos_y = 0
    while running:
        dt = clock.tick(fps)

        if "current_block" not in gd or gd["current_block"] is None:
            if gen_new_blocks(gd) is False:
                print("game over")
                running = False
            internal_pos_y = 0

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    move_block_left(gd)
                elif e.key == pygame.K_RIGHT:
                    move_block_right(gd)
                elif e.key == pygame.K_UP:
                    rotate_block(gd)
                elif e.key == pygame.K_DOWN:
                    move_block_down(gd)
                elif e.key == pygame.K_SPACE:
                    drop_block(gd)
                elif e.key == pygame.K_h:
                    hold_block(gd)
                elif e.key == pygame.K_ESCAPE:
                    running = False

        internal_pos_y += .1 * dt
        if internal_pos_y >= 50:
            move_block_down(gd)
            internal_pos_y = 0

        if not can_go_down(gd):
            copy_block_to_board(gd)
            gd["current_block"] = None

        num_deleted_rows = delete_rows(gd)
        if num_deleted_rows > 0:
            gd["score"] += gd["score_table"][num_deleted_rows - 1]


        # print(f"x pos = {gd['x_pos']} ||| y pos = {gd['y_pos']} ||| direction = {gd['current_block'][1]} dt = {dt}")
        print(gd["score"])
        draw_all(gd)
        pygame.display.update()


def start_game():
    pygame.init()

    gd = {}
    gd["screen_width"] = screen_width = 1000
    gd["screen_height"] = screen_height = 1100
    gd["screen"] = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris")
    gd = initialize(gd)

    play_game(gd)
    pygame.quit()


if __name__ == "__main__":
    start_game()
