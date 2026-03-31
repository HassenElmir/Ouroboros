import pygame
import random
import sys
import math

pygame.init()

# ---------------- Window & Settings ----------------
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ouroboros - Animated Snake Edition")

clock = pygame.time.Clock()

# ---------------- Load Sounds & Music ----------------
pygame.mixer.init()
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
    eat_sound.set_volume(1.0)
except:
    print("Warning: eat.wav not found!")
    eat_sound = None

try:
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Warning: music.mp3 not found!")

# ---------------- Colors ----------------
WHITE        = (255, 255, 255)
BLACK        = (0,   0,   0  )
GREEN_HEAD   = (0,   255, 0  )
GREEN_BODY   = (0,   180, 0  )
BLUE_HEAD    = (0,   180, 255)
BLUE_BODY    = (0,   100, 200)
RED          = (220, 0,   0  )
DARK_GRAY    = (50,  50,  50 )
YELLOW       = (255, 255, 0  )
PURPLE       = (128, 0,   128)
GRAY         = (150, 150, 150)
HIGHLIGHT    = (255, 200, 0  )
TONGUE_COLOR = (255, 0,   0  )
BRICK_COLOR  = (139, 69,  19 )
GOLD         = (255, 200, 0  )

# ---------------- Fonts ----------------
title_font   = pygame.font.SysFont("comicsansms", 44, bold=True)
subtitle_font= pygame.font.SysFont("comicsansms", 22, bold=False)
option_font  = pygame.font.SysFont("comicsansms", 28)
small_font   = pygame.font.SysFont("comicsansms", 20)
big_font     = pygame.font.SysFont("comicsansms", 62, bold=True)

BLOCK = 20

# ================================================================
# MENU
# ================================================================
def menu():
    selected_speed = 10
    selected_lives = 3
    use_obstacles  = False
    game_mode      = "single"   # "single" | "multi"
    option         = 0          # 0=Speed 1=Lives 2=Obstacles 3=Mode 4=Start

    running = True
    while running:
        screen.fill(BLACK)

        # --- Title ---
        t1 = title_font.render("OUROBOROS", True, GREEN_HEAD)
        t2 = subtitle_font.render("Animated Snake Edition", True, GOLD)
        screen.blit(t1, [WIDTH//2 - t1.get_width()//2, HEIGHT*0.04])
        screen.blit(t2, [WIDTH//2 - t2.get_width()//2, HEIGHT*0.04 + t1.get_height() + 4])

        items = [
            option_font.render(f"Speed: {selected_speed}",
                               True, WHITE if option==0 else GRAY),
            option_font.render(f"Lives: {selected_lives}",
                               True, WHITE if option==1 else GRAY),
            option_font.render(f"Obstacles: {'ON' if use_obstacles else 'OFF'}",
                               True, WHITE if option==2 else GRAY),
            option_font.render(f"Mode: {'Multiplayer' if game_mode=='multi' else 'Single Player'}",
                               True, WHITE if option==3 else GRAY),
            option_font.render("Start Game",
                               True, WHITE if option==4 else GRAY),
        ]

        positions_y = [HEIGHT*0.24, HEIGHT*0.34, HEIGHT*0.44, HEIGHT*0.54, HEIGHT*0.64]
        for item, py in zip(items, positions_y):
            screen.blit(item, [WIDTH//2 - item.get_width()//2, py])

        if game_mode == "multi":
            hint = small_font.render(
                "P1 (Green): Arrow Keys  |  P2 (Blue): WASD  —  lose all lives = instant defeat",
                True, BLUE_HEAD)
            screen.blit(hint, [WIDTH//2 - hint.get_width()//2, HEIGHT*0.73])

        nav = small_font.render(
            "UP/DOWN to navigate, LEFT/RIGHT to change, ENTER to start.", True, WHITE)
        screen.blit(nav, [WIDTH//2 - nav.get_width()//2, HEIGHT*0.84])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option = (option - 1) % 5
                elif event.key == pygame.K_DOWN:
                    option = (option + 1) % 5
                elif event.key == pygame.K_LEFT:
                    if option == 0: selected_speed = max(5,  selected_speed - 1)
                    elif option == 1: selected_lives = max(1, selected_lives  - 1)
                    elif option == 2: use_obstacles  = not use_obstacles
                    elif option == 3: game_mode = "single" if game_mode == "multi" else "multi"
                elif event.key == pygame.K_RIGHT:
                    if option == 0: selected_speed = min(25, selected_speed + 1)
                    elif option == 1: selected_lives = min(10, selected_lives + 1)
                    elif option == 2: use_obstacles  = not use_obstacles
                    elif option == 3: game_mode = "multi" if game_mode == "single" else "single"
                elif event.key == pygame.K_RETURN and option == 4:
                    running = False

    return selected_speed, selected_lives, use_obstacles, game_mode


# ================================================================
# RIDDLES
# ================================================================
riddles = [
    {"question": "What has keys but can't open locks?",                                        "answer": "keyboard"},
    {"question": "What has a face and two hands but no arms or legs?",                         "answer": "clock"},
    {"question": "I speak without a mouth and hear without ears. What am I?",                  "answer": "echo"},
    {"question": "What has to be broken before you can use it?",                               "answer": "egg"},
    {"question": "What has words but never speaks?",                                           "answer": "book"},
    {"question": "The more of this there is, the less you see. What is it?",                   "answer": "darkness"},
    {"question": "I'm tall when I'm young and short when I'm old. What am I?",                 "answer": "candle"},
    {"question": "What goes up but never comes down?",                                         "answer": "age"},
    {"question": "What gets wetter as it dries?",                                              "answer": "towel"},
    {"question": "What begins with T, ends with T, and has T in it?",                          "answer": "teapot"},
    {"question": "I'm always hungry and must be fed, but if you give me water I will die. What am I?", "answer": "fire"},
    {"question": "What can travel around the world while staying in a corner?",                 "answer": "stamp"},
    {"question": "What has one eye but can't see?",                                            "answer": "needle"},
    {"question": "I'm light as a feather, yet the strongest man cannot hold me for much longer than a minute. What am I?", "answer": "breath"},
    {"question": "What has a neck but no head?",                                               "answer": "bottle"},
    {"question": "What comes down but never goes up?",                                         "answer": "rain"},
    {"question": "I have branches but no fruit, trunk, or leaves. What am I?",                 "answer": "bank"},
    {"question": "What runs but never walks?",                                                 "answer": "river"},
    {"question": "What can fill a room but takes up no space?",                                "answer": "light"},
    {"question": "If you drop me I'm sure to crack, but give me a smile and I'll always smile back. What am I?", "answer": "mirror"},
    {"question": "The more you take, the more you leave behind. What am I?",                   "answer": "footsteps"},
    {"question": "What has a head and a tail but no body?",                                    "answer": "coin"},
    {"question": "What is so fragile that saying its name breaks it?",                         "answer": "silence"},
    {"question": "I am always in front of you but can't be seen. What am I?",                  "answer": "future"},
    {"question": "I am full of holes but still holds water. What am I?",                       "answer": "sponge"},
    {"question": "What has many teeth, but can't bite?",                                       "answer": "comb"},
    {"question": "I'm often running yet I have no legs. What am I?",                           "answer": "water"},
    {"question": "What invention lets you look right through a wall?",                         "answer": "window"},
    {"question": "I'm found in socks, scarves and mittens; and often in the paws of playful kittens. What am I?", "answer": "yarn"},
    {"question": "What begins with an E, ends with an E, but only contains one letter?",       "answer": "envelope"},
]
used_riddles = []


def puzzle_life():
    global used_riddles
    available = [r for r in riddles if r not in used_riddles]
    if not available:
        used_riddles = []
        available = riddles.copy()
    riddle = random.choice(available)
    used_riddles.append(riddle)

    correct = riddle["answer"]
    options = [correct] + random.sample(
        [r["answer"] for r in riddles if r["answer"] != correct], 3)
    random.shuffle(options)
    letters  = ["A", "B", "C", "D"]
    selected = 0

    asking = True
    while asking:
        screen.fill(BLACK)
        prompt = option_font.render(f"Riddle: {riddle['question']}", True, WHITE)
        screen.blit(prompt, [WIDTH//2 - prompt.get_width()//2, HEIGHT*0.15])
        for i, opt in enumerate(options):
            color = HIGHLIGHT if i == selected else WHITE
            text  = option_font.render(f"{letters[i]}. {opt}", True, color)
            screen.blit(text, [WIDTH//2 - text.get_width()//2, HEIGHT*0.3 + i*HEIGHT*0.08])
        info = small_font.render("Use UP/DOWN to select, ENTER to confirm", True, WHITE)
        screen.blit(info, [WIDTH//2 - info.get_width()//2, HEIGHT*0.8])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    selected = (selected - 1) % 4
                elif event.key == pygame.K_DOWN: selected = (selected + 1) % 4
                elif event.key == pygame.K_RETURN: asking = False

    return options[selected].lower() == correct.lower()


# ================================================================
# SHARED HELPERS
# ================================================================
def random_food(snake=[], obstacles=[], snake2=[]):
    while True:
        x = random.randrange(BLOCK, WIDTH  - BLOCK, BLOCK)
        y = random.randrange(BLOCK, HEIGHT - BLOCK, BLOCK)
        if (x, y) not in snake and (x, y) not in obstacles and (x, y) not in snake2:
            break
    r = random.random()
    if   r < 0.1: return {"type": "golden",  "position": (x, y)}
    elif r < 0.2: return {"type": "poison",  "position": (x, y)}
    else:         return {"type": "normal",  "position": (x, y)}


def draw_grid():
    for x in range(BLOCK, WIDTH  - BLOCK, BLOCK):
        pygame.draw.line(screen, DARK_GRAY, (x, BLOCK), (x, HEIGHT - BLOCK))
    for y in range(BLOCK, HEIGHT - BLOCK, BLOCK):
        pygame.draw.line(screen, DARK_GRAY, (BLOCK, y), (WIDTH - BLOCK, y))


def draw_walls(obstacles=[]):
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.rect(screen, BRICK_COLOR, (x, 0,            BLOCK, BLOCK))
        pygame.draw.rect(screen, BRICK_COLOR, (x, HEIGHT-BLOCK, BLOCK, BLOCK))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.rect(screen, BRICK_COLOR, (0,            y, BLOCK, BLOCK))
        pygame.draw.rect(screen, BRICK_COLOR, (WIDTH-BLOCK,  y, BLOCK, BLOCK))
    for ox, oy in obstacles:
        pygame.draw.rect(screen, BRICK_COLOR, (ox, oy, BLOCK, BLOCK))


def draw_snake(snake_list, direction, tongue_phase,
               head_color=GREEN_HEAD, body_color=GREEN_BODY):
    for i, (x, y) in enumerate(snake_list):
        if head_color == BLUE_HEAD:
            fade  = max(50, body_color[2] - i * 5)
            color = head_color if i == 0 else (body_color[0], body_color[1], fade)
        else:
            fade  = max(50, body_color[1] - i * 5)
            color = head_color if i == 0 else (body_color[0], fade, body_color[2])
        pygame.draw.rect(screen, color, (x, y, BLOCK, BLOCK),
                         border_radius=8 if i == 0 else 6)

    hx, hy       = snake_list[0]
    eye_off      = BLOCK // 4
    pr           = 3

    if direction == 'UP':
        pygame.draw.circle(screen, WHITE, (hx + eye_off,   hy + 5), pr)
        pygame.draw.circle(screen, WHITE, (hx + 3*eye_off, hy + 5), pr)
        if tongue_phase % 20 < 10:
            pygame.draw.line(screen, TONGUE_COLOR, (hx+BLOCK//2, hy), (hx+BLOCK//2, hy-5), 2)
    elif direction == 'DOWN':
        pygame.draw.circle(screen, WHITE, (hx + eye_off,   hy + BLOCK - 5), pr)
        pygame.draw.circle(screen, WHITE, (hx + 3*eye_off, hy + BLOCK - 5), pr)
        if tongue_phase % 20 < 10:
            pygame.draw.line(screen, TONGUE_COLOR, (hx+BLOCK//2, hy+BLOCK), (hx+BLOCK//2, hy+BLOCK+5), 2)
    elif direction == 'LEFT':
        pygame.draw.circle(screen, WHITE, (hx + 5, hy + eye_off),   pr)
        pygame.draw.circle(screen, WHITE, (hx + 5, hy + 3*eye_off), pr)
        if tongue_phase % 20 < 10:
            pygame.draw.line(screen, TONGUE_COLOR, (hx, hy+BLOCK//2), (hx-5, hy+BLOCK//2), 2)
    elif direction == 'RIGHT':
        pygame.draw.circle(screen, WHITE, (hx + BLOCK - 5, hy + eye_off),   pr)
        pygame.draw.circle(screen, WHITE, (hx + BLOCK - 5, hy + 3*eye_off), pr)
        if tongue_phase % 20 < 10:
            pygame.draw.line(screen, TONGUE_COLOR, (hx+BLOCK, hy+BLOCK//2), (hx+BLOCK+5, hy+BLOCK//2), 2)


def draw_food(food, phase):
    x, y   = food["position"]
    radius = BLOCK // 2 + int(3 * math.sin(phase / 5))
    if   food["type"] == "normal": pygame.draw.circle(screen, RED,    (x+BLOCK//2, y+BLOCK//2), radius)
    elif food["type"] == "golden": pygame.draw.circle(screen, YELLOW, (x+BLOCK//2, y+BLOCK//2), radius)
    elif food["type"] == "poison": pygame.draw.circle(screen, PURPLE, (x+BLOCK//2, y+BLOCK//2), radius)


def show_info(score, lives, fps):
    screen.blit(option_font.render(f"Score: {score}", True, WHITE), (10, 5))
    screen.blit(option_font.render(f"Lives: {lives}", True, WHITE), (WIDTH-180, 5))
    screen.blit(option_font.render(f"Speed: {fps}",  True, WHITE), (WIDTH//2-50, 5))


def show_info_multi(score1, lives1, score2, lives2, fps):
    p1s = option_font.render(f"P1  Score:{score1}  Lives:{lives1}", True, GREEN_HEAD)
    p2s = option_font.render(f"Score:{score2}  Lives:{lives2}  P2", True, BLUE_HEAD)
    sp  = option_font.render(f"Spd:{fps}", True, WHITE)
    screen.blit(p1s, (10, 5))
    screen.blit(sp,  (WIDTH//2 - sp.get_width()//2, 5))
    screen.blit(p2s, (WIDTH - p2s.get_width() - 10, 5))


def make_obstacles():
    obs = []
    for i in range(5, WIDTH//BLOCK - 5, 6):
        obs.append((i * BLOCK, HEIGHT // 2))
    for i in range(5, HEIGHT//BLOCK - 5, 6):
        obs.append((WIDTH // 3, i * BLOCK))
    return obs


# ================================================================
# GAME-OVER SCREENS
# ================================================================
def game_over_screen(score):
    screen.fill(BLACK)
    msg = big_font.render("Game Over!", True, RED)
    sub = option_font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(msg, [WIDTH//2 - msg.get_width()//2, HEIGHT//3])
    screen.blit(sub, [WIDTH//2 - sub.get_width()//2, HEIGHT//2])
    pygame.display.update()
    pygame.time.delay(3000)


def multiplayer_over_screen(winner, score1, score2):
    """
    winner: 1  → P1 wins
            2  → P2 wins
            0  → tie (simultaneous death, shouldn't happen but handled)
    """
    screen.fill(BLACK)
    if winner == 1:
        w_text  = big_font.render("Player 1 Wins!", True, GREEN_HEAD)
        d_text  = option_font.render("Player 2 has been eliminated!", True, RED)
    elif winner == 2:
        w_text  = big_font.render("Player 2 Wins!", True, BLUE_HEAD)
        d_text  = option_font.render("Player 1 has been eliminated!", True, RED)
    else:
        w_text  = big_font.render("It's a Draw!", True, YELLOW)
        d_text  = option_font.render("Both players fell at the same time!", True, GRAY)

    s1 = option_font.render(f"P1 Score: {score1}", True, GREEN_HEAD)
    s2 = option_font.render(f"P2 Score: {score2}", True, BLUE_HEAD)

    screen.blit(w_text, [WIDTH//2 - w_text.get_width()//2, HEIGHT*0.18])
    screen.blit(d_text, [WIDTH//2 - d_text.get_width()//2, HEIGHT*0.38])
    screen.blit(s1,     [WIDTH//2 - s1.get_width()//2,     HEIGHT*0.52])
    screen.blit(s2,     [WIDTH//2 - s2.get_width()//2,     HEIGHT*0.62])
    pygame.display.update()
    pygame.time.delay(4000)


# ================================================================
# SINGLE-PLAYER GAME  (unchanged from original)
# ================================================================
def main_single(speed, lives, use_obstacles):
    snake        = [(100, 100)]
    dx, dy       = BLOCK, 0
    FPS          = speed
    score        = 0
    tongue_phase = 0
    food_phase   = 0
    direction    = 'RIGHT'

    obstacles = make_obstacles() if use_obstacles else []
    food      = random_food(snake, obstacles)
    running   = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if   event.key == pygame.K_UP    and dy == 0: dx, dy = 0, -BLOCK; direction = 'UP'
                elif event.key == pygame.K_DOWN  and dy == 0: dx, dy = 0,  BLOCK; direction = 'DOWN'
                elif event.key == pygame.K_LEFT  and dx == 0: dx, dy = -BLOCK, 0; direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy =  BLOCK, 0; direction = 'RIGHT'
                elif event.key == pygame.K_w: FPS = min(FPS + 1, 25)
                elif event.key == pygame.K_s: FPS = max(FPS - 1, 5)

        hx, hy   = snake[0]
        new_head = (hx + dx, hy + dy)

        collision = (new_head[0] < BLOCK or new_head[0] >= WIDTH - BLOCK or
                     new_head[1] < BLOCK or new_head[1] >= HEIGHT - BLOCK or
                     new_head in snake or new_head in obstacles)

        if collision:
            solved = puzzle_life()
            lives  = lives + 1 if solved else lives - 1
            if lives == 0:
                running = False
            snake     = [(100, 100)]
            dx, dy    = BLOCK, 0
            direction = 'RIGHT'
            new_head  = snake[0]
            pygame.time.delay(500)

        snake.insert(0, new_head)

        if new_head == food["position"]:
            if food["type"] == "normal":
                score += 1
                if eat_sound: eat_sound.play()
            elif food["type"] == "golden":
                score += 5
                if eat_sound: eat_sound.play()
            elif food["type"] == "poison":
                solved = puzzle_life()
                lives  = lives + 1 if solved else lives - 1
                if lives == 0:
                    running = False
            food = random_food(snake, obstacles)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_walls(obstacles)
        draw_grid()
        draw_snake(snake, direction, tongue_phase)
        draw_food(food, food_phase)
        show_info(score, lives, FPS)

        pygame.display.update()
        clock.tick(FPS)
        tongue_phase += 1
        food_phase   += 1

    game_over_screen(score)


# ================================================================
# MULTIPLAYER GAME
# P1 = Green  → Arrow keys
# P2 = Blue   → WASD
#
# Each player starts with the chosen number of lives.
# Collision → lose 1 life + brief respawn flash.
# Lives reach 0 → that player is DEAD → other player WINS instantly.
# Simultaneous death → draw.
# ================================================================
def main_multi(speed, lives_start, use_obstacles):
    # --- State ---
    snake1 = [(200, 200)]
    snake2 = [(700, 400)]
    dx1, dy1 = BLOCK,  0
    dx2, dy2 = -BLOCK, 0
    dir1 = 'RIGHT'
    dir2 = 'LEFT'
    FPS  = speed

    score1 = 0
    score2 = 0
    lives1 = lives_start
    lives2 = lives_start

    tongue1    = 0
    tongue2    = 0
    food_phase = 0

    # Respawn flash: counts down frames; snake is invisible while odd 5-frame blocks
    flash1 = 0   # >0 → P1 just respawned, flash effect
    flash2 = 0

    dead1  = False
    dead2  = False

    obstacles = make_obstacles() if use_obstacles else []
    food      = random_food(snake1, obstacles, snake2)
    running   = True

    def respawn1():
        nonlocal snake1, dx1, dy1, dir1, flash1
        snake1 = [(200, 200)]
        dx1, dy1 = BLOCK, 0
        dir1  = 'RIGHT'
        flash1 = 60   # ~1 s flash

    def respawn2():
        nonlocal snake2, dx2, dy2, dir2, flash2
        snake2 = [(700, 400)]
        dx2, dy2 = -BLOCK, 0
        dir2  = 'LEFT'
        flash2 = 60

    while running:
        # ---- Events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                # P1
                if not dead1 and flash1 == 0:
                    if   event.key == pygame.K_UP    and dy1 == 0: dx1, dy1 = 0, -BLOCK; dir1 = 'UP'
                    elif event.key == pygame.K_DOWN  and dy1 == 0: dx1, dy1 = 0,  BLOCK; dir1 = 'DOWN'
                    elif event.key == pygame.K_LEFT  and dx1 == 0: dx1, dy1 = -BLOCK, 0; dir1 = 'LEFT'
                    elif event.key == pygame.K_RIGHT and dx1 == 0: dx1, dy1 =  BLOCK, 0; dir1 = 'RIGHT'
                # P2
                if not dead2 and flash2 == 0:
                    if   event.key == pygame.K_w and dy2 == 0: dx2, dy2 = 0, -BLOCK; dir2 = 'UP'
                    elif event.key == pygame.K_s and dy2 == 0: dx2, dy2 = 0,  BLOCK; dir2 = 'DOWN'
                    elif event.key == pygame.K_a and dx2 == 0: dx2, dy2 = -BLOCK, 0; dir2 = 'LEFT'
                    elif event.key == pygame.K_d and dx2 == 0: dx2, dy2 =  BLOCK, 0; dir2 = 'RIGHT'

        # ---- Move P1 ----
        if not dead1 and flash1 == 0:
            hx1, hy1 = snake1[0]
            nh1      = (hx1 + dx1, hy1 + dy1)
            hit1     = (nh1[0] < BLOCK or nh1[0] >= WIDTH  - BLOCK or
                        nh1[1] < BLOCK or nh1[1] >= HEIGHT - BLOCK or
                        nh1 in snake1 or nh1 in obstacles or nh1 in snake2)
            if hit1:
                lives1 -= 1
                if lives1 <= 0:
                    dead1 = True
                else:
                    respawn1()
                    nh1 = snake1[0]
            if not dead1:
                snake1.insert(0, nh1)
                if nh1 == food["position"]:
                    if food["type"] == "normal":
                        score1 += 1
                        if eat_sound: eat_sound.play()
                    elif food["type"] == "golden":
                        score1 += 5
                        if eat_sound: eat_sound.play()
                    elif food["type"] == "poison":
                        lives1 -= 1
                        if lives1 <= 0:
                            dead1 = True
                    food = random_food(snake1, obstacles, snake2)
                else:
                    snake1.pop()
        elif flash1 > 0:
            flash1 -= 1

        # ---- Move P2 ----
        if not dead2 and flash2 == 0:
            hx2, hy2 = snake2[0]
            nh2      = (hx2 + dx2, hy2 + dy2)
            hit2     = (nh2[0] < BLOCK or nh2[0] >= WIDTH  - BLOCK or
                        nh2[1] < BLOCK or nh2[1] >= HEIGHT - BLOCK or
                        nh2 in snake2 or nh2 in obstacles or nh2 in snake1)
            if hit2:
                lives2 -= 1
                if lives2 <= 0:
                    dead2 = True
                else:
                    respawn2()
                    nh2 = snake2[0]
            if not dead2:
                snake2.insert(0, nh2)
                if nh2 == food["position"]:
                    if food["type"] == "normal":
                        score2 += 1
                        if eat_sound: eat_sound.play()
                    elif food["type"] == "golden":
                        score2 += 5
                        if eat_sound: eat_sound.play()
                    elif food["type"] == "poison":
                        lives2 -= 1
                        if lives2 <= 0:
                            dead2 = True
                    food = random_food(snake1, obstacles, snake2)
                else:
                    snake2.pop()
        elif flash2 > 0:
            flash2 -= 1

        # ---- Win / lose check ----
        if dead1 or dead2:
            running = False

        # ---- Draw ----
        screen.fill(BLACK)
        draw_walls(obstacles)
        draw_grid()

        # P1: hidden when flash is in "off" half of cycle
        show_p1 = not dead1 and (flash1 == 0 or (flash1 // 6) % 2 == 0)
        show_p2 = not dead2 and (flash2 == 0 or (flash2 // 6) % 2 == 0)

        if show_p1: draw_snake(snake1, dir1, tongue1, GREEN_HEAD, GREEN_BODY)
        if show_p2: draw_snake(snake2, dir2, tongue2, BLUE_HEAD,  BLUE_BODY)

        draw_food(food, food_phase)
        show_info_multi(score1, lives1, score2, lives2, FPS)

        # Flash labels
        if flash1 > 0:
            lbl = small_font.render("P1 RESPAWNING...", True, GREEN_HEAD)
            screen.blit(lbl, [WIDTH//4 - lbl.get_width()//2, HEIGHT//2 - 20])
        if flash2 > 0:
            lbl = small_font.render("P2 RESPAWNING...", True, BLUE_HEAD)
            screen.blit(lbl, [3*WIDTH//4 - lbl.get_width()//2, HEIGHT//2 - 20])

        # Lives indicator dots
        for i in range(lives1):
            pygame.draw.circle(screen, GREEN_HEAD, (15 + i * 18, HEIGHT - 20), 6)
        for i in range(lives2):
            pygame.draw.circle(screen, BLUE_HEAD, (WIDTH - 15 - i * 18, HEIGHT - 20), 6)

        pygame.display.update()
        clock.tick(FPS)
        tongue1    += 1
        tongue2    += 1
        food_phase += 1

    # Determine winner
    if dead1 and dead2: winner = 0
    elif dead1:         winner = 2
    else:               winner = 1

    multiplayer_over_screen(winner, score1, score2)


# ================================================================
# RUN
# ================================================================
if __name__ == "__main__":
    speed, lives, use_obstacles, game_mode = menu()
    if game_mode == "single":
        main_single(speed, lives, use_obstacles)
    else:
        main_multi(speed, lives, use_obstacles)
    pygame.quit()
    sys.exit()
