# sprites.py - All game object classes

import pygame
import math
import random
from settings import *


# ══════════════════════════════════════════════════════════════════════════════
#  DRAWING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def draw_rounded_rect(surf, color, rect, radius=6):
    pygame.draw.rect(surf, color, rect, border_radius=radius)

def draw_eye(surf, cx, cy, facing_right=True, blink=False):
    """Draw a cartoon eye."""
    pygame.draw.circle(surf, WHITE, (cx, cy), 5)
    pupil_ox = 2 if facing_right else -2
    if not blink:
        pygame.draw.circle(surf, BLACK, (cx + pupil_ox, cy + 1), 3)
        pygame.draw.circle(surf, WHITE, (cx + pupil_ox + 1, cy), 1)
    else:
        pygame.draw.line(surf, BLACK, (cx - 4, cy), (cx + 4, cy), 2)


# ══════════════════════════════════════════════════════════════════════════════
#  PARTICLE
# ══════════════════════════════════════════════════════════════════════════════

class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, life=30, size=4, gravity=0.15):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.vx = vx if vx is not None else random.uniform(-3, 3)
        self.vy = vy if vy is not None else random.uniform(-5, -1)
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = gravity
        self.alive = True

    def update(self):
        self.vx *= 0.96
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self, surf, cam_x):
        alpha = self.life / self.max_life
        sz = max(1, int(self.size * alpha))
        sx = int(self.x - cam_x)
        sy = int(self.y)
        if -10 < sx < SCREEN_WIDTH + 10:
            pygame.draw.circle(surf, self.color, (sx, sy), sz)


class FloatingText:
    def __init__(self, x, y, text, color=YELLOW, size=22):
        self.x = float(x)
        self.y = float(y)
        self.text = text
        self.color = color
        self.life = 60
        self.max_life = 60
        self.vy = -1.2
        self.alive = True
        self.font = pygame.font.SysFont("Arial", size, bold=True)

    def update(self):
        self.y += self.vy
        self.vy *= 0.97
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self, surf, cam_x):
        alpha = min(255, int(255 * self.life / self.max_life))
        img = self.font.render(self.text, True, self.color)
        img.set_alpha(alpha)
        sx = int(self.x - cam_x) - img.get_width() // 2
        sy = int(self.y)
        surf.blit(img, (sx, sy))


# ══════════════════════════════════════════════════════════════════════════════
#  TILE
# ══════════════════════════════════════════════════════════════════════════════

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type, theme):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.tile_type = tile_type
        self.theme = theme
        self.image = self._make_image()
        self.solid = tile_type != TILE_LAVA

    def _make_image(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        t = self.tile_type
        th = self.theme

        if t == TILE_GROUND:
            self._draw_ground(surf)
        elif t == TILE_BRICK:
            self._draw_brick(surf)
        elif t == TILE_QUESTION:
            self._draw_question(surf)
        elif t == TILE_SOLID:
            self._draw_solid(surf)
        elif t == TILE_PLATFORM:
            self._draw_platform(surf)
        elif t == TILE_LAVA:
            self._draw_lava(surf)
        return surf

    def _draw_ground(self, surf):
        th = THEMES[self.theme]
        pygame.draw.rect(surf, th["ground_body"], (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, th["ground_top"], (0, 0, TILE_SIZE, 8))
        pygame.draw.rect(surf, th["ground_edge"], (0, 0, TILE_SIZE, 3))
        # Subtle grid lines
        pygame.draw.line(surf, th["ground_body"], (0, 8), (0, TILE_SIZE), 1)
        pygame.draw.line(surf, th["ground_body"], (TILE_SIZE-1, 8), (TILE_SIZE-1, TILE_SIZE), 1)

    def _draw_brick(self, surf):
        th = THEMES[self.theme]
        bc = th["brick_color"]
        bd = th["brick_dark"]
        pygame.draw.rect(surf, bc, (0, 0, TILE_SIZE, TILE_SIZE))
        # Mortar lines
        pygame.draw.rect(surf, bd, (0, 0, TILE_SIZE, TILE_SIZE), 1)
        pygame.draw.line(surf, bd, (0, TILE_SIZE//2), (TILE_SIZE, TILE_SIZE//2), 2)
        pygame.draw.line(surf, bd, (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE//2), 2)
        pygame.draw.line(surf, bd, (TILE_SIZE//4, TILE_SIZE//2), (TILE_SIZE//4, TILE_SIZE), 2)
        pygame.draw.line(surf, bd, (3*TILE_SIZE//4, TILE_SIZE//2), (3*TILE_SIZE//4, TILE_SIZE), 2)
        # Highlight
        pygame.draw.line(surf, tuple(min(255, c+40) for c in bc), (1, 1), (TILE_SIZE-2, 1), 1)

    def _draw_question(self, surf):
        th = THEMES[self.theme]
        qc = th["question_color"]
        qs = th["question_shine"]
        pygame.draw.rect(surf, qc, (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, DARK_BROWN, (0, 0, TILE_SIZE, TILE_SIZE), 2)
        # Shine
        pygame.draw.rect(surf, qs, (2, 2, TILE_SIZE-4, 5))
        # "?" symbol
        font = pygame.font.SysFont("Arial", 20, bold=True)
        q_surf = font.render("?", True, WHITE)
        surf.blit(q_surf, (TILE_SIZE//2 - q_surf.get_width()//2,
                           TILE_SIZE//2 - q_surf.get_height()//2))

    def _draw_solid(self, surf):
        th = THEMES[self.theme]
        sc = th.get("ground_body", DARK_GRAY)
        pygame.draw.rect(surf, sc, (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, th.get("ground_top", GRAY), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        pygame.draw.line(surf, tuple(min(255, c+30) for c in sc), (1,1),(TILE_SIZE-1,1), 1)

    def _draw_platform(self, surf):
        th = THEMES[self.theme]
        pygame.draw.rect(surf, th["ground_top"], (0, 0, TILE_SIZE, 10))
        pygame.draw.rect(surf, th["ground_body"], (0, 10, TILE_SIZE, TILE_SIZE-10))
        pygame.draw.rect(surf, th["ground_edge"], (0, 0, TILE_SIZE, 3))

    def _draw_lava(self, surf):
        pygame.draw.rect(surf, LAVA_RED, (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, LAVA_ORANGE, (0, 4, TILE_SIZE, 4))
        pygame.draw.rect(surf, LAVA_YELLOW, (0, 2, TILE_SIZE, 2))

    def draw(self, surf, cam_x):
        sx = self.rect.x - cam_x
        if -TILE_SIZE < sx < SCREEN_WIDTH + TILE_SIZE:
            surf.blit(self.image, (sx, self.rect.y))


class QuestionBlock(Tile):
    def __init__(self, x, y, theme, item_type):
        self.item_type = item_type
        self.activated = False
        self.anim_timer = 0
        self.bump_vy = 0
        self.bump_y = 0
        super().__init__(x, y, TILE_QUESTION, theme)
        self.base_y = y

    def activate(self):
        if not self.activated:
            self.activated = True
            self.bump_vy = -8
            self.image = self._make_used_image()
            return True
        return False

    def _make_used_image(self):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(surf, BROWN, (0, 0, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(surf, DARK_BROWN, (0, 0, TILE_SIZE, TILE_SIZE), 2)
        pygame.draw.rect(surf, DARK_BROWN, (3, 3, TILE_SIZE-6, TILE_SIZE-6))
        return surf

    def update(self):
        if self.bump_vy != 0:
            self.bump_y += self.bump_vy
            self.bump_vy += 1.5
            if self.bump_y >= 0:
                self.bump_y = 0
                self.bump_vy = 0
        self.rect.y = self.base_y + int(self.bump_y)
        self.anim_timer += 1

    def draw(self, surf, cam_x):
        sx = self.rect.x - cam_x
        if -TILE_SIZE < sx < SCREEN_WIDTH + TILE_SIZE:
            if not self.activated:
                # Animated shimmer
                shimmer = abs(math.sin(self.anim_timer * 0.08)) * 20
                img = self.image.copy()
                overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                overlay.fill((255, 255, 100, int(shimmer)))
                img.blit(overlay, (0, 0))
                surf.blit(img, (sx, self.rect.y))
            else:
                surf.blit(self.image, (sx, self.rect.y))


class BrickBlock(Tile):
    def __init__(self, x, y, theme):
        super().__init__(x, y, TILE_BRICK, theme)
        self.base_y = y
        self.bump_vy = 0
        self.bump_y = 0
        self.breaking = False
        self.break_timer = 0
        self.alive = True

    def bump(self, big=False):
        if big:
            self.breaking = True
            self.break_timer = 0
            return True  # signals: remove this brick
        else:
            self.bump_vy = -8
            return False

    def update(self):
        if self.bump_vy != 0:
            self.bump_y += self.bump_vy
            self.bump_vy += 1.5
            if self.bump_y >= 0:
                self.bump_y = 0
                self.bump_vy = 0
        self.rect.y = self.base_y + int(self.bump_y)
        if self.breaking:
            self.break_timer += 1
            if self.break_timer > 5:
                self.alive = False

    def draw(self, surf, cam_x):
        if not self.alive:
            return
        sx = self.rect.x - cam_x
        if -TILE_SIZE < sx < SCREEN_WIDTH + TILE_SIZE:
            surf.blit(self.image, (sx, self.rect.y))


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, height_tiles, theme):
        super().__init__()
        h = height_tiles * TILE_SIZE
        self.rect = pygame.Rect(x, y - h + TILE_SIZE, TILE_SIZE * 2, h)
        self.theme = theme
        self.image = self._make_image(h)

    def _make_image(self, h):
        surf = pygame.Surface((TILE_SIZE * 2, h), pygame.SRCALPHA)
        th = THEMES[self.theme]
        body = th["pipe_body"]
        rim  = th["pipe_rim"]
        # Body
        pygame.draw.rect(surf, body, (2, TILE_SIZE, TILE_SIZE*2-4, h - TILE_SIZE))
        # Rim
        pygame.draw.rect(surf, rim,  (0, 0, TILE_SIZE*2, TILE_SIZE+4), border_radius=4)
        pygame.draw.rect(surf, body, (4, 4, TILE_SIZE*2-8, TILE_SIZE-4))
        # Highlights
        light = tuple(min(255, c+50) for c in body)
        pygame.draw.line(surf, light, (4, TILE_SIZE+2), (4, h-2), 2)
        pygame.draw.line(surf, light, (4, 4), (TILE_SIZE*2-8, 4), 2)
        return surf

    def draw(self, surf, cam_x):
        sx = self.rect.x - cam_x
        if -TILE_SIZE*2 < sx < SCREEN_WIDTH + TILE_SIZE*2:
            surf.blit(self.image, (sx, self.rect.y))


# ══════════════════════════════════════════════════════════════════════════════
#  COIN
# ══════════════════════════════════════════════════════════════════════════════

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 20)
        self.rect.centerx = x
        self.anim = 0
        self.collected = False
        self.alive = True

    def update(self):
        self.anim += 0.1

    def draw(self, surf, cam_x):
        sx = self.rect.centerx - cam_x
        sy = self.rect.centery
        if -30 < sx < SCREEN_WIDTH + 30:
            t = abs(math.sin(self.anim))
            w = max(3, int(14 * t))
            # Shadow
            pygame.draw.ellipse(surf, DARK_BROWN, (sx - 7, sy + 9, 14, 4))
            # Coin body (squished circle = ellipse for spin effect)
            pygame.draw.ellipse(surf, GOLD,   (sx - w//2, sy - 10, w, 20))
            pygame.draw.ellipse(surf, YELLOW, (sx - max(1,w//2-2), sy - 8, max(2,w-4), 16))


# ══════════════════════════════════════════════════════════════════════════════
#  POWER-UP
# ══════════════════════════════════════════════════════════════════════════════

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, ptype):
        super().__init__()
        self.ptype = ptype
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.vx = 2.0
        self.vy = 0.0
        self.on_ground = False
        self.alive = True
        self.anim = 0
        self.emerge_y = y
        self.emerging = True
        self.emerge_progress = 0

    def update(self, solid_tiles):
        self.anim += 0.1
        if self.emerging:
            self.emerge_progress += 2
            self.rect.y = self.emerge_y - self.emerge_progress
            if self.emerge_progress >= TILE_SIZE:
                self.emerging = False
            return

        if self.ptype == POWERUP_MUSHROOM:
            self.vy += GRAVITY
            self.vy = min(self.vy, MAX_FALL_SPEED)
            self.rect.x += int(self.vx)
            self._check_horizontal(solid_tiles)
            self.rect.y += int(self.vy)
            self._check_vertical(solid_tiles)
        elif self.ptype == POWERUP_STAR:
            self.vy += GRAVITY * 0.7
            if self.on_ground:
                self.vy = -10
            self.vy = min(self.vy, MAX_FALL_SPEED)
            self.rect.x += int(self.vx)
            self._check_horizontal(solid_tiles)
            self.rect.y += int(self.vy)
            self.on_ground = False
            self._check_vertical(solid_tiles)
        # Fire flower stays put
        if self.rect.x < 0 or self.rect.x > 4000:
            self.alive = False

    def _check_horizontal(self, tiles):
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vx > 0:
                    self.rect.right = t.rect.left
                    self.vx = -abs(self.vx)
                else:
                    self.rect.left = t.rect.right
                    self.vx = abs(self.vx)

    def _check_vertical(self, tiles):
        self.on_ground = False
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vy > 0:
                    self.rect.bottom = t.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = t.rect.bottom
                    self.vy = 0

    def draw(self, surf, cam_x):
        sx = self.rect.x - cam_x
        sy = self.rect.y
        if -40 < sx < SCREEN_WIDTH + 40:
            if self.ptype == POWERUP_MUSHROOM:
                self._draw_mushroom(surf, sx, sy)
            elif self.ptype == POWERUP_STAR:
                self._draw_star(surf, sx, sy)
            elif self.ptype == POWERUP_FIRE:
                self._draw_fire_flower(surf, sx, sy)

    def _draw_mushroom(self, surf, sx, sy):
        # Cap
        pygame.draw.ellipse(surf, RED, (sx+1, sy, TILE_SIZE-2, TILE_SIZE//2+6))
        pygame.draw.circle(surf, WHITE, (sx+8, sy+8), 5)
        pygame.draw.circle(surf, WHITE, (sx+22, sy+10), 4)
        pygame.draw.circle(surf, WHITE, (sx+16, sy+4), 3)
        # Stem
        pygame.draw.rect(surf, CREAM, (sx+6, sy+14, TILE_SIZE-12, TILE_SIZE-14), border_radius=3)
        # Eyes
        draw_eye(surf, sx+10, sy+18, True)
        draw_eye(surf, sx+20, sy+18, True)

    def _draw_star(self, surf, sx, sy):
        cx, cy = sx + TILE_SIZE//2, sy + TILE_SIZE//2
        bob = math.sin(self.anim * 3) * 3
        cy += bob
        # Star polygon
        pts = []
        for i in range(10):
            angle = math.pi/2 + i * math.pi/5
            r = 14 if i % 2 == 0 else 6
            pts.append((cx + r*math.cos(angle), cy - r*math.sin(angle)))
        pygame.draw.polygon(surf, YELLOW, pts)
        pygame.draw.polygon(surf, GOLD, pts, 2)
        # Eyes
        draw_eye(surf, cx-5, cy, True)
        draw_eye(surf, cx+5, cy, True)

    def _draw_fire_flower(self, surf, sx, sy):
        # Stem
        pygame.draw.line(surf, DARK_GREEN, (sx+16, sy+28), (sx+16, sy+30), 3)
        # Leaves
        pygame.draw.ellipse(surf, GREEN, (sx+4, sy+18, 14, 8))
        pygame.draw.ellipse(surf, GREEN, (sx+16, sy+20, 12, 7))
        # Petals
        for angle in range(0, 360, 60):
            rad = math.radians(angle + self.anim * 30)
            px = int(sx+16 + 11*math.cos(rad))
            py = int(sy+14 + 11*math.sin(rad))
            col = ORANGE if (angle//60) % 2 == 0 else RED
            pygame.draw.circle(surf, col, (px, py), 6)
        # Center
        pygame.draw.circle(surf, YELLOW, (sx+16, sy+14), 7)
        draw_eye(surf, sx+12, sy+14, True)
        draw_eye(surf, sx+20, sy+14, True)


# ══════════════════════════════════════════════════════════════════════════════
#  FIREBALL
# ══════════════════════════════════════════════════════════════════════════════

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.rect = pygame.Rect(x, y, 14, 14)
        self.vx = 10 * direction
        self.vy = 0
        self.alive = True
        self.anim = 0
        self.bounces = 0

    def update(self, solid_tiles):
        self.anim += 0.3
        self.vy += GRAVITY
        self.vy = min(self.vy, 8)
        self.rect.x += int(self.vx)
        # Wall check
        for t in solid_tiles:
            if self.rect.colliderect(t.rect):
                self.alive = False
                return
        self.rect.y += int(self.vy)
        for t in solid_tiles:
            if self.rect.colliderect(t.rect):
                if self.vy > 0:
                    self.rect.bottom = t.rect.top
                    self.vy = -8
                    self.bounces += 1
                    if self.bounces > 4:
                        self.alive = False
                        return
                else:
                    self.rect.top = t.rect.bottom
                    self.vy = 1
        if self.rect.x < -100 or self.rect.x > 5000:
            self.alive = False

    def draw(self, surf, cam_x):
        sx = self.rect.centerx - cam_x
        sy = self.rect.centery
        pulse = abs(math.sin(self.anim)) * 3
        pygame.draw.circle(surf, WHITE,  (sx, sy), 7 + int(pulse))
        pygame.draw.circle(surf, YELLOW, (sx, sy), 5 + int(pulse*0.7))
        pygame.draw.circle(surf, ORANGE, (sx, sy), 3)


# ══════════════════════════════════════════════════════════════════════════════
#  MOVING PLATFORM
# ══════════════════════════════════════════════════════════════════════════════

class MovingPlatform:
    def __init__(self, x, y, width_tiles, move_type, move_range, speed, theme):
        w = width_tiles * TILE_SIZE
        self.rect = pygame.Rect(x, y, w, TILE_SIZE)
        self.move_type = move_type
        self.move_range = move_range
        self.speed = speed
        self.direction = 1
        self.origin_x = x
        self.origin_y = y
        self.theme = theme
        self.image = self._make_image(w)

    def _make_image(self, w):
        surf = pygame.Surface((w, TILE_SIZE), pygame.SRCALPHA)
        th = THEMES[self.theme]
        pygame.draw.rect(surf, th["ground_top"], (0, 0, w, TILE_SIZE), border_radius=6)
        pygame.draw.rect(surf, th["ground_edge"], (0, 0, w, 5), border_radius=6)
        pygame.draw.rect(surf, tuple(max(0,c-30) for c in th["ground_top"]),
                         (0, 0, w, TILE_SIZE), 2, border_radius=6)
        return surf

    def update(self):
        if self.move_type == 'h':
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.origin_x) >= self.move_range:
                self.direction *= -1
        else:
            self.rect.y += self.speed * self.direction
            if abs(self.rect.y - self.origin_y) >= self.move_range:
                self.direction *= -1

    def draw(self, surf, cam_x):
        sx = self.rect.x - cam_x
        if -self.rect.width < sx < SCREEN_WIDTH + self.rect.width:
            surf.blit(self.image, (sx, self.rect.y))


# ══════════════════════════════════════════════════════════════════════════════
#  ENEMIES
# ══════════════════════════════════════════════════════════════════════════════

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, etype, patrol_dist):
        super().__init__()
        self.etype = etype
        self.patrol_dist = patrol_dist
        self.origin_x = x
        self.alive = True
        self.dying = False
        self.die_timer = 0
        self.anim = 0
        self.vx = -1.5
        self.vy = 0.0
        self.on_ground = False
        self.facing_right = False
        self._setup(x, y)

    def _setup(self, x, y):
        if self.etype == ENEMY_GOOMBA:
            self.rect = pygame.Rect(x, y - 32, 30, 32)
            self.speed = 1.5
            self.stomp_kills = True
            self.hp = 1
        elif self.etype == ENEMY_KOOPA:
            self.rect = pygame.Rect(x, y - 40, 30, 40)
            self.speed = 1.5
            self.stomp_kills = True
            self.hp = 1
            self.shelled = False
            self.shell_timer = 0
        elif self.etype == ENEMY_FLYING_KOOPA:
            self.rect = pygame.Rect(x, y - 40, 30, 40)
            self.speed = 1.5
            self.stomp_kills = True
            self.hp = 1
            self.shelled = False
            self.fly_y = float(y - 40)
            self.fly_origin = float(y - 40)
        elif self.etype == ENEMY_BOSS:
            self.rect = pygame.Rect(x, y - 80, 60, 80)
            self.speed = 1.0
            self.stomp_kills = True
            self.hp = 3
            self.vx = -1.0

    def update(self, solid_tiles, player_x):
        if self.dying:
            self.die_timer += 1
            if self.etype == ENEMY_KOOPA and self.shelled:
                self.rect.y += 3
            return

        self.anim += 0.12

        if self.etype == ENEMY_FLYING_KOOPA:
            self._update_flying()
        else:
            self._update_walking(solid_tiles)

    def _update_flying(self):
        self.fly_y += math.sin(self.anim) * 1.5
        self.rect.y = int(self.fly_y)
        self.rect.x += int(self.vx)
        # Patrol
        if abs(self.rect.x - self.origin_x) > max(self.patrol_dist, 80):
            self.vx *= -1
            self.facing_right = not self.facing_right

    def _update_walking(self, solid_tiles):
        self.vy += GRAVITY
        self.vy = min(self.vy, MAX_FALL_SPEED)

        self.rect.x += int(self.vx)
        for t in solid_tiles:
            if self.rect.colliderect(t.rect):
                if self.vx > 0:
                    self.rect.right = t.rect.left
                    self.vx = -abs(self.vx)
                else:
                    self.rect.left = t.rect.right
                    self.vx = abs(self.vx)
                self.facing_right = self.vx > 0

        self.rect.y += int(self.vy)
        self.on_ground = False
        for t in solid_tiles:
            if self.rect.colliderect(t.rect):
                if self.vy > 0:
                    self.rect.bottom = t.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = t.rect.bottom
                    self.vy = 1

        # Patrol boundaries
        if self.patrol_dist > 0:
            if abs(self.rect.x - self.origin_x) > self.patrol_dist:
                self.vx *= -1
                self.facing_right = self.vx > 0

        # Fall off ledge detection
        if self.on_ground and self.etype != ENEMY_BOSS:
            check_x = self.rect.right + 2 if self.vx > 0 else self.rect.left - 2
            check_rect = pygame.Rect(check_x, self.rect.bottom + 1, 4, 4)
            on_edge = True
            for t in solid_tiles:
                if t.rect.colliderect(check_rect):
                    on_edge = False
                    break
            if on_edge:
                self.vx *= -1
                self.facing_right = self.vx > 0

    def stomp(self):
        """Called when player stomps this enemy. Returns score."""
        if self.etype == ENEMY_KOOPA and not self.shelled:
            self.shelled = True
            self.vx = 0
            self.shell_timer = 180
            return ENEMY_STOMP_SCORE
        elif self.etype == ENEMY_BOSS:
            self.hp -= 1
            if self.hp <= 0:
                self._die()
                return ENEMY_STOMP_SCORE * 5
            return ENEMY_STOMP_SCORE
        else:
            self._die()
            return ENEMY_STOMP_SCORE

    def kick_shell(self):
        """Returns True if shell was kicked."""
        if self.etype == ENEMY_KOOPA and self.shelled:
            self.vx = 8 if self.facing_right else -8
            return True
        return False

    def _die(self):
        self.dying = True
        self.die_timer = 0
        self.vy = -6
        self.vx = 0

    def fireball_hit(self):
        if self.etype == ENEMY_BOSS:
            self.hp -= 1
            if self.hp <= 0:
                self._die()
                return ENEMY_STOMP_SCORE * 5
            return ENEMY_STOMP_SCORE
        self._die()
        return ENEMY_STOMP_SCORE

    def draw(self, surf, cam_x):
        sx = self.rect.x - cam_x
        sy = self.rect.y
        if -80 < sx < SCREEN_WIDTH + 80:
            if self.etype == ENEMY_GOOMBA:
                self._draw_goomba(surf, sx, sy)
            elif self.etype in (ENEMY_KOOPA, ENEMY_FLYING_KOOPA):
                self._draw_koopa(surf, sx, sy)
            elif self.etype == ENEMY_BOSS:
                self._draw_boss(surf, sx, sy)

    def _draw_goomba(self, surf, sx, sy):
        w, h = self.rect.width, self.rect.height
        walk_squish = int(math.sin(self.anim * 2) * 2) if not self.dying else 0

        if self.dying and self.die_timer < 30:
            # Squished
            pygame.draw.ellipse(surf, BROWN, (sx, sy + h - 10, w, 10))
            pygame.draw.ellipse(surf, DARK_BROWN, (sx+2, sy + h - 8, w-4, 6))
            return

        # Body
        pygame.draw.ellipse(surf, BROWN, (sx, sy + walk_squish, w, h - walk_squish))
        # Feet
        foot_off = int(math.sin(self.anim * 3) * 3)
        pygame.draw.ellipse(surf, DARK_BROWN, (sx - 2, sy + h - 10, 14, 10))
        pygame.draw.ellipse(surf, DARK_BROWN, (sx + w - 12, sy + h - 10, 14, 10))
        # Eyes
        ew = w // 2
        draw_eye(surf, sx + ew//2, sy + h//3, not self.facing_right)
        draw_eye(surf, sx + ew + ew//2, sy + h//3, not self.facing_right)
        # Eyebrows (angry)
        pygame.draw.line(surf, BLACK, (sx+4, sy+h//3-8), (sx+ew-2, sy+h//3-5), 2)
        pygame.draw.line(surf, BLACK, (sx+ew+2, sy+h//3-5), (sx+w-4, sy+h//3-8), 2)
        # Mouth
        pygame.draw.arc(surf, DARK_BROWN,
                        pygame.Rect(sx+6, sy+h//2, w-12, h//4),
                        math.pi, 2*math.pi, 2)

    def _draw_koopa(self, surf, sx, sy):
        w, h = self.rect.width, self.rect.height
        is_flying = self.etype == ENEMY_FLYING_KOOPA

        if self.dying:
            if self.die_timer < 40:
                # Shell spinning
                shell_col = (40, 160, 40) if not is_flying else (100, 100, 200)
                pygame.draw.ellipse(surf, shell_col, (sx, sy + h//2, w, h//2))
                pygame.draw.ellipse(surf, (60, 200, 60), (sx+4, sy+h//2+4, w-8, h//2-8))
            return

        if hasattr(self, 'shelled') and self.shelled:
            # Shell only
            pygame.draw.ellipse(surf, (40, 160, 40), (sx, sy + h//3, w, 2*h//3))
            pygame.draw.ellipse(surf, LIGHT_GREEN, (sx+4, sy+h//3+4, w-8, 2*h//3-8))
            # Cross on shell
            pygame.draw.line(surf, (30, 120, 30), (sx+w//2, sy+h//3+2), (sx+w//2, sy+h-2), 2)
            pygame.draw.line(surf, (30, 120, 30), (sx+4, sy+h//3+h//3), (sx+w-4, sy+h//3+h//3), 2)
            return

        shell_col = (100, 100, 200) if is_flying else (40, 160, 40)
        shell_lite = (140, 140, 240) if is_flying else LIGHT_GREEN

        # Feet
        walk = int(math.sin(self.anim*3) * 3) if not is_flying else 0
        pygame.draw.ellipse(surf, DARK_GREEN, (sx-2, sy+h-12+walk, 14, 10))
        pygame.draw.ellipse(surf, DARK_GREEN, (sx+w-12, sy+h-12-walk, 14, 10))
        # Shell
        pygame.draw.ellipse(surf, shell_col, (sx, sy+h//3, w, 2*h//3))
        pygame.draw.ellipse(surf, shell_lite, (sx+4, sy+h//3+4, w-8, h//3))
        # Cross
        pygame.draw.line(surf, tuple(max(0,c-30) for c in shell_col),
                         (sx+w//2, sy+h//3+2), (sx+w//2, sy+h-2), 2)
        # Head
        pygame.draw.ellipse(surf, (120, 200, 80), (sx+3, sy, w-6, h//2))
        # Eyes
        ex = sx + w//2 + (5 if self.facing_right else -5)
        draw_eye(surf, ex, sy + h//4, self.facing_right)
        # Beak
        beak_x = sx+w-4 if self.facing_right else sx
        pygame.draw.polygon(surf, ORANGE, [
            (beak_x, sy+h//3),
            (beak_x + (8 if self.facing_right else -8), sy+h//3+4),
            (beak_x, sy+h//3+8),
        ])
        # Wings for flying
        if is_flying:
            wing_flap = math.sin(self.anim*4) * 8
            if self.facing_right:
                pygame.draw.polygon(surf, WHITE, [
                    (sx-5, sy+h//3+5),
                    (sx-16, sy+h//3-int(wing_flap)),
                    (sx-8, sy+h//3+15),
                ])
            else:
                pygame.draw.polygon(surf, WHITE, [
                    (sx+w+5, sy+h//3+5),
                    (sx+w+16, sy+h//3-int(wing_flap)),
                    (sx+w+8, sy+h//3+15),
                ])

    def _draw_boss(self, surf, sx, sy):
        w, h = self.rect.width, self.rect.height
        walk = int(math.sin(self.anim*2) * 3)

        # Body
        pygame.draw.rect(surf, (50, 120, 50), (sx, sy+h//3, w, 2*h//3), border_radius=8)
        # Shell on back
        pygame.draw.ellipse(surf, (30, 80, 30), (sx-5, sy+h//4, w+10, 2*h//3))
        pygame.draw.ellipse(surf, (60, 140, 60), (sx, sy+h//4+5, w, h//3))
        # Head
        pygame.draw.ellipse(surf, (80, 160, 60), (sx+5, sy, w-10, h//2))
        # Eyes
        draw_eye(surf, sx+w//3, sy+h//4, not self.facing_right)
        draw_eye(surf, sx+2*w//3, sy+h//4, not self.facing_right)
        # Horns
        pygame.draw.polygon(surf, ORANGE, [
            (sx+10, sy), (sx+4, sy-18), (sx+18, sy-2)
        ])
        pygame.draw.polygon(surf, ORANGE, [
            (sx+w-10, sy), (sx+w-4, sy-18), (sx+w-18, sy-2)
        ])
        # Spiked shell row
        for i in range(4):
            ix = sx + 8 + i*12
            pygame.draw.polygon(surf, ORANGE, [
                (ix, sy+h//4),
                (ix+4, sy+h//4-10),
                (ix+8, sy+h//4),
            ])
        # HP bar
        for i in range(3):
            col = RED if i < self.hp else DARK_GRAY
            pygame.draw.rect(surf, col, (sx + i*20 + 2, sy-16, 16, 10), border_radius=3)
        # Arms / claws
        pygame.draw.ellipse(surf, (50, 120, 50), (sx-14, sy+h//2, 18, 30))
        pygame.draw.ellipse(surf, (50, 120, 50), (sx+w-4, sy+h//2, 18, 30))
        # Claws
        for dx in [-3, 3]:
            pygame.draw.line(surf, (30,80,30), (sx-5+dx, sy+h//2+28),(sx-5+dx, sy+h//2+36),3)
            pygame.draw.line(surf, (30,80,30), (sx+w+9+dx,sy+h//2+28),(sx+w+9+dx,sy+h//2+36),3)
        # Feet
        pygame.draw.ellipse(surf, (40, 100, 40), (sx+5, sy+h-14+walk, 22, 14))
        pygame.draw.ellipse(surf, (40, 100, 40), (sx+w-27, sy+h-14-walk, 22, 14))


# ══════════════════════════════════════════════════════════════════════════════
#  FLAG / GOAL
# ══════════════════════════════════════════════════════════════════════════════

class FlagPole:
    def __init__(self, x, theme):
        self.x = x
        self.pole_x = x + 8
        self.top_y = 200
        self.bottom_y = 544
        self.theme = theme
        self.flag_y = 210.0
        self.sliding = False
        self.done = False

    def start_slide(self):
        self.sliding = True

    def update(self):
        if self.sliding and self.flag_y < 500:
            self.flag_y += 4

    def draw(self, surf, cam_x):
        sx = self.pole_x - cam_x
        if -50 < sx < SCREEN_WIDTH + 50:
            # Pole
            pygame.draw.line(surf, GRAY, (sx, self.top_y), (sx, self.bottom_y), 5)
            # Ball on top
            pygame.draw.circle(surf, GOLD, (sx, self.top_y), 8)
            # Flag
            fy = int(self.flag_y)
            pygame.draw.polygon(surf, GREEN, [
                (sx, fy), (sx+24, fy+8), (sx, fy+16)
            ])
            pygame.draw.line(surf, DARK_GREEN, (sx, fy), (sx, fy+16), 2)


# ══════════════════════════════════════════════════════════════════════════════
#  PLAYER
# ══════════════════════════════════════════════════════════════════════════════

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.facing_right = True
        self.on_ground = False
        self.state = "small"   # small, big, fire
        self.invincible = False
        self.inv_timer = 0
        self.star_timer = 0
        self.fire_cooldown = 0
        self.jump_hold = 0
        self.is_jumping = False
        self.walk_anim = 0
        self.alive = True
        self.dying = False
        self.die_timer = 0
        self.die_vy = -14
        self.growing = False
        self.grow_timer = 0
        self.crouching = False

        self._update_rect()

    def _update_rect(self):
        if self.state == "small":
            w, h = PLAYER_SMALL_W, PLAYER_SMALL_H
        else:
            w, h = PLAYER_BIG_W, PLAYER_BIG_H
        old_bottom = self.y + (PLAYER_SMALL_H if self.state == "small" else PLAYER_BIG_H)
        self.rect = pygame.Rect(int(self.x), int(self.y), w, h)

    @property
    def w(self):
        return self.rect.width

    @property
    def h(self):
        return self.rect.height

    def grow(self, new_state):
        if new_state == "fire" and self.state in ("small", "big"):
            self.state = "fire"
            self.growing = True
            self.grow_timer = 30
        elif new_state == "big" and self.state == "small":
            old_bottom = self.rect.bottom
            self.state = "big"
            self._update_rect()
            self.rect.bottom = old_bottom
            self.y = float(self.rect.y)
            self.growing = True
            self.grow_timer = 20
        elif new_state == "star":
            self.star_timer = 600
            self.invincible = True

    def get_hit(self):
        if self.invincible:
            return False
        if self.state in ("big", "fire"):
            old_bottom = self.rect.bottom
            self.state = "small"
            self._update_rect()
            self.rect.bottom = old_bottom
            self.y = float(self.rect.y)
            self.invincible = True
            self.inv_timer = 120
            return False  # not dead, just shrunk
        return True  # small -> die

    def die(self):
        self.dying = True
        self.alive = False
        self.die_timer = 0
        self.vy = self.die_vy
        self.vx = 0

    def jump(self, holding=False):
        if not holding:
            if self.on_ground:
                self.vy = JUMP_FORCE
                self.on_ground = False
                self.is_jumping = True
                self.jump_hold = 0
                return True
        else:
            if self.is_jumping and self.jump_hold < MAX_JUMP_HOLD and self.vy < 0:
                self.vy += JUMP_HOLD_FORCE
                self.jump_hold += 1
        return False

    def update(self, keys, solid_tiles, dt=1.0):
        if self.dying:
            self.die_timer += 1
            self.vy += GRAVITY
            self.y += self.vy
            self.rect.y = int(self.y)
            return

        # Star timer
        if self.star_timer > 0:
            self.star_timer -= 1
            if self.star_timer == 0:
                self.invincible = False
        elif self.inv_timer > 0:
            self.inv_timer -= 1
            self.invincible = self.inv_timer > 0

        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

        # Horizontal movement
        running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        speed = PLAYER_RUN_SPEED if running else PLAYER_SPEED

        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx -= PLAYER_ACCEL
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx += PLAYER_ACCEL
            self.facing_right = True
            moving = True

        self.vx = max(-speed, min(speed, self.vx))
        if not moving:
            self.vx *= PLAYER_FRICTION
            if abs(self.vx) < 0.2:
                self.vx = 0

        # Jump hold
        jump_held = (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE])
        if jump_held and self.is_jumping:
            self.jump(holding=True)
        if not jump_held:
            self.is_jumping = False

        # Gravity
        self.vy += GRAVITY
        self.vy = min(self.vy, MAX_FALL_SPEED)

        # Move X
        self.x += self.vx
        self.rect.x = int(self.x)
        self._collide_horizontal(solid_tiles)

        # Move Y
        self.y += self.vy
        self.rect.y = int(self.y)
        self.on_ground = False
        self._collide_vertical(solid_tiles)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Walk animation
        if moving and self.on_ground:
            self.walk_anim += abs(self.vx) * 0.15
        elif not self.on_ground:
            self.walk_anim += 0.1

        # Keep on screen left edge
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = 0.0
            self.vx = 0

    def _collide_horizontal(self, tiles):
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vx > 0:
                    self.rect.right = t.rect.left
                    self.vx = 0
                elif self.vx < 0:
                    self.rect.left = t.rect.right
                    self.vx = 0
                self.x = float(self.rect.x)

    def _collide_vertical(self, tiles):
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vy > 0:
                    self.rect.bottom = t.rect.top
                    self.vy = 0
                    self.on_ground = True
                    self.is_jumping = False
                elif self.vy < 0:
                    self.rect.top = t.rect.bottom
                    self.vy = 1
        self.y = float(self.rect.y)

    def draw(self, surf, cam_x, star_active=False):
        if self.dying and self.die_timer > 60:
            return
        sx = self.rect.x - cam_x
        sy = self.rect.y

        # Invincibility flicker
        if self.inv_timer > 0 and (self.inv_timer // 4) % 2 == 0:
            return

        # Star rainbow color cycling
        if self.star_timer > 0:
            hue = (pygame.time.get_ticks() // 50) % 6
            hat_color = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE][hue]
        else:
            hat_color = RED

        if self.state == "small":
            self._draw_small(surf, sx, sy, hat_color)
        else:
            self._draw_big(surf, sx, sy, hat_color)

    def _draw_small(self, surf, sx, sy, hat_color):
        w, h = PLAYER_SMALL_W, PLAYER_SMALL_H
        walk = math.sin(self.walk_anim) if self.on_ground else 0

        # Shoes
        shoe_off = int(walk * 4)
        pygame.draw.ellipse(surf, DARK_BROWN,
                            (sx - 3, sy + h - 10 + shoe_off, 14, 10))
        pygame.draw.ellipse(surf, DARK_BROWN,
                            (sx + w - 11, sy + h - 10 - shoe_off, 14, 10))

        # Overalls (blue)
        pygame.draw.rect(surf, BLUE, (sx + 2, sy + h//2 - 2, w - 4, h//2 + 2), border_radius=4)
        # Shirt (red)
        pygame.draw.rect(surf, RED, (sx + 2, sy + h//2 - 6, w - 4, 12), border_radius=3)

        # Skin - head
        pygame.draw.ellipse(surf, TAN, (sx + 2, sy + 4, w - 4, h//2 - 2))

        # Hat
        pygame.draw.rect(surf, hat_color, (sx, sy + 4, w, 10), border_radius=3)
        pygame.draw.rect(surf, hat_color, (sx + 4, sy, w - 8, 10), border_radius=4)

        # Eye
        ex = sx + w - 9 if self.facing_right else sx + 3
        draw_eye(surf, ex + 3, sy + h//4 + 4, self.facing_right)

        # Mustache
        mx = sx + w//2
        my = sy + h//3 + 2
        pygame.draw.ellipse(surf, DARK_BROWN, (mx - 8, my, 8, 5))
        pygame.draw.ellipse(surf, DARK_BROWN, (mx, my, 8, 5))

        # Overalls straps
        pygame.draw.line(surf, DARK_BLUE,
                         (sx + 6, sy + h//2 - 6), (sx + 6, sy + h//2 - 14), 3)
        pygame.draw.line(surf, DARK_BLUE,
                         (sx + w - 6, sy + h//2 - 6), (sx + w - 6, sy + h//2 - 14), 3)

    def _draw_big(self, surf, sx, sy, hat_color):
        w, h = PLAYER_BIG_W, PLAYER_BIG_H
        walk = math.sin(self.walk_anim) if self.on_ground else 0

        # Shoes
        shoe_off = int(walk * 4)
        pygame.draw.ellipse(surf, DARK_BROWN,
                            (sx - 3, sy + h - 12 + shoe_off, 16, 12))
        pygame.draw.ellipse(surf, DARK_BROWN,
                            (sx + w - 13, sy + h - 12 - shoe_off, 16, 12))

        # Legs
        pygame.draw.rect(surf, BLUE,
                         (sx + 2, sy + 3*h//4, w//2 - 1, h//4), border_radius=3)
        pygame.draw.rect(surf, BLUE,
                         (sx + w//2 + 1, sy + 3*h//4, w//2 - 3, h//4), border_radius=3)

        # Overalls body
        pygame.draw.rect(surf, BLUE,
                         (sx + 2, sy + h//2, w - 4, h//4 + 2), border_radius=4)
        # Shirt
        pygame.draw.rect(surf, RED,
                         (sx + 2, sy + h//2 - 8, w - 4, 16), border_radius=3)

        # Head
        head_h = h // 3
        pygame.draw.ellipse(surf, TAN,
                            (sx + 2, sy + 2, w - 4, head_h))

        # Hat
        pygame.draw.rect(surf, hat_color,
                         (sx, sy + 6, w, 11), border_radius=3)
        pygame.draw.rect(surf, hat_color,
                         (sx + 4, sy, w - 8, 12), border_radius=4)

        # Eye
        ex = sx + w - 9 if self.facing_right else sx + 3
        draw_eye(surf, ex + 3, sy + head_h//2 + 6, self.facing_right)

        # Mustache
        mx = sx + w//2
        my = sy + head_h//2 + 10
        pygame.draw.ellipse(surf, DARK_BROWN, (mx - 9, my, 9, 6))
        pygame.draw.ellipse(surf, DARK_BROWN, (mx, my, 9, 6))

        # Straps
        pygame.draw.line(surf, DARK_BLUE,
                         (sx + 7, sy + h//2 - 8), (sx + 7, sy + h//2 - 18), 3)
        pygame.draw.line(surf, DARK_BLUE,
                         (sx + w - 7, sy + h//2 - 8), (sx + w - 7, sy + h//2 - 18), 3)

        # Fire state: flame on hand
        if self.state == "fire":
            fx = sx + w + 2 if self.facing_right else sx - 10
            fy = sy + h//2 + 4
            pygame.draw.circle(surf, ORANGE, (fx, fy), 7)
            pygame.draw.circle(surf, YELLOW, (fx, fy), 4)
            pygame.draw.circle(surf, WHITE,  (fx, fy), 2)
