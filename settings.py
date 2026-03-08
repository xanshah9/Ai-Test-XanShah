# settings.py - All constants, colors, and theme definitions

# Screen
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Super Mario Bros - Python Edition"

# Tile
TILE_SIZE = 32

# Physics
GRAVITY = 0.6
MAX_FALL_SPEED = 14
PLAYER_SPEED = 4.5
PLAYER_RUN_SPEED = 7.0
JUMP_FORCE = -14.0
JUMP_HOLD_FORCE = -0.6
MAX_JUMP_HOLD = 18
PLAYER_ACCEL = 0.8
PLAYER_FRICTION = 0.82

# Player sizes
PLAYER_SMALL_W = 28
PLAYER_SMALL_H = 44
PLAYER_BIG_W = 28
PLAYER_BIG_H = 56

# Lives & Score
STARTING_LIVES = 3
COIN_SCORE = 100
ENEMY_STOMP_SCORE = 200
POWERUP_SCORE = 1000
LEVEL_COMPLETE_SCORE = 5000

# Colors
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (220, 30, 30)
DARK_RED    = (150, 10, 10)
BLUE        = (40, 80, 220)
DARK_BLUE   = (20, 40, 140)
LIGHT_BLUE  = (135, 206, 250)
SKY_BLUE    = (100, 180, 255)
GREEN       = (60, 180, 60)
DARK_GREEN  = (30, 100, 30)
LIGHT_GREEN = (120, 220, 80)
BROWN       = (140, 80, 30)
DARK_BROWN  = (90, 50, 15)
YELLOW      = (255, 220, 0)
GOLD        = (255, 190, 0)
ORANGE      = (255, 130, 0)
PINK        = (255, 160, 180)
PURPLE      = (140, 40, 180)
GRAY        = (130, 130, 140)
LIGHT_GRAY  = (200, 200, 210)
DARK_GRAY   = (60, 60, 70)
LAVA_RED    = (220, 50, 0)
LAVA_ORANGE = (255, 120, 0)
LAVA_YELLOW = (255, 220, 50)
TAN         = (210, 170, 110)
CREAM       = (255, 235, 180)
CAVE_DARK   = (25, 18, 40)
CAVE_PURPLE = (60, 40, 80)
CAVE_STONE  = (80, 70, 90)
CASTLE_DARK = (35, 20, 20)
CASTLE_STONE= (70, 55, 55)
CLOUD_WHITE = (240, 248, 255)

# ─── Theme Definitions ────────────────────────────────────────────────────────
THEMES = {
    "green_hills": {
        "name": "World 1 – Green Hills",
        "bg_top":    (100, 200, 255),
        "bg_bottom": (160, 230, 255),
        "ground_top": GREEN,
        "ground_body": DARK_BROWN,
        "ground_edge": LIGHT_GREEN,
        "brick_color": (190, 100, 40),
        "brick_dark":  (140, 65, 20),
        "question_color": GOLD,
        "question_shine": YELLOW,
        "pipe_body":  (50, 160, 50),
        "pipe_rim":   (30, 120, 30),
        "cloud_color": CLOUD_WHITE,
        "hill_color":  (80, 170, 60),
        "hill_dark":   (50, 120, 40),
        "has_lava": False,
        "music_tempo": 120,
    },
    "cave": {
        "name": "World 2 – Underground Cave",
        "bg_top":    CAVE_DARK,
        "bg_bottom": CAVE_PURPLE,
        "ground_top": CAVE_STONE,
        "ground_body": (40, 30, 55),
        "ground_edge": (100, 80, 120),
        "brick_color": (90, 75, 100),
        "brick_dark":  (55, 45, 65),
        "question_color": GOLD,
        "question_shine": YELLOW,
        "pipe_body":  (40, 130, 40),
        "pipe_rim":   (20, 90, 20),
        "cloud_color": (80, 60, 100),
        "hill_color":  (50, 40, 65),
        "hill_dark":   (30, 22, 45),
        "has_lava": True,
        "music_tempo": 100,
    },
    "sky": {
        "name": "World 3 – Sky Islands",
        "bg_top":    (70, 160, 255),
        "bg_bottom": (160, 220, 255),
        "ground_top": (255, 255, 255),
        "ground_body": (220, 240, 255),
        "ground_edge": (200, 225, 255),
        "brick_color": (220, 200, 255),
        "brick_dark":  (180, 160, 220),
        "question_color": GOLD,
        "question_shine": YELLOW,
        "pipe_body":  (50, 200, 100),
        "pipe_rim":   (30, 150, 70),
        "cloud_color": CLOUD_WHITE,
        "hill_color":  (200, 230, 255),
        "hill_dark":   (160, 200, 240),
        "has_lava": False,
        "music_tempo": 140,
    },
    "lava_castle": {
        "name": "World 4 – Lava Castle",
        "bg_top":    CASTLE_DARK,
        "bg_bottom": (60, 20, 10),
        "ground_top": CASTLE_STONE,
        "ground_body": (45, 30, 30),
        "ground_edge": (90, 60, 55),
        "brick_color": (100, 60, 50),
        "brick_dark":  (65, 38, 30),
        "question_color": GOLD,
        "question_shine": YELLOW,
        "pipe_body":  (40, 40, 40),
        "pipe_rim":   (25, 25, 25),
        "cloud_color": (100, 60, 40),
        "hill_color":  (80, 40, 30),
        "hill_dark":   (55, 25, 18),
        "has_lava": True,
        "music_tempo": 110,
    },
}

THEME_ORDER = ["green_hills", "cave", "sky", "lava_castle"]

# Enemy types
ENEMY_GOOMBA       = "goomba"
ENEMY_KOOPA        = "koopa"
ENEMY_FLYING_KOOPA = "flying_koopa"
ENEMY_BOSS         = "boss"

# Power-up types
POWERUP_MUSHROOM = "mushroom"
POWERUP_STAR     = "star"
POWERUP_FIRE     = "fire_flower"

# Tile types
TILE_GROUND   = "ground"
TILE_BRICK    = "brick"
TILE_QUESTION = "question"
TILE_PIPE     = "pipe"
TILE_PLATFORM = "platform"
TILE_SOLID    = "solid"
TILE_LAVA     = "lava"
