import pygame
import sys
import math
import random
import traceback

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mini mario edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28, bold=True)
small_font = pygame.font.SysFont("Arial", 20, bold=True)
big_font = pygame.font.SysFont("Arial", 48, bold=True)


SKY = (107, 140, 255)
BRICK = (200, 100, 30)
BRICK_DARK = (0, 0, 0)
BRICK_SHADOW = (120, 50, 15)
BRICK_LIGHT = (252, 252, 252)

COIN_COLOR = (255, 215, 0)
FLAG_COLOR = (240, 240, 240)
KEY_COLOR = (255, 220, 50)
CAGE_COLOR = (180, 180, 180)
CAGE_DARK = (100, 100, 100)
PORTAL_COLOR = (150, 50, 255)



#'#' и 'B' — кирпичи. 'C' — монета, 'E' — зелёный слизень,
#'G' — фиолетовый слизень, 'F' — флаг, 'X' — босс,
#'L' — клетка, 'O' — портал, '.' — ниче.
LEVEL_1 = [
    "........................................................",
    "..........C.............................................",
    ".........BBB............................................",
    "........................................................",
    ".......B.........................B.................C....",
    ".....C..........................BB.................B....",
    "....BB.........................BBB.........BBBB....B....",
    "..............................BBBB..........BBB....B....",
    "........B.E........G.........BBBBB.......B..BBB....B....",
    "............................BBBBBB..........BBB....B...F",
    "BBBBBBBBBBBBBBB....BBBB...BBBBBBBB......BBBBBBB....BBBBB",
]

LEVEL_2 = [
    "..................................................................",
    "..................................................................",
    "..........C.....................C................C................",
    "........BBBB..................BBBB.............BBB................",
    "..............B......................B.......B....................",
    "............C............................C...B....................",
    "..........BBB.....................B.....BBB..B....................",
    ".................................BB..........B....................",
    ".......EB.............G.......E.BBB.....G....B.E..............E...",
    "...............................BBBB..........B.........BBB.......F",
    "BBBBBBBBBBBBBBBB....BBBBB...BBBBBBB..........BBBBBBBB........BBBBB",
]

LEVEL_3 = [
    "....................................................................",
    "....................................................................",
    ".....C..............C..............C................................",
    "....BB.............BB.............BB................................",
    "......B.......B..............B....B.....B...........................",
    "..........C..............C........B.....N..............C............",
    "........BB.............BB......B..B.....B............BB.............",
    "........BB..............B.........B.....B...........................",
    ".....GB.BB...E.....E.B.GB..E.B...EB..G..BE.....E...GB..E.....E...G..",
    "........BB..............B.........B.....B..........................O",
    "BBBBBBBBBB.BBBBB...BBBBBB..BBBBB..BBBBBBB..BBBBB...BBBBB...BB...BBBB",
]

LEVEL_BOSS = [
    "........................................",
    "........................................",
    "........................................",
    "........................................",
    "........................................",
    "........................................",
    "..............X................L........",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
]

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_BOSS]

def draw_brick_tile(x, y):
    s = TILE
    h = TILE // 2

    pygame.draw.rect(screen, BRICK, (x, y, s, s))
    pygame.draw.rect(screen, BRICK_SHADOW, (x, y + s - 4, s, 4))

    pygame.draw.line(screen, BRICK_DARK, (x, y + h), (x + s, y + h), 2)
    pygame.draw.line(screen, BRICK_DARK,
                     (x + s // 2, y), (x + s // 2, y + h), 2)
    pygame.draw.line(screen, BRICK_DARK,
                     (x + s // 4, y + h), (x + s // 4, y + s), 2)
    pygame.draw.line(screen, BRICK_DARK,
                     (x + 3 * s // 4, y + h), (x + 3 * s // 4, y + s), 2)

    pygame.draw.rect(screen, BRICK_DARK, (x, y, s, s), 2)


def draw_world(tiles, cam_x, map_h):
    for t in tiles:
        x = t.x - cam_x
        y = t.y
        if x + TILE < -50 or x > WIDTH + 50:
            continue
        draw_brick_tile(x, y)

    bottom_row_by_col = {}
    for t in tiles:
        if t.x not in bottom_row_by_col or t.y > bottom_row_by_col[t.x]:
            bottom_row_by_col[t.x] = t.y

    for col_x, bottom_y in bottom_row_by_col.items():
        y = bottom_y + TILE
        while y < HEIGHT:
            sx = col_x - cam_x
            if -TILE < sx < WIDTH:
                draw_brick_tile(sx, y)
            y += TILE

class Player:
    COLOR_1  = (255, 200, 150)   
    COLOR_2  = (90, 50, 20)      
    COLOR_3  = (220, 30, 30)    
    COLOR_4  = (220, 30, 30)     
    COLOR_5  = (40, 80, 200)     
    COLOR_6  = (255, 215, 50)    
    COLOR_7  = (255, 255, 255)   
    COLOR_8  = (30, 30, 30)      
    COLOR_9  = (120, 40, 40)     
    COLOR_10 = (100, 60, 20)    

    SPRITE = [
        "................",
        ".....CCCCCC.....",
        "....CCCCCCCC....",
        "....CCCCCCCC....",
        "...CCCCCCCCCC...",
        "...HHHHHHHHHH...",
        "...HHSSSSSSHH...",
        "...HSSEESSEEH...",
        "...HSSEPPSEPS...",
        "....SSSSSSSS....",
        "....SHHHHHS.....",
        "....SSMMMMSS....",
        ".....SSSSSS.....",
        "....RRRRRRRR....",
        "...RRRRRRRRRR...",
        "..SRRRRRRRRRRS..",
        "..SSRRRRRRRRSS..",
        "....BBBBBBBB....",
        "....BBYBBYBB....",
        "....BBBBBBBB....",
        "....BBB..BBB....",
        "....BBB..BBB....",
        "....BBB..BBB....",
        "...SSSS..SSSS...",
        "..SSSSSS.SSSSSS.",
    ]

    JUMP_BUFFER_FRAMES = 8
    COYOTE_FRAMES = 8

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.65
        self.coins = 0
        self.alive = True
        self.won_level = False
        self.won_game = False
        self.jump_held = False
        self.facing = 1
        self.has_key = False
        self.hp = 3
        self.max_hp = 3
        self.invuln = 0

        self.jump_buffer = 0
        self.coyote_timer = 0

    def get_palette(self):
        return {
            'S': self.COLOR_1,   
            'H': self.COLOR_2,   
            'C': self.COLOR_3,   
            'R': self.COLOR_4,   
            'B': self.COLOR_5,   
            'Y': self.COLOR_6,   
            'E': self.COLOR_7,   
            'P': self.COLOR_8,   
            'M': self.COLOR_9,  
        }

    def take_damage(self, amount=1):
        if self.invuln > 0:
            return
        self.hp -= amount
        self.invuln = 150
        self.vy = -8
        if self.facing == 1:
            self.vx = -6
        else:
            self.vx = 6
        if self.hp <= 0:
            self.alive = False

    def update(self, tiles, enemies, boss, map_h, map_w=999999):
        keys = pygame.key.get_pressed()
        move_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -self.speed
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = self.speed
            self.facing = 1

        if self.invuln > 0:
            self.vx *= 0.9
        else:
            self.vx = move_x

        if abs(self.vx) > 30:
            self.vx = 0
        if abs(self.vy) > 40:
            self.vy = 40

        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]

        if jump_pressed and not self.jump_held:
            self.jump_buffer = self.JUMP_BUFFER_FRAMES

        if self.jump_buffer > 0:
            self.jump_buffer -= 1

        can_jump = self.on_ground or self.coyote_timer > 0

        if self.jump_buffer > 0 and can_jump:
            self.vy = self.jump_power
            self.on_ground = False
            self.jump_buffer = 0
            self.coyote_timer = 0

        self.jump_held = jump_pressed

        self.rect.x += int(self.vx)
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vx > 0:
                    self.rect.right = t.left
                elif self.vx < 0:
                    self.rect.left = t.right

        if self.rect.left < 0:
            self.rect.left = 0
            if self.vx < 0:
                self.vx = 0

        self.vy += self.gravity
        if self.vy > 20:
            self.vy = 20
        self.rect.y += int(self.vy)
        self.on_ground = False
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vy > 0:
                    self.rect.bottom = t.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = t.bottom
                    self.vy = 0

        if self.on_ground:
            self.coyote_timer = self.COYOTE_FRAMES
        else:
            if self.coyote_timer > 0:
                self.coyote_timer -= 1

        for e in enemies:
            if e.alive and self.rect.colliderect(e.rect):
                if self.vy > 0 and self.rect.bottom - e.rect.top < 25:
                    e.alive = False
                    self.vy = -10
                else:
                    self.take_damage(1)

        if boss and boss.alive:
            if self.rect.colliderect(boss.rect):
                if self.vy > 0 and self.rect.bottom - boss.rect.top < 30:
                    if boss.hit_flash <= 0:
                        boss.take_hit()
                    self.vy = -12
                else:
                    self.take_damage(1)

        if self.rect.top > map_h + 500:
            self.alive = False

        if self.invuln > 0:
            self.invuln -= 1

    def draw(self, cam_x):
        if self.invuln > 0 and (self.invuln // 8) % 2 == 0:
            return
        palette = self.get_palette()
        px = self.rect.width / len(self.SPRITE[0])
        py = self.rect.height / len(self.SPRITE)
        sprite_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        for row, line in enumerate(self.SPRITE):
            for col, ch in enumerate(line):
                color = palette.get(ch)
                if color is not None:
                    pygame.draw.rect(
                        sprite_surf, color,
                        (int(col * px), int(row * py),
                         int(px) + 1, int(py) + 1)
                    )
        if self.facing == -1:
            sprite_surf = pygame.transform.flip(sprite_surf, True, False)
        screen.blit(sprite_surf, (self.rect.x - cam_x, self.rect.y))


def draw_hearts(surface, x, y, hp, max_hp):
    for i in range(max_hp):
        cx = x + i * 35
        color = (220, 40, 40) if i < hp else (80, 80, 80)
        pygame.draw.circle(surface, color, (cx + 8, y + 8), 8)
        pygame.draw.circle(surface, color, (cx + 22, y + 8), 8)
        pygame.draw.polygon(surface, color, [
            (cx, y + 12), (cx + 30, y + 12), (cx + 15, y + 28),
        ])



#ЗЕЛЁНЫЙ СЛИЗЕНЬ

class Enemy:
    GRAVITY = 0.7
    MAX_FALL = 15

    COLOR_1 = (70, 200, 60)
    COLOR_2 = (30, 130, 40)
    COLOR_3 = (220, 255, 200)
    COLOR_4 = (255, 255, 255)
    COLOR_5 = (20, 20, 30)
    COLOR_6 = (30, 80, 30)

    SPRITE_NORMAL = [
        "................", "................", "......LLLL......",
        "....BBBBBBBB....", "...BBBBBBBBBB...", "..BBBBBBBBBBBB..",
        ".BBBBBBBBBBBBBB.", ".BBEEBBBBBBEEBB.", ".BBEPBBBBBBPEBB.",
        "BBBBBBBBBBBBBBBB", "BBBBBBMMMMBBBBBB", "BBBBBBBBBBBBBBBB",
        "BBBBBBBBBBBBBBBB", ".BBBBBBBBBBBBBB.", "..DDDDDDDDDDDD..",
        "................",
    ]
    SPRITE_SQUISH = [
        "................", "................", "................",
        "................", "................", "......LLLL......",
        "...BBBBBBBBBB...", ".BBBBBBBBBBBBBB.", "BBEEBBBBBBBBEEBB",
        "BBEPBBBBBBBBPEBB", "BBBBBBMMMMBBBBBB", "BBBBBBBBBBBBBBBB",
        "BBBBBBBBBBBBBBBB", "BBBBBBBBBBBBBBBB", "DDDDDDDDDDDDDDDD",
        "................",
    ]

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vx = 1.6
        self.vy = 0.0
        self.on_ground = False
        self.alive = True
        self.start_x = x
        self.range = 400
        self.anim_timer = 0
        self.anim_frame = 0

    def get_palette(self):
        return {
            'B': self.COLOR_1,
            'L': self.COLOR_3,
            'D': self.COLOR_2,
            'E': self.COLOR_4,
            'P': self.COLOR_5, 
            'M': self.COLOR_6, 
        }

    def _ground_ahead(self, tiles):
        if self.vx > 0:
            probe = pygame.Rect(self.rect.right + 4, self.rect.bottom + 4, 8, 4)
        else:
            probe = pygame.Rect(self.rect.left - 12, self.rect.bottom + 4, 8, 4)
        return any(probe.colliderect(t) for t in tiles)

    def update(self, tiles):
        if not self.alive:
            return
        self.anim_timer += 1
        if self.anim_timer >= 20:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2

        self.rect.x += int(self.vx)
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vx > 0:
                    self.rect.right = t.left
                else:
                    self.rect.left = t.right
                self.vx *= -1

        self.vy += self.GRAVITY
        if self.vy > self.MAX_FALL:
            self.vy = self.MAX_FALL
        self.rect.y += int(self.vy)
        self.on_ground = False
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vy > 0:
                    self.rect.bottom = t.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = t.bottom
                    self.vy = 0

        if self.on_ground and not self._ground_ahead(tiles):
            self.vx *= -1
        if abs(self.rect.x - self.start_x) > self.range:
            self.vx *= -1
        if self.rect.top > 2000:
            self.alive = False

    def draw(self, cam_x):
        if not self.alive:
            return
        sprite = self.SPRITE_NORMAL if self.anim_frame == 0 else self.SPRITE_SQUISH
        palette = self.get_palette()
        px = self.rect.width / len(sprite[0])
        py = self.rect.height / len(sprite)
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        for row, line in enumerate(sprite):
            for col, ch in enumerate(line):
                color = palette.get(ch)
                if color is not None:
                    pygame.draw.rect(surf, color,
                                     (int(col * px), int(row * py),
                                      int(px) + 1, int(py) + 1))
        screen.blit(surf, (self.rect.x - cam_x, self.rect.y))



# ФИОЛЕТОВЫЙ СЛИЗЕНЬ(который прыгает)

class Goomba:
    GRAVITY = 0.7
    MAX_FALL = 15
    JUMP_POWER = -13
    JUMP_INTERVAL = 180

    COLOR_1 = (150, 70, 220)     
    COLOR_2 = (80, 30, 130)      
    COLOR_3 = (240, 220, 255)    
    COLOR_4 = (255, 255, 255)    
    COLOR_5 = (20, 20, 30)       
    COLOR_6 = (60, 20, 90)       

    SPRITE_NORMAL = Enemy.SPRITE_NORMAL
    SPRITE_SQUISH = Enemy.SPRITE_SQUISH

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vx = 1.6
        self.vy = 0.0
        self.on_ground = False
        self.alive = True
        self.start_x = x
        self.range = 400
        self.anim_timer = 0
        self.anim_frame = 0
        self.jump_timer = 0

    def get_palette(self):
        return {
            'B': self.COLOR_1,  
            'L': self.COLOR_3,  
            'D': self.COLOR_2,  
            'E': self.COLOR_4,   
            'P': self.COLOR_5,   
            'M': self.COLOR_6, 
        }

    def _ground_ahead(self, tiles):
        if self.vx > 0:
            probe = pygame.Rect(self.rect.right + 4, self.rect.bottom + 4, 8, 4)
        else:
            probe = pygame.Rect(self.rect.left - 12, self.rect.bottom + 4, 8, 4)
        return any(probe.colliderect(t) for t in tiles)

    def update(self, tiles):
        if not self.alive:
            return
        self.anim_timer += 1
        if self.anim_timer >= 20:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2

        self.jump_timer += 1
        if self.jump_timer >= self.JUMP_INTERVAL and self.on_ground:
            if self._ground_ahead(tiles):
                self.vy = self.JUMP_POWER
                self.on_ground = False
                self.jump_timer = 0
                self.anim_frame = 1
            else:
                self.vx *= -1
                self.jump_timer = 0

        self.rect.x += int(self.vx)
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vx > 0:
                    self.rect.right = t.left
                else:
                    self.rect.left = t.right
                self.vx *= -1

        self.vy += self.GRAVITY
        if self.vy > self.MAX_FALL:
            self.vy = self.MAX_FALL
        self.rect.y += int(self.vy)
        self.on_ground = False
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vy > 0:
                    self.rect.bottom = t.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = t.bottom
                    self.vy = 0

        if self.on_ground and not self._ground_ahead(tiles):
            self.vx *= -1
        if abs(self.rect.x - self.start_x) > self.range:
            self.vx *= -1
        if self.rect.top > 2000:
            self.alive = False

    def draw(self, cam_x):
        if not self.alive:
            return
        sprite = self.SPRITE_NORMAL if self.anim_frame == 0 else self.SPRITE_SQUISH
        palette = self.get_palette()
        px = self.rect.width / len(sprite[0])
        py = self.rect.height / len(sprite)
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        for row, line in enumerate(sprite):
            for col, ch in enumerate(line):
                color = palette.get(ch)
                if color is not None:
                    pygame.draw.rect(surf, color,
                                     (int(col * px), int(row * py),
                                      int(px) + 1, int(py) + 1))
        screen.blit(surf, (self.rect.x - cam_x, self.rect.y))

class Boss:
    HIT_FLASH_FRAMES = 70
    HURT_COOLDOWN_FRAMES = 70
    ENRAGE_THRESHOLD = 3


    COLOR_1  = (60, 170, 80)    
    COLOR_2  = (240, 220, 130) 
    COLOR_3  = (200, 130, 220) 
    COLOR_4  = (250, 240, 200)
    COLOR_5  = (255, 255, 60)
    COLOR_6  = (20, 20, 20) 
    COLOR_7  = (220, 220, 220)  
    COLOR_8  = (120, 30, 30)   

    COLOR_9  = (255, 60, 60)   
    COLOR_10 = (255, 80, 40)  

    SPRITE = [
        "................",
        "..HH........HH..",
        "..HH...SS...HH..",
        "..HH..SSSS..HH..",
        "...SSSSSSSSSS...",
        "..SSEE SSSSEE SS",
        "..SSEP SSSSPE SS",
        "..SSSSSSSSSSSS..",
        "..SSSMMMMMMSSS..",
        "..SSSCCCCCCSSS..",
        "..WWSSBBBBSSWW..",
        ".WWWWBBBBBBWWWW.",
        ".WWWWBBBBBBWWWW.",
        "..WW.SBBBBBS.WW.",
        ".....SSSSSSS....",
        ".....CC...CC....",
    ]

    def __init__(self, x, y, arena_left, arena_right):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.start_y = y
        self.max_hp = 8
        self.hp = 8
        self.alive = True
        self.vx = 2.4
        self.vy = 0
        self.arena_left = arena_left
        self.arena_right = arena_right
        self.hit_flash = 0
        self.hurt_cooldown = 0
        self.facing = -1
        self.attack_timer = 0
        self.attack_cooldown = 90
        self.projectiles = []
        self.jumping = False
        self.minions = []
        self.dashing = False
        self.dash_timer = 0
        self.dash_vx = 0
        self.enraged = False

    def get_palette(self):
        if self.enraged:

            return {
                'S': (200, 80, 60), 
                'B': self.COLOR_2,   
                'W': (220, 80, 100),
                'H': self.COLOR_9,   
                'E': self.COLOR_10,  
                'P': self.COLOR_6,    
                'C': self.COLOR_7,    
                'M': self.COLOR_8,   
            }
        
        return {
            'S': self.COLOR_1,     
            'B': self.COLOR_2,      
            'W': self.COLOR_3,  
            'H': self.COLOR_4,       
            'E': self.COLOR_5,        
            'P': self.COLOR_6,        
            'C': self.COLOR_7,       
            'M': self.COLOR_8,       
        }

    def take_hit(self):
        if self.hit_flash > 0:
            return
        self.hp -= 1
        self.hit_flash = self.HIT_FLASH_FRAMES
        self.hurt_cooldown = self.HURT_COOLDOWN_FRAMES
        if self.hp <= self.ENRAGE_THRESHOLD and not self.enraged:
            self.enraged = True
            self.vx = 3.4
            self.attack_cooldown = 60
            self.projectiles.clear()
        if self.hp <= 0:
            self.alive = False

    def update(self, tiles, player):
        if not self.alive:
            return
        speed_mult = 0.3 if self.hurt_cooldown > 0 else 1.0
        dist_to_player = abs(player.rect.centerx - self.rect.centerx)

        if self.dashing:
            self.rect.x += int(self.dash_vx)
            self.dash_timer -= 1
            if self.rect.x < self.arena_left:
                self.rect.x = self.arena_left
                self.dashing = False
            if self.rect.right > self.arena_right:
                self.rect.right = self.arena_right
                self.dashing = False
            if self.rect.colliderect(player.rect):
                player.take_damage(1)
                self.dashing = False
            if self.dash_timer <= 0:
                self.dashing = False
        elif not self.jumping:
            self.rect.x += int(self.vx * speed_mult)
            if self.rect.x < self.arena_left:
                self.rect.x = self.arena_left
                self.vx *= -1
            if self.rect.right > self.arena_right:
                self.rect.right = self.arena_right
                self.vx *= -1

        self.facing = -1 if player.rect.centerx < self.rect.centerx else 1

        if self.jumping:
            self.vy += 0.7
            self.rect.y += int(self.vy)
            if self.rect.y >= self.start_y:
                self.rect.y = self.start_y
                self.vy = 0
                self.jumping = False
                shock_l = pygame.Rect(self.rect.centerx - 180,
                                      self.rect.bottom - 30, 180, 40)
                shock_r = pygame.Rect(self.rect.centerx,
                                      self.rect.bottom - 30, 180, 40)
                if shock_l.colliderect(player.rect) or shock_r.colliderect(player.rect):
                    player.take_damage(1)
        else:
            if self.hurt_cooldown <= 0 and dist_to_player < 600:
                self.attack_timer += 1
                if self.attack_timer >= self.attack_cooldown:
                    self.attack_timer = 0
                    self.choose_attack(player, dist_to_player)

        for p in self.projectiles:
            p['rect'].x += int(p['vx'])
            p['rect'].y += int(p['vy'])
            if p['type'] == 'arc':
                p['vy'] += 0.18
            p['life'] -= 1
        self.projectiles = [p for p in self.projectiles
                            if p['life'] > 0
                            and self.arena_left - 800 < p['rect'].x < self.arena_right + 800]

        for m in self.minions[:]:
            if not m['alive']:
                self.minions.remove(m)
                continue
            m['rect'].x += int(m['vx'])
            if m['rect'].left < self.arena_left:
                m['rect'].left = self.arena_left              
                m['vx'] *= -1
            if m['rect'].right > self.arena_right:
                m['rect'].right = self.arena_right
                m['vx'] *= -1

        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.hurt_cooldown > 0:
            self.hurt_cooldown -= 1

    def choose_attack(self, player, dist):
        roll = random.random()
        if self.enraged:
            if dist < 180:
                if roll < 0.5:
                    self.start_jump(player)
                else:
                    self.start_dash(player)
            elif dist > 400:
                if roll < 0.5:
                    self.spread_shot(player)
                else:
                    self.shoot_volley(player)
            else:
                if roll < 0.4:
                    self.start_dash(player)
                elif roll < 0.7:
                    self.spread_shot(player)
                else:
                    self.start_jump(player)
        else:
            if dist < 150:
                self.start_jump(player)
            elif dist > 350:
                self.shoot_volley(player)
            else:
                if roll < 0.4:
                    self.shoot_volley(player)
                elif roll < 0.7:
                    self.start_jump(player)
                else:
                    self.spread_shot(player)

    def start_jump(self, player):
        self.jumping = True
        self.vy = -14
        self.vx = 4 if player.rect.centerx > self.rect.centerx else -4

    def start_dash(self, player):
        self.dashing = True
        self.dash_timer = 30
        self.dash_vx = 12 if player.rect.centerx > self.rect.centerx else -12

    def shoot_volley(self, player):
        base_dx = player.rect.centerx - self.rect.centerx
        base_dy = player.rect.centery - self.rect.centery
        base_angle = math.atan2(base_dy, base_dx)
        for offset in [-0.25, 0, 0.25]:
            angle = base_angle + offset
            speed = 6
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            proj = pygame.Rect(self.rect.centerx - 8, self.rect.centery - 8, 16, 16)
            self.projectiles.append({
                'rect': proj, 'vx': vx, 'vy': vy,
                'life': 200, 'type': 'straight'
            })

    def spread_shot(self, player):
        for angle_deg in range(0, 360, 51):
            angle = math.radians(angle_deg)
            speed = 4
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            proj = pygame.Rect(self.rect.centerx - 8, self.rect.centery - 8, 16, 16)
            self.projectiles.append({
                'rect': proj, 'vx': vx, 'vy': vy,
                'life': 200, 'type': 'arc'
            })

    def check_projectile_hit(self, player):
        if not self.alive:
            return False
        for p in self.projectiles[:]:
            if p['rect'].colliderect(player.rect):
                self.projectiles.remove(p)
                return True
        return False

    def draw(self, cam_x):
        if not self.alive:
            return

        if self.attack_timer > self.attack_cooldown - 30 and not self.jumping and not self.dashing:
            pygame.draw.circle(screen, (255, 220, 100),
                               (self.rect.centerx - cam_x, self.rect.top - 20), 8)

        if self.enraged:
            pygame.draw.rect(screen, (255, 80, 50),
                             (self.rect.x - cam_x - 5, self.rect.y - 5,
                              self.rect.width + 10, self.rect.height + 10), 2)

        sprite = self.SPRITE
        palette = self.get_palette()
        flashing = self.hit_flash > 0 and (self.hit_flash // 6) % 2 == 0
        px = self.rect.width / len(sprite[0])
        py = self.rect.height / len(sprite)
        surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        for row, line in enumerate(sprite):
            for col, ch in enumerate(line):
                color = palette.get(ch)
                if color is not None:
                    if flashing:
                        color = (255, 255, 255)
                    pygame.draw.rect(surf, color,
                                     (int(col * px), int(row * py),
                                      int(px) + 1, int(py) + 1))
        if self.facing == 1:
            surf = pygame.transform.flip(surf, True, False)
        screen.blit(surf, (self.rect.x - cam_x, self.rect.y))

        for p in self.projectiles:
            px_ = p['rect'].x - cam_x + 8
            py_ = p['rect'].y + 8
            c1 = (255, 100, 30)
            c2 = (255, 220, 100)
            if p['type'] == 'arc':
                c1 = (200, 50, 255)
                c2 = (255, 180, 255)
            pygame.draw.circle(screen, c1, (px_, py_), 8)
            pygame.draw.circle(screen, c2, (px_, py_), 4)
#ПРЕДМЕТЫ
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 8, y + 8, 24, 24)
        self.collected = False

    def draw(self, cam_x):
        if self.collected:
            return
        cx = self.rect.x - cam_x + 12
        cy = self.rect.y + 12
        pygame.draw.circle(screen, COIN_COLOR, (cx, cy), 12)
        pygame.draw.circle(screen, (200, 160, 0), (cx, cy), 12, 2)
        pygame.draw.circle(screen, (255, 240, 100), (cx - 3, cy - 3), 3)

class Key:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.vy = -3
        self.collected = False
        self.on_ground = False

    def update(self, tiles):
        if self.collected or self.on_ground:
            return
        self.vy += 0.5
        self.rect.y += int(self.vy)
        for t in tiles:
            if self.rect.colliderect(t):
                if self.vy > 0:
                    self.rect.bottom = t.top
                    self.vy = 0
                    self.on_ground = True

    def draw(self, cam_x):
        if self.collected:
            return
        cx = self.rect.centerx - cam_x
        cy = self.rect.y + 10
        pygame.draw.circle(screen, KEY_COLOR, (cx, cy), 8)
        pygame.draw.circle(screen, (200, 160, 0), (cx, cy), 8, 2)
        pygame.draw.circle(screen, (50, 40, 20), (cx, cy), 3)
        pygame.draw.rect(screen, KEY_COLOR, (cx - 2, cy + 8, 4, 14))
        pygame.draw.rect(screen, KEY_COLOR, (cx + 2, cy + 16, 5, 3))
        pygame.draw.rect(screen, KEY_COLOR, (cx + 2, cy + 21, 5, 3))

class Cage:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - TILE, TILE * 3, TILE * 2)
        self.opened = False
        self.flag_rect = pygame.Rect(x + TILE, y - TILE, 20, TILE * 2)

    def draw(self, cam_x):
        x = self.rect.x - cam_x
        y = self.rect.y
        if not self.opened:
            cage_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            cage_surf.fill((100, 100, 100, 60))
            screen.blit(cage_surf, (x, y))
            for i in range(0, self.rect.width + 1, 20):
                pygame.draw.rect(screen, CAGE_COLOR, (x + i - 3, y, 6, self.rect.height))
            pygame.draw.rect(screen, CAGE_DARK, (x, y, self.rect.width, 6))
            pygame.draw.rect(screen, CAGE_DARK,
                             (x, y + self.rect.height - 6, self.rect.width, 6))
            pygame.draw.rect(screen, (220, 180, 40),
                             (x + self.rect.width // 2 - 8,
                              y + self.rect.height // 2 - 10, 16, 20))
            pygame.draw.circle(screen, (80, 60, 20),
                               (x + self.rect.width // 2,
                                y + self.rect.height // 2 - 2), 3)

        fx = self.flag_rect.x - cam_x
        fy = self.flag_rect.y
        pygame.draw.rect(screen, (100, 100, 100), (fx + 8, fy, 4, TILE * 2))
        pygame.draw.polygon(screen, FLAG_COLOR, [
            (fx + 12, fy + 10), (fx + 12, fy + 50), (fx + 50, fy + 30),
        ])

    def try_open(self, player_has_key):
        if player_has_key and not self.opened:
            self.opened = True
            return True
        return False

class Portal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 5, y - TILE, TILE - 10, TILE * 2)
        self.phase = 0.0

    def update(self):
        self.phase += 0.15

    def draw(self, cam_x):
        cx = self.rect.centerx - cam_x
        cy = self.rect.centery
        for r in range(45, 5, -8):
            pulse = math.sin(self.phase + r * 0.2)
            if pulse > 0:
                pygame.draw.circle(screen, PORTAL_COLOR, (cx, cy), r, 2)
        pygame.draw.polygon(screen, PORTAL_COLOR, [
            (cx, cy - 10), (cx + 10, cy), (cx, cy + 10), (cx - 10, cy),
        ], 2)

# СБОРКА УРОВНЯ
def build_level(level_data):
    tiles = []
    enemies = []
    coins = []
    flag = None
    boss = None
    cage = None
    portal = None

    for row, line in enumerate(level_data):
        for col, ch in enumerate(line):
            x, y = col * TILE, row * TILE
            # '#' и 'B' — теперь и то, и другое кирпич
            if ch == '#' or ch == 'B':
                tiles.append(pygame.Rect(x, y, TILE, TILE))
            elif ch == 'C':
                coins.append(Coin(x, y))
            elif ch == 'E':
                enemies.append(Enemy(x, y + 8))
            elif ch == 'G':
                enemies.append(Goomba(x, y + 8))
            elif ch == 'F':
                flag = pygame.Rect(x, y + TILE - TILE * 2, 40, TILE * 2)
            elif ch == 'X':
                arena_left = max(0, x - TILE * 6)
                arena_right = min(len(level_data[0]) * TILE, x + TILE * 8)
                boss = Boss(x, y - 24, arena_left, arena_right)
            elif ch == 'L':
                cage = Cage(x, y)
            elif ch == 'O':
                portal = Portal(x, y)
    return tiles, enemies, coins, flag, boss, cage, portal


def draw_background(cam_x, map_w):
    screen.fill(SKY)
    cloud_offset = cam_x * 0.3
    for i in range(12):
        cx = int(i * 350 - cloud_offset) % (map_w + 700) - 200
        cy = 80 + (i * 37) % 180
        pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 30)
        pygame.draw.circle(screen, (255, 255, 255), (cx + 30, cy - 10), 40)
        pygame.draw.circle(screen, (255, 255, 255), (cx + 70, cy), 30)
        pygame.draw.ellipse(screen, (220, 220, 240),
                            (cx - 20, cy + 15, 130, 15))


def load_level(index, total_coins):
    level_data = LEVELS[index]
    max_len = max(len(line) for line in level_data)
    level_data = [line.ljust(max_len, '.') for line in level_data]
    level_data = [line[:max_len] for line in level_data]

    map_w = max_len * TILE
    map_h = len(level_data) * TILE

    tiles, enemies, coins, flag, boss, cage, portal = build_level(level_data)

    ground_row = len(level_data) - 1
    for i in range(len(level_data) - 1, -1, -1):
        if level_data[i].count('#') + level_data[i].count('B') > 10:
            ground_row = i
            break

    start_x = TILE
    start_y = ground_row * TILE - 40
    player = Player(start_x, start_y)
    player.coins = total_coins
    return player, tiles, enemies, coins, flag, boss, cage, portal, map_w, map_h

def main():
    current_level = 0
    total_coins = 0
    (player, tiles, enemies, coins, flag,
     boss, cage, portal, MAP_W, MAP_H) = load_level(current_level, total_coins)
    cam_x = 0
    transition_timer = 0
    spawned_key = None
    boss_seen = False

    running = True
    while running:
        clock.tick(FPS)

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        current_level = 0
                        total_coins = 0
                        (player, tiles, enemies, coins, flag,
                         boss, cage, portal, MAP_W, MAP_H) = load_level(current_level, total_coins)
                        cam_x = 0
                        transition_timer = 0
                        spawned_key = None
                        boss_seen = False

            if player.alive and not player.won_game:
                if not player.won_level:
                    player.update(tiles, enemies, boss, MAP_H, MAP_W)
                    for e in enemies:
                        e.update(tiles)
                    if portal:
                        portal.update()

                    if boss:
                        boss.update(tiles, player)
                        if abs(boss.rect.centerx - player.rect.centerx) < 400:
                            boss_seen = True
                        if boss.check_projectile_hit(player):
                            player.take_damage(1)
                        if not boss.alive and spawned_key is None:
                            spawned_key = Key(boss.rect.centerx, boss.rect.centery)

                    if spawned_key and not spawned_key.collected:
                        spawned_key.update(tiles)
                        if spawned_key.rect.colliderect(player.rect):
                            spawned_key.collected = True
                            player.has_key = True

                    if cage and not cage.opened:
                        if cage.rect.colliderect(player.rect):
                            cage.try_open(player.has_key)

                    for c in coins:
                        if not c.collected and player.rect.colliderect(c.rect):
                            c.collected = True
                            player.coins += 1

                    if portal and player.rect.colliderect(portal.rect):
                        player.won_level = True
                        transition_timer = FPS

                    if cage and cage.opened:
                        if player.rect.colliderect(cage.flag_rect):
                            player.won_level = True
                            transition_timer = FPS
                    elif flag and not cage and player.rect.colliderect(flag):
                        player.won_level = True
                        transition_timer = FPS
                else:
                    transition_timer -= 1
                    if transition_timer <= 0:
                        total_coins = player.coins
                        current_level += 1
                        if current_level >= len(LEVELS):
                            player.won_game = True
                        else:
                            (player, tiles, enemies, coins, flag,
                             boss, cage, portal, MAP_W, MAP_H) = load_level(current_level, total_coins)
                            cam_x = 0
                            spawned_key = None
                            boss_seen = False

            target_cam = player.rect.centerx - WIDTH // 2
            cam_x += (target_cam - cam_x) * 0.1
            cam_x = max(0, min(cam_x, MAP_W - WIDTH))

            draw_background(cam_x, MAP_W)
            draw_world(tiles, cam_x, MAP_H)

            if portal:
                portal.draw(cam_x)
            if cage:
                cage.draw(cam_x)

            if flag and not cage:
                pygame.draw.rect(screen, (100, 100, 100),
                                 (flag.x - cam_x + 15, flag.y, 4, TILE * 2))
                pygame.draw.polygon(screen, FLAG_COLOR, [
                    (flag.x - cam_x + 19, flag.y + 5),
                    (flag.x - cam_x + 19, flag.y + 40),
                    (flag.x - cam_x + 55, flag.y + 22),
                ])

            for c in coins:
                c.draw(cam_x)
            if spawned_key:
                spawned_key.draw(cam_x)
            for e in enemies:
                e.draw(cam_x)
            if boss:
                boss.draw(cam_x)
            if player.alive:
                player.draw(cam_x)

            hud = font.render(f"Уровень {current_level + 1}/{len(LEVELS)}", True, (255, 255, 255))
            screen.blit(hud, (20, 20))
            hud2 = font.render(f"Монеты: {player.coins}", True, COIN_COLOR)
            screen.blit(hud2, (20, 55))

            draw_hearts(screen, 20, 95, player.hp, player.max_hp)

            if player.has_key:
                pygame.draw.circle(screen, KEY_COLOR, (30, 150), 10)
                pygame.draw.circle(screen, (50, 40, 20), (30, 150), 4)
                key_txt = small_font.render("Ключ", True, KEY_COLOR)
                screen.blit(key_txt, (50, 140))

            progress = min(1.0, player.rect.centerx / max(1, MAP_W))
            bar_w = 200
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH - bar_w - 20, 25, bar_w, 20), 2)
            pygame.draw.rect(screen, (100, 200, 100),
                             (WIDTH - bar_w - 20, 25, int(bar_w * progress), 20))

            if boss and boss_seen and boss.alive:
                boss_bar_w = 500
                boss_bar_h = 28
                boss_bar_x = (WIDTH - boss_bar_w) // 2
                boss_bar_y = 20
                pygame.draw.rect(screen, (0, 0, 0),
                                 (boss_bar_x - 4, boss_bar_y - 4,
                                  boss_bar_w + 8, boss_bar_h + 8))
                pygame.draw.rect(screen, (60, 20, 20),
                                 (boss_bar_x, boss_bar_y, boss_bar_w, boss_bar_h))
                fill_w = int(boss_bar_w * (boss.hp / boss.max_hp))
                hp_color = (220, 40, 40) if boss.hp > 3 else (255, 120, 30)
                pygame.draw.rect(screen, hp_color,
                                 (boss_bar_x, boss_bar_y, fill_w, boss_bar_h))
                for i in range(1, boss.max_hp):
                    dx = boss_bar_x + int(boss_bar_w * i / boss.max_hp)
                    pygame.draw.rect(screen, (0, 0, 0), (dx, boss_bar_y, 2, boss_bar_h))
                title = small_font.render(
                    f"ДРАКОН {boss.hp}/{boss.max_hp}" +
                    (" [ЯРОСТЬ!]" if boss.enraged else ""),
                    True, (255, 255, 255))
                screen.blit(title, (WIDTH // 2 - title.get_width() // 2,
                                    boss_bar_y + boss_bar_h + 6))

            if not player.alive:
                msg = big_font.render("Игра окончена!", True, (255, 80, 80))
                screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
                msg2 = font.render("R — заново", True, (255, 255, 255))
                screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 20))
            elif player.won_game:
                msg = big_font.render("ПОБЕДА!", True, (255, 255, 100))
                screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 60))
                msg2 = font.render(f"Монет собрано: {player.coins}", True, COIN_COLOR)
                screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2))
                msg3 = small_font.render("R — играть снова", True, (255, 255, 255))
                screen.blit(msg3, (WIDTH // 2 - msg3.get_width() // 2, HEIGHT // 2 + 40))
            elif player.won_level:
                if current_level == 2:
                    msg = font.render("Портал активирован!", True, (180, 100, 255))
                    msg2 = small_font.render("Вход в комнату босса...", True, (255, 255, 255))
                else:
                    msg = font.render(f"Уровень {current_level + 1} пройден!", True, (100, 255, 100))
                    if current_level + 1 < len(LEVELS):
                        msg2 = small_font.render(f"Загрузка уровня {current_level + 2}...",
                                                 True, (255, 255, 255))
                    else:
                        msg2 = None
                screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 30))
                if msg2:
                    screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 20))

            pygame.display.flip()

        except Exception as e:
            print(f"[ОШИБКА] {type(e).__name__}: {e}")
            traceback.print_exc()
            pygame.time.wait(100)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()