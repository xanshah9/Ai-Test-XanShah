# levels.py - Level data definitions

from settings import *

# Each level dict:
#   ground_segments: list of (x, y, width, height) rects for ground tiles (in pixels, auto-tiled)
#   platforms:       list of (x, y, width, tile_type) floating platforms
#   bricks:          list of (x, y) brick block positions
#   questions:       list of (x, y, item_type) question blocks
#   pipes:           list of (x, y, height) pipes
#   enemies:         list of (x, y, enemy_type, patrol_dist)
#   coins:           list of (x, y) coin positions
#   moving_platforms:list of (x, y, width, move_type, range_val, speed)
#                      move_type = 'h' or 'v'
#   lava_pits:       list of (x, width) lava surface rects
#   flag_x:          x position of goal flag pole
#   start_x, start_y: player start

T = TILE_SIZE  # 32

def make_ground_row(x, y, tile_count):
    """Return a ground segment spanning tile_count tiles wide, 1 tile tall."""
    return (x, y, tile_count * T, T)

# ─── LEVEL 1 – Green Hills ─────────────────────────────────────────────────
LEVEL_1 = {
    "theme": "green_hills",
    "start_x": 80,
    "start_y": 500,
    "flag_x": 2900,
    "width": 3100,

    # Ground segments: (x, y, w, h) in pixels
    "ground_segments": [
        # Main ground runs from x=0 to x=500
        (0,    544, 500,  56),
        # gap at 500–560
        (560,  544, 640,  56),   # 560..1200
        # gap at 1200–1260
        (1260, 544, 700,  56),   # 1260..1960
        # gap at 1960–2040
        (2040, 544, 860,  56),   # 2040..2900+
    ],

    "platforms": [
        # (x, y, width_in_tiles, tile_type)
        (160,  448, 3, TILE_BRICK),
        (320,  384, 4, TILE_BRICK),
        (600,  416, 3, TILE_BRICK),
        (800,  352, 5, TILE_BRICK),
        (1040, 416, 3, TILE_BRICK),
        (1300, 384, 4, TILE_BRICK),
        (1500, 352, 3, TILE_BRICK),
        (1700, 416, 4, TILE_BRICK),
        (1900, 384, 3, TILE_BRICK),
        (2100, 352, 5, TILE_BRICK),
        (2400, 416, 3, TILE_BRICK),
        (2600, 384, 4, TILE_BRICK),
    ],

    "questions": [
        # (x, y, item_type)
        (192,  416, POWERUP_MUSHROOM),
        (352,  352, POWERUP_STAR),
        (832,  320, POWERUP_FIRE),
        (608,  384, "coin"),
        (640,  384, "coin"),
        (672,  384, "coin"),
        (1072, 384, "coin"),
        (1312, 352, POWERUP_MUSHROOM),
        (1732, 384, "coin"),
        (1764, 384, "coin"),
        (2432, 384, POWERUP_STAR),
        (2632, 352, "coin"),
    ],

    "bricks": [
        (224, 416), (256, 416),
        (384, 352), (416, 352), (448, 352),
        (864, 320), (896, 320),
        (1108, 416), (1140, 416),
        (1344, 352), (1376, 352),
        (1536, 320), (1568, 320),
        (2464, 384), (2496, 384),
        (2668, 352),
    ],

    "pipes": [
        # (x, y, height_in_tiles)
        (680,  480, 2),
        (900,  480, 3),
        (1450, 480, 2),
        (2200, 480, 2),
        (2700, 480, 3),
    ],

    "enemies": [
        # (x, y, type, patrol_dist)
        (400,  512, ENEMY_GOOMBA, 120),
        (700,  512, ENEMY_GOOMBA, 80),
        (1000, 512, ENEMY_GOOMBA, 100),
        (1400, 512, ENEMY_KOOPA,  150),
        (1800, 512, ENEMY_GOOMBA, 120),
        (2100, 512, ENEMY_GOOMBA, 80),
        (2500, 512, ENEMY_KOOPA,  140),
    ],

    "coins": [
        # Rows of coins
        *[(x, 500) for x in range(80, 460, 32)],
        *[(x, 468) for x in range(600, 750, 32)],
        *[(x, 500) for x in range(800, 1000, 32)],
        *[(x, 468) for x in range(1100, 1200, 32)],
        *[(x, 500) for x in range(1300, 1500, 32)],
        *[(x, 468) for x in range(1600, 1750, 32)],
        *[(x, 500) for x in range(2050, 2200, 32)],
        *[(x, 468) for x in range(2300, 2500, 32)],
        *[(x, 500) for x in range(2600, 2900, 32)],
    ],

    "moving_platforms": [],
    "lava_pits": [],

    "decorations": {
        "hills": [(100, 510), (500, 490), (900, 505), (1500, 510), (2000, 500), (2600, 510)],
        "clouds": [(150, 80), (350, 60), (600, 90), (900, 70), (1200, 85), (1600, 65), (2000, 80), (2400, 70), (2700, 85)],
    }
}

# ─── LEVEL 2 – Cave ────────────────────────────────────────────────────────
LEVEL_2 = {
    "theme": "cave",
    "start_x": 80,
    "start_y": 500,
    "flag_x": 2900,
    "width": 3100,

    "ground_segments": [
        (0,    544, 400,  56),
        # gap/lava 400-480
        (480,  544, 350,  56),
        # gap/lava 830-930
        (930,  544, 450,  56),
        # gap/lava 1380-1500
        (1500, 544, 400,  56),
        # gap/lava 1900-2020
        (2020, 544, 300,  56),
        # gap/lava 2320-2440
        (2440, 544, 660,  56),
    ],

    "platforms": [
        (100,  448, 3, TILE_BRICK),
        (280,  384, 4, TILE_BRICK),
        (500,  416, 3, TILE_BRICK),
        (700,  352, 5, TILE_BRICK),
        (950,  416, 4, TILE_BRICK),
        (1150, 352, 3, TILE_BRICK),
        (1320, 384, 3, TILE_BRICK),
        (1520, 416, 4, TILE_BRICK),
        (1740, 352, 3, TILE_BRICK),
        (1900, 320, 4, TILE_BRICK),
        (2050, 384, 3, TILE_BRICK),
        (2200, 352, 5, TILE_BRICK),
        (2460, 416, 3, TILE_BRICK),
        (2650, 384, 4, TILE_BRICK),
    ],

    "questions": [
        (132,  416, POWERUP_MUSHROOM),
        (312,  352, "coin"),
        (344,  352, "coin"),
        (732,  320, POWERUP_FIRE),
        (982,  384, "coin"),
        (1182, 320, POWERUP_MUSHROOM),
        (1550, 384, "coin"),
        (1582, 384, "coin"),
        (1932, 288, POWERUP_STAR),
        (2082, 352, "coin"),
        (2232, 320, "coin"),
        (2492, 384, POWERUP_MUSHROOM),
        (2682, 352, "coin"),
    ],

    "bricks": [
        (164, 416), (196, 416),
        (376, 352), (408, 352),
        (764, 320), (796, 320), (828, 320),
        (1016, 384), (1048, 384),
        (1214, 352), (1246, 352),
        (1614, 384), (1646, 384),
        (1772, 320), (1804, 320),
        (1964, 288),
        (2264, 320), (2296, 320),
        (2524, 384),
    ],

    "pipes": [
        (250,  480, 2),
        (600,  480, 3),
        (1050, 480, 2),
        (1600, 480, 3),
        (2100, 480, 2),
        (2550, 480, 2),
    ],

    "enemies": [
        (200,  512, ENEMY_GOOMBA, 100),
        (350,  512, ENEMY_GOOMBA, 80),
        (560,  512, ENEMY_KOOPA,  120),
        (800,  512, ENEMY_GOOMBA, 100),
        (1000, 512, ENEMY_GOOMBA, 90),
        (1200, 512, ENEMY_KOOPA,  130),
        (1550, 512, ENEMY_GOOMBA, 80),
        (1780, 512, ENEMY_GOOMBA, 100),
        (2060, 512, ENEMY_KOOPA,  120),
        (2300, 512, ENEMY_GOOMBA, 90),
        (2500, 512, ENEMY_GOOMBA, 100),
        (2700, 512, ENEMY_KOOPA,  140),
    ],

    "coins": [
        *[(x, 500) for x in range(60, 380, 32)],
        *[(x, 468) for x in range(490, 690, 32)],
        *[(x, 500) for x in range(940, 1130, 32)],
        *[(x, 468) for x in range(1200, 1380, 32)],
        *[(x, 500) for x in range(1510, 1700, 32)],
        *[(x, 468) for x in range(1900, 2000, 32)],
        *[(x, 500) for x in range(2030, 2310, 32)],
        *[(x, 468) for x in range(2450, 2700, 32)],
    ],

    "moving_platforms": [],

    "lava_pits": [
        (400, 80),   # x=400, width=80
        (830, 100),
        (1380, 120),
        (1900, 120),
        (2320, 120),
    ],

    "stalactites": [
        (100, 0), (200, 0), (350, 0), (500, 0), (650, 0), (800, 0),
        (950, 0), (1100, 0), (1250, 0), (1400, 0), (1600, 0),
        (1750, 0), (1900, 0), (2050, 0), (2200, 0), (2350, 0),
        (2500, 0), (2650, 0), (2800, 0),
    ],

    "decorations": {
        "hills": [],
        "clouds": [],
    }
}

# ─── LEVEL 3 – Sky Islands ──────────────────────────────────────────────────
LEVEL_3 = {
    "theme": "sky",
    "start_x": 80,
    "start_y": 400,
    "flag_x": 2900,
    "width": 3100,

    "ground_segments": [
        (0,   480, 300, 120),   # starter island
        # Big sky gap
        (500, 480, 200, 120),   # small island
        (800, 480, 250, 120),
        (1150,480, 200, 120),
        (1450,480, 300, 120),
        (1850,480, 200, 120),
        (2150,480, 250, 120),
        (2500,480, 200, 120),
        (2800,480, 300, 120),   # end island
    ],

    "platforms": [
        (350,  416, 3, TILE_BRICK),
        (550,  352, 4, TILE_BRICK),
        (750,  416, 3, TILE_BRICK),
        (1000, 352, 5, TILE_BRICK),
        (1220, 416, 3, TILE_BRICK),
        (1500, 352, 4, TILE_BRICK),
        (1700, 416, 3, TILE_BRICK),
        (1950, 352, 4, TILE_BRICK),
        (2200, 416, 3, TILE_BRICK),
        (2400, 352, 5, TILE_BRICK),
        (2650, 416, 3, TILE_BRICK),
    ],

    "questions": [
        (382,  384, POWERUP_MUSHROOM),
        (582,  320, POWERUP_STAR),
        (1032, 320, POWERUP_FIRE),
        (1252, 384, "coin"),
        (1532, 320, "coin"),
        (1564, 320, "coin"),
        (1982, 320, POWERUP_MUSHROOM),
        (2232, 384, "coin"),
        (2432, 320, POWERUP_STAR),
        (2682, 384, "coin"),
    ],

    "bricks": [
        (414, 384), (446, 384),
        (614, 320), (646, 320), (678, 320),
        (782, 416), (814, 416),
        (1064, 320), (1096, 320),
        (1286, 384),
        (1596, 320), (1628, 320),
        (1732, 416), (1764, 416),
        (2014, 320), (2046, 320),
        (2464, 320), (2496, 320), (2528, 320),
    ],

    "pipes": [
        (280,  416, 2),
        (860,  416, 2),
        (1500, 416, 2),
        (2150, 416, 2),
        (2860, 416, 2),
    ],

    "enemies": [
        (150,  448, ENEMY_GOOMBA,       100),
        (550,  448, ENEMY_FLYING_KOOPA,  0),
        (850,  448, ENEMY_GOOMBA,        120),
        (1050, 448, ENEMY_FLYING_KOOPA,  0),
        (1300, 448, ENEMY_KOOPA,         100),
        (1550, 448, ENEMY_FLYING_KOOPA,  0),
        (1750, 448, ENEMY_GOOMBA,        80),
        (1950, 448, ENEMY_FLYING_KOOPA,  0),
        (2200, 448, ENEMY_KOOPA,         120),
        (2450, 448, ENEMY_FLYING_KOOPA,  0),
        (2650, 448, ENEMY_GOOMBA,        90),
    ],

    "coins": [
        *[(x, 448) for x in range(80, 280, 32)],
        *[(x, 384) for x in range(360, 500, 32)],
        *[(x, 320) for x in range(560, 700, 32)],
        *[(x, 448) for x in range(810, 1000, 32)],
        *[(x, 384) for x in range(1160, 1300, 32)],
        *[(x, 320) for x in range(1460, 1640, 32)],
        *[(x, 448) for x in range(1860, 2000, 32)],
        *[(x, 384) for x in range(2160, 2320, 32)],
        *[(x, 320) for x in range(2510, 2650, 32)],
        *[(x, 448) for x in range(2810, 2950, 32)],
    ],

    "moving_platforms": [
        # (x, y, width_tiles, 'h'/'v', range_px, speed)
        (680,  416, 3, 'h', 160, 2.0),
        (1380, 384, 3, 'h', 140, 2.5),
        (2080, 416, 3, 'v',  80, 1.5),
    ],

    "lava_pits": [],

    "decorations": {
        "hills": [],
        "clouds": [
            (80, 50), (250, 30), (450, 60), (700, 40), (950, 55),
            (1150, 35), (1400, 60), (1650, 45), (1900, 30), (2150, 55),
            (2400, 40), (2650, 60), (2850, 35),
        ],
    }
}

# ─── LEVEL 4 – Lava Castle ──────────────────────────────────────────────────
LEVEL_4 = {
    "theme": "lava_castle",
    "start_x": 80,
    "start_y": 500,
    "flag_x": 2900,
    "width": 3100,

    "ground_segments": [
        (0,    544, 350,  56),
        # lava 350-480
        (480,  544, 300,  56),
        # lava 780-940
        (940,  544, 300,  56),
        # lava 1240-1400
        (1400, 544, 250,  56),
        # lava 1650-1820
        (1820, 544, 300,  56),
        # lava 2120-2300
        (2300, 544, 260,  56),
        # lava 2560-2700
        (2700, 544, 400,  56),
    ],

    "platforms": [
        (100,  448, 3, TILE_SOLID),
        (250,  384, 4, TILE_SOLID),
        (500,  416, 3, TILE_SOLID),
        (700,  352, 5, TILE_SOLID),
        (950,  416, 4, TILE_SOLID),
        (1150, 352, 3, TILE_SOLID),
        (1320, 384, 4, TILE_SOLID),
        (1420, 416, 3, TILE_SOLID),
        (1650, 352, 4, TILE_SOLID),
        (1820, 384, 3, TILE_SOLID),
        (2000, 352, 4, TILE_SOLID),
        (2150, 416, 3, TILE_SOLID),
        (2320, 352, 5, TILE_SOLID),
        (2500, 384, 3, TILE_SOLID),
        (2600, 320, 4, TILE_SOLID),
        (2750, 384, 3, TILE_SOLID),
    ],

    "questions": [
        (282,  352, POWERUP_STAR),
        (732,  320, POWERUP_FIRE),
        (982,  384, POWERUP_MUSHROOM),
        (1182, 320, "coin"),
        (1452, 384, "coin"),
        (1682, 320, POWERUP_STAR),
        (1852, 352, "coin"),
        (2032, 320, POWERUP_FIRE),
        (2352, 320, "coin"),
        (2532, 352, POWERUP_MUSHROOM),
        (2632, 288, POWERUP_STAR),
    ],

    "bricks": [
        (314, 352), (346, 352),
        (764, 320), (796, 320),
        (1014, 384), (1046, 384),
        (1214, 320), (1246, 320),
        (1484, 384),
        (1714, 320), (1746, 320),
        (1884, 352), (1916, 352),
        (2064, 320), (2096, 320),
        (2384, 320), (2416, 320), (2448, 320),
        (2664, 288), (2696, 288),
    ],

    "pipes": [
        (200,  480, 2),
        (600,  480, 3),
        (1000, 480, 2),
        (1500, 480, 2),
        (2000, 480, 3),
        (2400, 480, 2),
        (2800, 480, 2),
    ],

    "enemies": [
        (150,  512, ENEMY_GOOMBA,  80),
        (280,  512, ENEMY_GOOMBA,  80),
        (550,  512, ENEMY_KOOPA,   120),
        (700,  512, ENEMY_GOOMBA,  80),
        (960,  512, ENEMY_GOOMBA,  100),
        (1100, 512, ENEMY_KOOPA,   130),
        (1250, 512, ENEMY_GOOMBA,  80),
        (1420, 512, ENEMY_KOOPA,   120),
        (1650, 512, ENEMY_GOOMBA,  80),
        (1840, 512, ENEMY_GOOMBA,  100),
        (2000, 512, ENEMY_KOOPA,   130),
        (2150, 512, ENEMY_GOOMBA,  80),
        (2310, 512, ENEMY_GOOMBA,  100),
        (2500, 512, ENEMY_KOOPA,   120),
        (2650, 512, ENEMY_GOOMBA,  80),
        (2750, 512, ENEMY_GOOMBA,  80),
        # Boss at end
        (2820, 470, ENEMY_BOSS,    100),
    ],

    "coins": [
        *[(x, 500) for x in range(60, 330, 32)],
        *[(x, 468) for x in range(490, 760, 32)],
        *[(x, 500) for x in range(950, 1220, 32)],
        *[(x, 468) for x in range(1310, 1490, 32)],
        *[(x, 500) for x in range(1410, 1640, 32)],
        *[(x, 468) for x in range(1830, 2110, 32)],
        *[(x, 500) for x in range(2310, 2540, 32)],
        *[(x, 468) for x in range(2650, 2870, 32)],
    ],

    "moving_platforms": [
        (400,  416, 3, 'h', 160, 2.0),
        (1100, 384, 3, 'h', 140, 2.5),
        (1900, 352, 3, 'v',  80, 1.8),
        (2450, 384, 3, 'h', 120, 2.2),
    ],

    "lava_pits": [
        (350, 130),
        (780, 160),
        (1240, 160),
        (1650, 170),
        (2120, 180),
        (2560, 140),
    ],

    "decorations": {
        "hills": [],
        "clouds": [(200, 100), (600, 80), (1000, 100), (1500, 90), (2000, 80), (2500, 100)],
    }
}

ALL_LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4]
