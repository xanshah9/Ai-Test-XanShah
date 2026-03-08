# game.py - Main Game class with all states and game loop

import pygame
import math
import random
import colorsys
from settings import *
from levels import ALL_LEVELS
from sprites import (
    Player, Enemy, Coin, PowerUp, Fireball,
    Tile, BrickBlock, QuestionBlock, Pipe, MovingPlatform, FlagPole,
    Particle, FloatingText
)


def lerp(a, b, t):
    return a + (b - a) * t


# ══════════════════════════════════════════════════════════════════════════════
#  SOLID RECT  (big ground block, no image needed)
# ══════════════════════════════════════════════════════════════════════════════

class _SolidRect:
    """One large solid collision rectangle representing a ground segment body."""
    def __init__(self, x, y, w, h, theme):
        self.rect = pygame.Rect(x, y, w, h)
        self.solid = True
        self.tile_type = TILE_GROUND
        self.theme = theme

    def draw(self, surf, cam_x):
        pass  # Ground is drawn separately in Level._draw_ground()


# ══════════════════════════════════════════════════════════════════════════════
#  BACKGROUND RENDERER
# ══════════════════════════════════════════════════════════════════════════════

class BackgroundRenderer:
    def __init__(self, theme_key, level_width):
        self.theme_key = theme_key
        self.theme = THEMES[theme_key]
        self.level_width = level_width
        random.seed(theme_key + "bg")
        self.cloud_positions = self._gen_clouds()
        self.hill_positions  = self._gen_hills()
        random.seed()

    def _gen_clouds(self):
        positions = []
        for i in range(30):
            x = random.randint(0, self.level_width)
            y = random.randint(20, 160)
            w = random.randint(60, 140)
            positions.append((x, y, w))
        return positions

    def _gen_hills(self):
        if self.theme_key in ("cave", "lava_castle"):
            return []
        positions = []
        for i in range(20):
            x = random.randint(0, self.level_width)
            h = random.randint(60, 140)
            w = random.randint(80, 200)
            positions.append((x, h, w))
        return positions

    def draw(self, surf, cam_x):
        th = self.theme
        # Sky gradient (draw per-scanline)
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(th["bg_top"][0] * (1-t) + th["bg_bottom"][0] * t)
            g = int(th["bg_top"][1] * (1-t) + th["bg_bottom"][1] * t)
            b = int(th["bg_top"][2] * (1-t) + th["bg_bottom"][2] * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Hills with parallax factor 0.3
        for (hx, hh, hw) in self.hill_positions:
            sx = int(hx - cam_x * 0.3) % (self.level_width + 400) - 200
            by = SCREEN_HEIGHT - 56
            pygame.draw.ellipse(surf, th["hill_color"],
                                (sx - hw//2, by - hh, hw, hh + 20))
            pygame.draw.ellipse(surf, th["hill_dark"],
                                (sx - hw//2 + 10, by - hh + 10, hw - 20, max(10, hh-10)))

        # Cave stalactites
        if self.theme_key == "cave":
            for i in range(0, self.level_width, 90):
                sx = int(i - cam_x * 0.8)
                stag_h = 40 + (i % 4) * 14
                if -20 < sx < SCREEN_WIDTH + 20:
                    pygame.draw.polygon(surf, CAVE_STONE,
                                        [(sx, 0), (sx+16, 0), (sx+8, stag_h)])
                    pygame.draw.polygon(surf, tuple(min(255, c+20) for c in CAVE_STONE),
                                        [(sx+2, 0), (sx+8, 0), (sx+4, stag_h//2)])

        # Lava glow at bottom for lava themes
        if self.theme_key in ("cave", "lava_castle"):
            for y in range(SCREEN_HEIGHT - 80, SCREEN_HEIGHT):
                alpha = (y - (SCREEN_HEIGHT - 80)) / 80.0
                rr = int(lerp(0, 200, alpha))
                gg = int(lerp(0, 30, alpha))
                pygame.draw.line(surf, (rr, gg, 0), (0, y), (SCREEN_WIDTH, y))

        # Distant stars for castle
        if self.theme_key == "lava_castle":
            random.seed(99)
            for _ in range(50):
                sx2 = random.randint(0, SCREEN_WIDTH)
                sy2 = random.randint(0, SCREEN_HEIGHT // 2)
                pygame.draw.circle(surf, WHITE, (sx2, sy2), 1)
            random.seed()

        # Clouds with parallax factor 0.6
        for (cx, cy, cw) in self.cloud_positions:
            sx = int(cx - cam_x * 0.6) % (self.level_width + 400) - 200
            self._draw_cloud(surf, sx, cy, cw)

    def _draw_cloud(self, surf, x, y, w):
        col = self.theme["cloud_color"]
        h = max(15, w // 3)
        pygame.draw.ellipse(surf, col, (x,       y,       w,      h))
        pygame.draw.ellipse(surf, col, (x+w//5,  y-h//2,  w*2//3, h))
        pygame.draw.ellipse(surf, col, (x+w//2,  y-h//4,  w//2,   h*2//3))
        dark = tuple(max(0, c-20) for c in col)
        pygame.draw.ellipse(surf, dark, (x+5, y+h//2, max(5, w-10), max(5, h//3)))


# ══════════════════════════════════════════════════════════════════════════════
#  HUD
# ══════════════════════════════════════════════════════════════════════════════

class HUD:
    def __init__(self):
        self.font_big  = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_med  = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_sml  = pygame.font.SysFont("Arial", 14, bold=True)

    def draw(self, surf, score, coins, lives, level_num, player_state, star_timer):
        # Translucent HUD bar
        hud_surf = pygame.Surface((SCREEN_WIDTH, 42), pygame.SRCALPHA)
        hud_surf.fill((0, 0, 0, 170))
        surf.blit(hud_surf, (0, 0))

        # Score
        self._draw_mini_star(surf, 10, 10)
        score_text = self.font_big.render(f"{score:08d}", True, WHITE)
        surf.blit(score_text, (28, 8))

        # Coin icon + count
        self._draw_mini_coin(surf, 175, 11)
        coin_text = self.font_big.render(f"x{coins:02d}", True, YELLOW)
        surf.blit(coin_text, (193, 8))

        # Lives
        self._draw_mini_mario(surf, 270, 8)
        life_text = self.font_big.render(f"x{lives}", True, WHITE)
        surf.blit(life_text, (292, 8))

        # Level name
        theme_name = THEMES[THEME_ORDER[min(level_num-1, len(THEME_ORDER)-1)]]["name"]
        lvl_text = self.font_med.render(theme_name, True, CREAM)
        surf.blit(lvl_text, (SCREEN_WIDTH//2 - lvl_text.get_width()//2, 12))

        # Player state
        state_colors = {"small": LIGHT_GRAY, "big": LIGHT_GREEN, "fire": ORANGE}
        sc = state_colors.get(player_state, WHITE)
        st = self.font_sml.render(player_state.upper(), True, sc)
        surf.blit(st, (SCREEN_WIDTH - 140, 6))

        # Star indicator
        if star_timer > 0:
            blink_alpha = 180 + int(math.sin(pygame.time.get_ticks() * 0.015) * 75)
            star_surf = self.font_med.render("STAR!", True, YELLOW)
            star_surf.set_alpha(blink_alpha)
            surf.blit(star_surf, (SCREEN_WIDTH - 140, 22))

        # Pause hint
        ph = self.font_sml.render("[P] Pause", True, LIGHT_GRAY)
        surf.blit(ph, (SCREEN_WIDTH - ph.get_width() - 4, 28))

    def _draw_mini_star(self, surf, x, y):
        pts = []
        cx, cy = x+10, y+12
        for i in range(10):
            angle = math.pi/2 + i * math.pi/5
            r = 9 if i % 2 == 0 else 4
            pts.append((cx + r*math.cos(angle), cy - r*math.sin(angle)))
        pygame.draw.polygon(surf, YELLOW, pts)

    def _draw_mini_coin(self, surf, x, y):
        pygame.draw.ellipse(surf, GOLD, (x, y, 12, 18))
        pygame.draw.ellipse(surf, YELLOW, (x+2, y+2, 8, 14))

    def _draw_mini_mario(self, surf, x, y):
        pygame.draw.rect(surf, RED,  (x, y, 20, 8), border_radius=2)
        pygame.draw.rect(surf, RED,  (x+3, y-5, 14, 8), border_radius=2)
        pygame.draw.ellipse(surf, TAN, (x+2, y+5, 16, 14))
        pygame.draw.ellipse(surf, DARK_BROWN, (x, y+16, 9, 6))
        pygame.draw.ellipse(surf, DARK_BROWN, (x+11, y+16, 9, 6))


# ══════════════════════════════════════════════════════════════════════════════
#  LEVEL
# ══════════════════════════════════════════════════════════════════════════════

class Level:
    def __init__(self, data):
        self.data = data
        self.theme_key = data["theme"]
        self.theme = THEMES[self.theme_key]
        self.width = data["width"]

        self.solid_tiles    = []   # all solid objects (for collision)
        self.draw_tiles     = []   # tiles that draw themselves
        self.bricks         = []
        self.questions      = []
        self.pipes          = []
        self.enemies        = []
        self.coins          = []
        self.powerups       = []
        self.fireballs      = []
        self.moving_platforms = []
        self.particles      = []
        self.floating_texts = []
        self.lava_rects     = []

        self._build()
        self.flag = FlagPole(data["flag_x"], self.theme_key)
        self.bg   = BackgroundRenderer(self.theme_key, self.width)
        self.completed    = False
        self.complete_timer = 0

    # ── BUILD ────────────────────────────────────────────────────────────────

    def _build(self):
        d = self.data
        T = TILE_SIZE

        # Ground segments — one _SolidRect per segment (for efficient collision)
        for (gx, gy, gw, gh) in d.get("ground_segments", []):
            sr = _SolidRect(gx, gy, gw, gh, self.theme_key)
            self.solid_tiles.append(sr)

        # Floating platforms
        for plat in d.get("platforms", []):
            px, py, pw, ptype = plat
            for i in range(pw):
                tile = Tile(px + i*T, py, ptype, self.theme_key)
                self.solid_tiles.append(tile)
                self.draw_tiles.append(tile)

        # Brick blocks
        for (bx, by) in d.get("bricks", []):
            brick = BrickBlock(bx, by, self.theme_key)
            self.bricks.append(brick)
            self.solid_tiles.append(brick)

        # Question blocks
        for q in d.get("questions", []):
            qx, qy, qitem = q
            qblock = QuestionBlock(qx, qy, self.theme_key, qitem)
            self.questions.append(qblock)
            self.solid_tiles.append(qblock)

        # Pipes
        for pipe_data in d.get("pipes", []):
            px, py, ph = pipe_data
            pipe = Pipe(px, py, ph, self.theme_key)
            self.pipes.append(pipe)
            # Pipe uses 2-tile width — add solid rect for it
            pipe_solid = _SolidRect(px, pipe.rect.y, TILE_SIZE*2, pipe.rect.height, self.theme_key)
            self.solid_tiles.append(pipe_solid)

        # Enemies
        for edata in d.get("enemies", []):
            ex, ey, etype, epatrol = edata
            enemy = Enemy(ex, ey, etype, epatrol)
            self.enemies.append(enemy)

        # Coins
        for (cx, cy) in d.get("coins", []):
            self.coins.append(Coin(cx, cy))

        # Moving platforms
        for mp in d.get("moving_platforms", []):
            mpx, mpy, mpw, mpt, mpr, mps = mp
            mplat = MovingPlatform(mpx, mpy, mpw, mpt, mpr, mps, self.theme_key)
            self.moving_platforms.append(mplat)
            self.solid_tiles.append(mplat)

        # Lava pits
        for (lx, lw) in d.get("lava_pits", []):
            self.lava_rects.append(pygame.Rect(lx, 544, lw, 60))

    # ── ACCESSORS ────────────────────────────────────────────────────────────

    def get_solid_tiles(self):
        """Return all current solid tiles (excluding dead bricks)."""
        return [t for t in self.solid_tiles
                if not (isinstance(t, BrickBlock) and not t.alive)]

    def get_player_solid(self):
        """Solid tiles relevant for player (and enemy) physics."""
        return self.get_solid_tiles()

    # ── SPAWN HELPERS ────────────────────────────────────────────────────────

    def spawn_powerup(self, x, y, item_type):
        if item_type == "coin":
            # Coin pop — particle burst only
            for _ in range(6):
                self.particles.append(
                    Particle(x+16, y, GOLD,
                             random.uniform(-2, 2), random.uniform(-7, -3),
                             35, 6, 0.25))
            return None
        pu = PowerUp(x, y, item_type)
        self.powerups.append(pu)
        return pu

    def spawn_particles(self, x, y, color, count=8, size=5):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, size=size))

    def spawn_brick_particles(self, x, y, color):
        for _ in range(10):
            dx = random.uniform(-4, 4)
            dy = random.uniform(-9, -2)
            self.particles.append(
                Particle(x+16, y+8, color, dx, dy, 40, 7, 0.35))

    # ── UPDATE ───────────────────────────────────────────────────────────────

    def update(self, player, cam_x):
        solid = self.get_player_solid()

        # Moving platforms: carry player if standing on them
        for mp in self.moving_platforms:
            old_x = mp.rect.x
            old_y = mp.rect.y
            mp.update()
            if mp in self.solid_tiles:
                pass  # reference stays valid since MovingPlatform updates in place
            # Carry player
            if (player.rect.bottom >= mp.rect.top - 2 and
                    player.rect.bottom <= mp.rect.top + 8 and
                    player.rect.right > mp.rect.left and
                    player.rect.left < mp.rect.right):
                dx = mp.rect.x - old_x
                dy = mp.rect.y - old_y
                player.x += dx
                player.rect.x = int(player.x)
                if dy < 0:  # platform going up, push player up
                    player.y += dy
                    player.rect.y = int(player.y)

        # Question blocks
        for q in self.questions:
            q.update()

        # Bricks
        dead_bricks = [b for b in self.bricks if not b.alive]
        for b in dead_bricks:
            self.bricks.remove(b)
            if b in self.solid_tiles:
                self.solid_tiles.remove(b)
        for b in self.bricks:
            b.update()

        # Enemies
        enemy_solid = [t for t in solid if not isinstance(t, MovingPlatform)]
        for mp in self.moving_platforms:
            enemy_solid.append(mp)
        for e in self.enemies:
            if e.dying and e.die_timer > 90:
                continue
            e.update(enemy_solid, player.rect.x)
            # Lava kills enemies
            for lr in self.lava_rects:
                if e.rect.colliderect(lr) and not e.dying:
                    e.dying = True

        # Coins
        for c in self.coins:
            c.update()

        # Power-ups
        pu_solid = [t for t in solid if not isinstance(t, PowerUp)]
        for pu in self.powerups:
            if pu.alive:
                pu.update(pu_solid)

        # Fireballs
        fb_solid = [t for t in solid]
        dead_fbs = []
        for fb in self.fireballs:
            if fb.alive:
                fb.update(fb_solid)
            if not fb.alive:
                dead_fbs.append(fb)
                self.spawn_particles(fb.rect.centerx, fb.rect.centery, ORANGE, 5, 4)
        for fb in dead_fbs:
            self.fireballs.remove(fb)

        # Fireball vs enemy
        for fb in list(self.fireballs):
            if not fb.alive:
                continue
            for e in self.enemies:
                if e.dying:
                    continue
                if fb.rect.colliderect(e.rect):
                    sc = e.fireball_hit()
                    fb.alive = False
                    self.spawn_particles(e.rect.centerx, e.rect.centery, ORANGE, 10, 5)
                    self.floating_texts.append(
                        FloatingText(e.rect.centerx - cam_x,
                                     e.rect.top, f"+{sc}", ORANGE))
                    break

        # Particles
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update()

        # Floating texts
        self.floating_texts = [ft for ft in self.floating_texts if ft.alive]
        for ft in self.floating_texts:
            ft.update()

        # Flag
        self.flag.update()
        if self.completed:
            self.complete_timer += 1

    # ── DRAW ─────────────────────────────────────────────────────────────────

    def draw(self, surf, cam_x):
        self.bg.draw(surf, cam_x)
        self._draw_lava_pits(surf, cam_x)
        self._draw_ground(surf, cam_x)

        # Pipes (drawn on top of ground)
        for pipe in self.pipes:
            pipe.draw(surf, cam_x)

        # Floating platform tiles
        for t in self.draw_tiles:
            t.draw(surf, cam_x)

        # Bricks
        for b in self.bricks:
            b.draw(surf, cam_x)

        # Question blocks
        for q in self.questions:
            q.draw(surf, cam_x)

        # Moving platforms
        for mp in self.moving_platforms:
            mp.draw(surf, cam_x)

        # Coins
        for c in self.coins:
            if not c.collected:
                c.draw(surf, cam_x)

        # Power-ups
        for pu in self.powerups:
            if pu.alive:
                pu.draw(surf, cam_x)

        # Enemies
        for e in self.enemies:
            if not e.dying or e.die_timer < 90:
                e.draw(surf, cam_x)

        # Fireballs
        for fb in self.fireballs:
            if fb.alive:
                fb.draw(surf, cam_x)

        # Particles
        for p in self.particles:
            p.draw(surf, cam_x)

        # Flag pole
        self.flag.draw(surf, cam_x)

        # Floating score texts
        for ft in self.floating_texts:
            ft.draw(surf, cam_x)

    def _draw_ground(self, surf, cam_x):
        th = self.theme
        for (gx, gy, gw, gh) in self.data.get("ground_segments", []):
            sx = gx - cam_x
            if -gw < sx < SCREEN_WIDTH + gw:
                # Body
                pygame.draw.rect(surf, th["ground_body"], (sx, gy, gw, gh))
                # Top strip
                pygame.draw.rect(surf, th["ground_top"],  (sx, gy, gw, 9))
                # Bright edge line
                pygame.draw.rect(surf, th["ground_edge"], (sx, gy, gw, 3))
                # Subtle vertical tile dividers
                for tx in range(0, gw, TILE_SIZE):
                    pygame.draw.line(surf, th["ground_body"],
                                     (sx+tx, gy+9), (sx+tx, gy+gh), 1)
                # Highlight left / right edges
                pygame.draw.line(surf, tuple(min(255,c+25) for c in th["ground_body"]),
                                 (sx, gy+9), (sx, gy+gh-1), 2)

    def _draw_lava_pits(self, surf, cam_x):
        t_ms = pygame.time.get_ticks() / 1000.0
        for lr in self.lava_rects:
            sx = lr.x - cam_x
            if -lr.width < sx < SCREEN_WIDTH + lr.width:
                w, h = lr.width, lr.height
                # Base
                pygame.draw.rect(surf, LAVA_RED, (sx, lr.y, w, h))
                # Wave layer
                for i in range(0, w, 18):
                    wy = lr.y + 5 + int(math.sin(t_ms*2 + i*0.25) * 5)
                    pygame.draw.ellipse(surf, LAVA_ORANGE,
                                        (sx+i-8, wy-7, 22, 13))
                # Bright surface line
                pygame.draw.rect(surf, LAVA_YELLOW, (sx, lr.y, w, 4))
                # Bubble sparkles
                for i in range(0, w, 45):
                    bx = sx + i + 10 + int(math.sin(t_ms*3.0 + i) * 6)
                    by = lr.y + 2 + int(math.sin(t_ms*4.5 + i*0.7) * 5)
                    pygame.draw.circle(surf, LAVA_YELLOW, (int(bx), int(by)), 3)


# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN SHAKE
# ══════════════════════════════════════════════════════════════════════════════

class ScreenShake:
    def __init__(self):
        self.intensity = 0
        self.timer = 0

    def shake(self, intensity=8, duration=15):
        self.intensity = max(self.intensity, intensity)
        self.timer = max(self.timer, duration)

    def update(self):
        if self.timer > 0:
            self.timer -= 1
            if self.timer == 0:
                self.intensity = 0

    def get_offset(self):
        if self.timer > 0:
            s = self.intensity * (self.timer / 15)
            return (random.randint(-int(s), int(s)),
                    random.randint(-int(s), int(s)))
        return (0, 0)


# ══════════════════════════════════════════════════════════════════════════════
#  GAME
# ══════════════════════════════════════════════════════════════════════════════

class Game:
    STATE_MENU     = "menu"
    STATE_PLAYING  = "playing"
    STATE_PAUSED   = "paused"
    STATE_DYING    = "dying"
    STATE_LEVEL_COMPLETE = "level_complete"
    STATE_GAME_OVER= "game_over"
    STATE_VICTORY  = "victory"

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.shake  = ScreenShake()
        self.render_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font_huge = pygame.font.SysFont("Arial", 68, bold=True)
        self.font_big  = pygame.font.SysFont("Arial", 44, bold=True)
        self.font_med  = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_sml  = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_tiny = pygame.font.SysFont("Arial", 15)

        self.hud = HUD()
        self.reset_game()

    # ── RESET / LOAD ─────────────────────────────────────────────────────────

    def reset_game(self):
        self.state      = self.STATE_MENU
        self.score      = 0
        self.coins      = 0
        self.lives      = STARTING_LIVES
        self.level_idx  = 0
        self.cam_x      = 0.0
        self.menu_anim  = 0.0
        self.lc_timer   = 0
        self.die_delay  = 0
        self.level      = None
        self.player     = None
        self._load_level()

    def _load_level(self):
        data = ALL_LEVELS[self.level_idx]
        self.level  = Level(data)
        px = data["start_x"]
        py = data["start_y"]
        self.player = Player(px, py)
        self.cam_x  = max(0.0, float(px) - SCREEN_WIDTH // 3)

    # ── MAIN LOOP ─────────────────────────────────────────────────────────────

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            # dt unused for physics (we use fixed-step logic), just for frame cap

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                self._handle_event(event)

            self._update()
            self._draw()

            shake_off = self.shake.get_offset()
            self.screen.blit(self.render_surf, shake_off)
            pygame.display.flip()

    # ── EVENT HANDLING ────────────────────────────────────────────────────────

    def _handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        k = event.key

        if self.state == self.STATE_MENU:
            if k in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.STATE_PLAYING
            elif k == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        elif self.state == self.STATE_PLAYING:
            if k == pygame.K_p:
                self.state = self.STATE_PAUSED
            elif k in (pygame.K_UP, pygame.K_w, pygame.K_SPACE):
                if self.player.jump():
                    self.level.spawn_particles(
                        self.player.rect.centerx,
                        self.player.rect.bottom,
                        (220, 220, 220), 4, 3)
            elif k in (pygame.K_x, pygame.K_LCTRL, pygame.K_RCTRL):
                self._try_shoot()

        elif self.state == self.STATE_PAUSED:
            if k in (pygame.K_p, pygame.K_ESCAPE):
                self.state = self.STATE_PLAYING

        elif self.state == self.STATE_LEVEL_COMPLETE:
            if k in (pygame.K_RETURN, pygame.K_SPACE) and self.lc_timer > 60:
                self._next_level()

        elif self.state in (self.STATE_GAME_OVER, self.STATE_VICTORY):
            if k in (pygame.K_RETURN, pygame.K_SPACE):
                self.reset_game()

    def _try_shoot(self):
        if self.player.state == "fire" and self.player.fire_cooldown == 0:
            d = 1 if self.player.facing_right else -1
            fx = self.player.rect.right if d == 1 else self.player.rect.left
            fy = self.player.rect.centery - 4
            self.level.fireballs.append(Fireball(fx, fy, d))
            self.player.fire_cooldown = 22

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def _update(self):
        self.shake.update()
        self.menu_anim += 0.03

        if self.state == self.STATE_MENU:
            return
        if self.state == self.STATE_PAUSED:
            return
        if self.state in (self.STATE_GAME_OVER, self.STATE_VICTORY):
            return

        if self.state == self.STATE_DYING:
            self._update_dying()
            return

        if self.state == self.STATE_LEVEL_COMPLETE:
            self.level.update(self.player, self.cam_x)
            self.lc_timer += 1
            return

        # STATE_PLAYING
        self._update_playing()

    def _update_dying(self):
        # Update player death animation
        keys = {k: False for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
                                    pygame.K_a, pygame.K_d, pygame.K_w,
                                    pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT]}
        self.player.update(keys, [], 1.0)
        self.die_delay += 1
        if self.die_delay > 130:
            self.lives -= 1
            if self.lives <= 0:
                self.state = self.STATE_GAME_OVER
            else:
                self._load_level()
                self.state = self.STATE_PLAYING

    def _update_playing(self):
        keys = pygame.key.get_pressed()
        p = self.player

        # Jump hold
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            p.jump(holding=True)

        # Continuous fire
        if (keys[pygame.K_x] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
            if p.state == "fire" and p.fire_cooldown == 0:
                self._try_shoot()

        # Get solid tiles once per frame for efficiency
        solid = self.level.get_player_solid()

        # Player update
        p.update(keys, solid, 1.0)

        # Camera follow (smooth)
        target_cam = p.rect.centerx - SCREEN_WIDTH // 3
        self.cam_x = lerp(self.cam_x, float(target_cam), 0.10)
        self.cam_x = max(0.0, min(self.cam_x, float(self.level.width - SCREEN_WIDTH)))

        # Level update
        self.level.update(p, self.cam_x)

        # Lava death
        for lr in self.level.lava_rects:
            if p.rect.colliderect(lr):
                self._player_killed()
                return

        # Fall off bottom
        if p.rect.top > SCREEN_HEIGHT + 80:
            self._player_killed()
            return

        # Collisions
        self._check_enemy_collisions()
        self._check_coin_collisions()
        self._check_powerup_collisions()
        self._check_block_hits()
        self._check_flag()

    # ── COLLISION CHECKS ─────────────────────────────────────────────────────

    def _check_enemy_collisions(self):
        p = self.player
        star_active = p.star_timer > 0

        for e in self.level.enemies:
            if e.dying:
                continue
            if not p.rect.colliderect(e.rect):
                continue

            if star_active:
                # Star: instantly kill enemy
                sc = e.stomp()
                self.score += sc
                self.level.spawn_particles(e.rect.centerx, e.rect.centery, YELLOW, 12, 6)
                self._add_float_text(e.rect.centerx, e.rect.top, f"+{sc}", YELLOW)
                self.shake.shake(3, 6)
                continue

            # Stomp check: player falling, hitting top half of enemy
            stomping = (p.vy > 1 and
                        p.rect.bottom <= e.rect.centery + 16 and
                        p.rect.bottom >= e.rect.top - 4)

            if stomping:
                sc = e.stomp()
                self.score += sc
                p.vy = -9.0
                p.is_jumping = True
                p.jump_hold = 0
                self.shake.shake(4, 8)
                self.level.spawn_particles(e.rect.centerx, e.rect.centery, ORANGE, 8, 5)
                self._add_float_text(e.rect.centerx, e.rect.top, f"+{sc}", ORANGE)
            else:
                # Koopa shell kick
                if getattr(e, 'shelled', False):
                    e.kick_shell()
                else:
                    self._player_hit()

    def _player_hit(self):
        p = self.player
        if p.invincible:
            return
        dead = p.get_hit()
        if dead:
            self._player_killed()
        else:
            self.shake.shake(7, 14)
            self.level.spawn_particles(p.rect.centerx, p.rect.centery,
                                       (255, 240, 60), 12, 6)

    def _player_killed(self):
        p = self.player
        if p.dying:
            return
        p.die()
        self.shake.shake(14, 28)
        self.level.spawn_particles(p.rect.centerx, p.rect.centery, RED, 20, 8)
        self.state = self.STATE_DYING
        self.die_delay = 0

    def _check_coin_collisions(self):
        for c in self.level.coins:
            if c.collected:
                continue
            if self.player.rect.colliderect(c.rect):
                c.collected = True
                self.coins += 1
                self.score += COIN_SCORE
                self.level.spawn_particles(c.rect.centerx, c.rect.centery, GOLD, 5, 4)
                self._add_float_text(c.rect.centerx, c.rect.top, "+100", GOLD, 16)
                if self.coins >= 100:
                    self.coins -= 100
                    self.lives += 1
                    self._add_float_text(c.rect.centerx, c.rect.top - 20,
                                         "1-UP!", LIGHT_GREEN, 22)

    def _check_powerup_collisions(self):
        for pu in list(self.level.powerups):
            if not pu.alive or pu.emerging:
                continue
            if self.player.rect.colliderect(pu.rect):
                pu.alive = False
                self.score += POWERUP_SCORE
                if pu.ptype == POWERUP_MUSHROOM:
                    if self.player.state == "small":
                        self.player.grow("big")
                    else:
                        self.score += POWERUP_SCORE
                elif pu.ptype == POWERUP_STAR:
                    self.player.grow("star")
                elif pu.ptype == POWERUP_FIRE:
                    self.player.grow("fire")
                self.level.spawn_particles(pu.rect.centerx, pu.rect.centery,
                                           YELLOW, 15, 7)
                self.shake.shake(4, 8)
                self._add_float_text(pu.rect.centerx, pu.rect.top,
                                     f"+{POWERUP_SCORE}", LIGHT_GREEN, 22)

    def _check_block_hits(self):
        p = self.player
        if p.vy >= 0:
            return  # only care about upward motion

        # A small sensor just above player's head
        head_sensor = pygame.Rect(p.rect.x + 6, p.rect.y - 6, p.rect.width - 12, 10)

        # Question blocks
        for q in self.level.questions:
            if q.activated:
                continue
            if head_sensor.colliderect(q.rect) and p.rect.top > q.rect.centery:
                if q.activate():
                    self.level.spawn_powerup(q.rect.x, q.rect.y - TILE_SIZE, q.item_type)
                    self.level.spawn_particles(q.rect.centerx, q.rect.top, GOLD, 8, 5)
                    self.score += 50
                    p.vy = 1.5  # soft bounce back

        # Brick blocks
        for b in list(self.level.bricks):
            if not b.alive:
                continue
            if head_sensor.colliderect(b.rect) and p.rect.top > b.rect.centery:
                big = p.state in ("big", "fire")
                broke = b.bump(big)
                if broke:
                    th = THEMES[self.level.theme_key]
                    self.level.spawn_brick_particles(b.rect.x, b.rect.y,
                                                     th["brick_color"])
                    self.score += 50
                    self.shake.shake(5, 8)
                p.vy = 1.5

    def _check_flag(self):
        if self.level.completed:
            return
        if self.player.rect.right >= self.level.data["flag_x"]:
            self.level.completed = True
            self.level.flag.start_slide()
            self.score += LEVEL_COMPLETE_SCORE
            self.state = self.STATE_LEVEL_COMPLETE
            self.lc_timer = 0
            self.shake.shake(10, 22)

    def _next_level(self):
        self.level_idx += 1
        if self.level_idx >= len(ALL_LEVELS):
            self.state = self.STATE_VICTORY
        else:
            self._load_level()
            self.state = self.STATE_PLAYING

    def _add_float_text(self, world_x, world_y, text, color=YELLOW, size=20):
        # Convert world coords to screen coords for floating text
        sx = world_x - self.cam_x
        self.level.floating_texts.append(
            FloatingText(sx, world_y, text, color, size))

    # ── DRAW ──────────────────────────────────────────────────────────────────

    def _draw(self):
        surf = self.render_surf
        surf.fill(BLACK)

        if self.state == self.STATE_MENU:
            self._draw_menu(surf)
        elif self.state in (self.STATE_PLAYING, self.STATE_DYING,
                             self.STATE_LEVEL_COMPLETE):
            self._draw_game(surf)
            if self.state == self.STATE_LEVEL_COMPLETE:
                self._draw_level_complete_overlay(surf)
        elif self.state == self.STATE_PAUSED:
            self._draw_game(surf)
            self._draw_pause_overlay(surf)
        elif self.state == self.STATE_GAME_OVER:
            self._draw_game(surf)
            self._draw_game_over_overlay(surf)
        elif self.state == self.STATE_VICTORY:
            self._draw_victory(surf)

    def _draw_game(self, surf):
        cam_x = int(self.cam_x)
        self.level.draw(surf, cam_x)
        self.player.draw(surf, cam_x, star_active=self.player.star_timer > 0)
        self.hud.draw(surf, self.score, self.coins, self.lives,
                      self.level_idx + 1, self.player.state, self.player.star_timer)

    # ── MENU ─────────────────────────────────────────────────────────────────

    def _draw_menu(self, surf):
        t = self.menu_anim
        # Animated sky gradient
        for y in range(SCREEN_HEIGHT):
            frac = y / SCREEN_HEIGHT
            r = int(lerp(40, 90, frac))
            g = int(lerp(80, 150, frac))
            b = int(lerp(180, 230, frac))
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Ground strip
        pygame.draw.rect(surf, GREEN, (0, SCREEN_HEIGHT-80, SCREEN_WIDTH, 80))
        pygame.draw.rect(surf, LIGHT_GREEN, (0, SCREEN_HEIGHT-80, SCREEN_WIDTH, 8))
        pygame.draw.rect(surf, DARK_BROWN,  (0, SCREEN_HEIGHT-56, SCREEN_WIDTH, 56))
        # Grid lines on ground
        for gx in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(surf, DARK_BROWN, (gx, SCREEN_HEIGHT-56), (gx, SCREEN_HEIGHT), 1)

        # Pipes
        for px in [80, 240, 700, 860]:
            self._draw_menu_pipe(surf, px, SCREEN_HEIGHT-80)

        # Animated clouds
        for i, (cx, cy, cw) in enumerate([
            (80, 70, 110), (280, 45, 90), (520, 80, 120),
            (760, 55, 100), (950, 75, 95)
        ]):
            ox = math.sin(t*0.5 + i*1.2) * 12
            self._draw_menu_cloud(surf, cx + ox, cy, cw)

        # Title shadow + text
        self._draw_shadowed(surf, self.font_huge, "SUPER MARIO", RED,    SCREEN_WIDTH//2, 110)
        self._draw_shadowed(surf, self.font_big,  "PYTHON EDITION", YELLOW, SCREEN_WIDTH//2, 195)

        # Animated player
        mx = int(SCREEN_WIDTH//2 + math.sin(t*1.2)*80)
        bounce = int(abs(math.sin(t*2.5)) * 25)
        my = SCREEN_HEIGHT - 125 - bounce
        self._draw_menu_mario(surf, mx, my)

        # Blink "Press Start"
        if int(t * 40) % 50 < 35:
            start = self.font_med.render("PRESS ENTER OR SPACE TO START", True, WHITE)
            surf.blit(start, (SCREEN_WIDTH//2 - start.get_width()//2, 280))

        # Controls box
        box_x, box_y = SCREEN_WIDTH//2 - 240, 340
        pygame.draw.rect(surf, (0,0,0,0), (box_x, box_y, 480, 140))
        pygame.draw.rect(surf, (20,20,20), (box_x, box_y, 480, 140), border_radius=10)
        pygame.draw.rect(surf, GOLD, (box_x, box_y, 480, 140), 2, border_radius=10)
        controls = [
            "Arrow Keys / WASD: Move      Shift: Run",
            "Up / W / Space: Jump (hold for higher)",
            "X / Ctrl: Shoot Fireball (Fire Power)",
            "P: Pause / ESC: Quit",
        ]
        for i, ctrl in enumerate(controls):
            ct = self.font_tiny.render(ctrl, True, CREAM)
            surf.blit(ct, (SCREEN_WIDTH//2 - ct.get_width()//2, box_y + 15 + i*28))

        # World count teaser
        wt = self.font_sml.render("4 WORLDS  |  Multiple Enemies  |  Power-Ups  |  Boss!", True, GOLD)
        surf.blit(wt, (SCREEN_WIDTH//2 - wt.get_width()//2, SCREEN_HEIGHT - 30))

    def _draw_menu_mario(self, surf, x, y):
        # Hat
        pygame.draw.rect(surf, RED, (x-16, y-40, 32, 13), border_radius=3)
        pygame.draw.rect(surf, RED, (x-12, y-52, 24, 16), border_radius=4)
        # Face
        pygame.draw.ellipse(surf, TAN, (x-12, y-30, 24, 22))
        # Eyes
        pygame.draw.circle(surf, BLACK, (x+4, y-22), 3)
        pygame.draw.circle(surf, WHITE, (x+5, y-23), 1)
        # Mustache
        pygame.draw.ellipse(surf, DARK_BROWN, (x-9, y-15, 9, 6))
        pygame.draw.ellipse(surf, DARK_BROWN, (x, y-15, 9, 6))
        # Body
        pygame.draw.rect(surf, RED,  (x-14, y-8, 28, 16), border_radius=3)
        pygame.draw.rect(surf, BLUE, (x-14, y+6, 28, 16), border_radius=4)
        # Overall straps
        pygame.draw.line(surf, DARK_BLUE, (x-7, y-8), (x-7, y-16), 3)
        pygame.draw.line(surf, DARK_BLUE, (x+7, y-8), (x+7, y-16), 3)
        # Shoes
        pygame.draw.ellipse(surf, DARK_BROWN, (x-16, y+20, 16, 10))
        pygame.draw.ellipse(surf, DARK_BROWN, (x, y+20, 16, 10))

    def _draw_menu_cloud(self, surf, x, y, w):
        h = max(18, w//3)
        pygame.draw.ellipse(surf, CLOUD_WHITE, (x, y, w, h))
        pygame.draw.ellipse(surf, CLOUD_WHITE, (x+w//5, y-h//2, int(w*0.65), h))
        pygame.draw.ellipse(surf, CLOUD_WHITE, (x+w//2, y-h//4, w//2, int(h*0.7)))
        # Shadow
        pygame.draw.ellipse(surf, (215, 230, 245), (x+6, y+h//2, max(5, w-12), max(5, h//3)))

    def _draw_menu_pipe(self, surf, x, y):
        pygame.draw.rect(surf, (40, 150, 40), (x, y-64, 44, 64))
        pygame.draw.rect(surf, (20, 100, 20), (x-6, y-72, 56, 18), border_radius=5)
        pygame.draw.rect(surf, (60, 190, 60), (x+4, y-68, 10, 14))

    def _draw_shadowed(self, surf, font, text, color, cx, y, shadow=(0,0,0)):
        shadow_surf = font.render(text, True, shadow)
        main_surf   = font.render(text, True, color)
        surf.blit(shadow_surf, (cx - main_surf.get_width()//2 + 4, y + 4))
        surf.blit(main_surf,   (cx - main_surf.get_width()//2, y))

    # ── PAUSE OVERLAY ────────────────────────────────────────────────────────

    def _draw_pause_overlay(self, surf):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 40, 170))
        surf.blit(overlay, (0, 0))
        self._draw_shadowed(surf, self.font_big, "PAUSED", WHITE,
                            SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70)
        resume = self.font_med.render("Press P or ESC to Resume", True, LIGHT_GRAY)
        surf.blit(resume, (SCREEN_WIDTH//2 - resume.get_width()//2,
                           SCREEN_HEIGHT//2 + 10))

    # ── LEVEL COMPLETE OVERLAY ───────────────────────────────────────────────

    def _draw_level_complete_overlay(self, surf):
        if self.lc_timer < 10:
            return
        fade = min(170, self.lc_timer * 4)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, fade))
        surf.blit(overlay, (0, 0))

        if self.lc_timer > 25:
            self._draw_shadowed(surf, self.font_big, "LEVEL CLEAR!", YELLOW,
                                SCREEN_WIDTH//2, 170)
            sc_surf = self.font_med.render(f"Score: {self.score:,}", True, WHITE)
            surf.blit(sc_surf, (SCREEN_WIDTH//2 - sc_surf.get_width()//2, 250))

            # Star rating
            threshold = [2000, 5000, 9000]
            stars_earned = sum(1 for th in threshold if self.score >= th)
            for i in range(3):
                col = GOLD if i < stars_earned else DARK_GRAY
                cx_s = SCREEN_WIDTH//2 - 70 + i * 70
                pts = []
                for j in range(10):
                    ang = math.pi/2 + j * math.pi/5
                    r = 24 if j%2==0 else 10
                    pts.append((cx_s + r*math.cos(ang), 330 - r*math.sin(ang)))
                pygame.draw.polygon(surf, col, pts)
                if i < stars_earned:
                    # Shine
                    pygame.draw.polygon(surf, YELLOW, pts, 2)

        if self.lc_timer > 80:
            if (self.lc_timer // 22) % 2 == 0:
                cont = self.font_sml.render("Press ENTER or SPACE to continue", True, CREAM)
                surf.blit(cont, (SCREEN_WIDTH//2 - cont.get_width()//2, 400))

    # ── GAME OVER OVERLAY ────────────────────────────────────────────────────

    def _draw_game_over_overlay(self, surf):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        surf.blit(overlay, (0, 0))
        self._draw_shadowed(surf, self.font_huge, "GAME OVER", RED,
                            SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120)
        sc_surf = self.font_med.render(f"Final Score: {self.score:,}", True, WHITE)
        surf.blit(sc_surf, (SCREEN_WIDTH//2 - sc_surf.get_width()//2, SCREEN_HEIGHT//2))
        retry = self.font_sml.render("Press ENTER to try again", True, YELLOW)
        surf.blit(retry, (SCREEN_WIDTH//2 - retry.get_width()//2, SCREEN_HEIGHT//2+70))

    # ── VICTORY SCREEN ───────────────────────────────────────────────────────

    def _draw_victory(self, surf):
        t = self.menu_anim
        # Rainbow background
        for y in range(SCREEN_HEIGHT):
            hue = ((y * 2 + int(t * 120)) % 360) / 360.0
            r2, g2, b2 = colorsys.hsv_to_rgb(hue, 0.65, 0.85)
            pygame.draw.line(surf, (int(r2*255), int(g2*255), int(b2*255)),
                             (0, y), (SCREEN_WIDTH, y))

        self._draw_shadowed(surf, self.font_huge, "YOU WIN!", YELLOW,
                            SCREEN_WIDTH//2, 100)
        self._draw_shadowed(surf, self.font_big, "Congratulations, Hero!", WHITE,
                            SCREEN_WIDTH//2, 200)
        sc_surf = self.font_med.render(f"Final Score: {self.score:,}", True, GOLD)
        surf.blit(sc_surf, (SCREEN_WIDTH//2 - sc_surf.get_width()//2, 270))

        # Firework bursts
        for i in range(8):
            fx = int(SCREEN_WIDTH//2 + math.cos(t * 0.8 + i * 0.78) * 320)
            fy = int(220 + math.sin(t * 1.1 + i * 1.1) * 140)
            colors_fw = [(255,80,80),(255,200,0),(0,255,100),(0,180,255),
                         (255,0,200),(255,140,0),(200,255,0),(130,100,255)]
            col_fw = colors_fw[i % len(colors_fw)]
            for j in range(12):
                ang = j * math.pi / 6
                pulse = 28 + int(math.sin(t*4 + j + i) * 10)
                px2 = fx + int(pulse * math.cos(ang))
                py2 = fy + int(pulse * math.sin(ang))
                pygame.draw.circle(surf, col_fw, (px2, py2), 4)
            pygame.draw.circle(surf, WHITE, (fx, fy), 6)

        # Big Mario in center
        self._draw_menu_mario(surf, SCREEN_WIDTH//2, 380)

        retry = self.font_sml.render("Press ENTER to play again!", True, WHITE)
        surf.blit(retry, (SCREEN_WIDTH//2 - retry.get_width()//2, 450))
