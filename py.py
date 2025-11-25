import pygame
import sys
import random
GAME_OVER_SCREEN = False
GAME_OVER_START = None
SCALE = 3
TILE = 16
WIDTH, HEIGHT = 26 * TILE, 15 * TILE
FPS = 60
GRAVITY = 0.35
FRICTION = 0.93
FOG = 0
ACCELERATION = 0.075
MAX_SPEED = 3.75
RUN_ACCELERATION = ACCELERATION * 1.75
RUN_MAX_SPEED = MAX_SPEED * 1.8
RUN_FRICTION = 0.99
JUMP_VELOCITY = -12
DEATH_GRAVITY = 0.25   # mniejsza grawitacja niż normalna
DEATH_JUMP = -14       # trochę większy podskok w górę
LIVES = 3
FIRST_REWARD = True
rewards = pygame.sprite.Group()
PHASE = "faza1"
FAZA = 1
COIN_COUNT = 0
# SCALING
TILE *= SCALE
WIDTH *= SCALE
HEIGHT *= SCALE
ENEMY_SPEED = 1.0   # domyślna prędkość przeciwników

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Kraków")
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
timer_value = 400  # jak Mario




pygame.mixer.init()
pygame.mixer.music.load(f"music/{PHASE}.mp3")
pygame.mixer.music.play(-1)   # -1 oznacza nieskończoną pętlę
pygame.mixer.music.set_volume(0.5)  # głośność 0.0–1.0
jump_sound = pygame.mixer.Sound("sounds/jump.mp3")
jump_sound.set_volume(0.2)
goomba_sound = pygame.mixer.Sound("sounds/stomp.mp3")
goomba_sound.set_volume(0.3)
death_sound = pygame.mixer.Sound("sounds/death.mp3")
death_sound.set_volume(0.3)
game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")
game_over_sound.set_volume(0.5)
# LEVEL MAP
LEVEL_MAP = [
"...............................................................................................................................................................................................................................",
"...............................................................................................................................................................................................................................",
".......................................................................................................................................................................................................~.......................",
"......................................................................................................................................................................................................@`.......................",
".......................................................................................................................................................................................................!.......................",
"......................?.........................................................BBBBBBBB...BBB?..............?............BBB....B??B........................................................QQ........|.......................",
"............................................................................................................................................................................................QQQ........|.......................",
"...........................................................................................................................................................................................QQQQ........|.......................",
"...............................................................?..........................................................................................................................QQQQQ........|.......................",
"...................?B?B?B.....................-+.........-+..................B?B..............B.....BB....?..?..?.....B...........BB......Q..Q..........QQ..Q............BB?B............QQQQQQ........|.......................",
"......................................-+......[].........[]..............................................................................QQ..QQ........QQQ..QQ..........................QQQQQQQ........|.......................",
"............................-+........[]......[].........[].............................................................................QQQ..QQQ......QQQQ..QQQ.....-+..............-+.QQQQQQQQ........|.......................",
".P..........................[]........[]E.....[]...E.E...[]......................................E.E.......E......E.E......E.E..E.E....QQQQ..QQQQ....QQQQQ..QQQQ....[].........E.E..[]QQQQQQQQQ........Q.......................",
"#####################################################################..###############...#################################################################..###################################################################",
"#####################################################################..###############...#################################################################..###################################################################",
]

COLOR_BG = (92, 148, 252)
COLOR_GROUND = (95, 62, 40)
COLOR_PLAYER = (255, 200, 0)
COLOR_ENEMY = (150, 0, 0)
font = pygame.font.Font("fonts/PressStart2P.ttf", 35)  # arcade font
font2 = pygame.font.Font("fonts/PressStart2P.ttf", 55)  # arcade font
minifont = pygame.font.Font("fonts/PressStart2P.ttf", 23)  # arcade font
hud_color = (255, 255, 255)  # biały
shadow_color = (0, 0, 0)     # czarny cień

shadow_color = (0, 0, 0)     # czarny cień

background_img = pygame.image.load("textures/background.png").convert()
background_img = pygame.transform.scale(background_img, (223 * TILE * SCALE / 3, 15 * TILE * SCALE / 3))
plate_image = pygame.image.load("textures/plate.png").convert_alpha()
ground_image = pygame.image.load("textures/ground.png").convert_alpha()
brick_image = pygame.image.load("textures/brick.png").convert_alpha()
pipe_l_image = pygame.image.load("textures/pipe_left.png").convert_alpha()
pipe_r_image = pygame.image.load("textures/pipe_right.png").convert_alpha()
pipe_l_end_image = pygame.image.load("textures/pipe_end_left.png").convert_alpha()
pipe_r_end_image = pygame.image.load("textures/pipe_end_right.png").convert_alpha()
flag1_image = pygame.image.load("textures/flag1.png").convert_alpha()
flag2_image = pygame.image.load("textures/flag2.png").convert_alpha()
flag3_image = pygame.image.load("textures/flag3.png").convert_alpha()
flag_end_image = pygame.image.load("textures/flag_end.png").convert_alpha()
pole_image = pygame.image.load("textures/pole.png").convert_alpha()
pole_image = pygame.transform.scale(pole_image, (TILE, TILE))
flag_end_image = pygame.transform.scale(flag_end_image, (TILE, TILE))
flag3_image = pygame.transform.scale(flag3_image, (TILE, TILE))
flag2_image = pygame.transform.scale(flag2_image, (TILE, TILE))
flag1_image = pygame.transform.scale(flag1_image, (TILE, TILE))
plate_image = pygame.transform.scale(plate_image, (TILE, TILE))
ground_image = pygame.transform.scale(ground_image, (TILE, TILE))
brick_image = pygame.transform.scale(brick_image, (TILE, TILE))
pipe_l_image = pygame.transform.scale(pipe_l_image, (TILE, TILE))
pipe_r_image = pygame.transform.scale(pipe_r_image, (TILE, TILE))
pipe_l_end_image = pygame.transform.scale(pipe_l_end_image, (TILE, TILE))
pipe_r_end_image = pygame.transform.scale(pipe_r_end_image, (TILE, TILE))


def load_background():
    global background_img, ACCELERATION, MAX_SPEED, RUN_ACCELERATION, RUN_MAX_SPEED, ENEMY_SPEED, enemies, goomba_frames, goomba_anim_speed, mario_death_trigger_time

    if FAZA == 1:
        background_img = pygame.image.load("textures/background.png").convert()

    elif FAZA == 2:
        background_img = pygame.image.load("textures/background2.png").convert()
        ACCELERATION = 0.075
        MAX_SPEED = 3.75
        RUN_ACCELERATION = ACCELERATION * 1.75
        RUN_MAX_SPEED = MAX_SPEED * 1.8
        ENEMY_SPEED = 0.8   # wolniejsi przeciwnicy

    elif FAZA == 3:
        background_img = pygame.image.load("textures/background3.png").convert()
        ACCELERATION = 0.075
        MAX_SPEED = 3
        RUN_ACCELERATION = ACCELERATION * 1.75
        RUN_MAX_SPEED = MAX_SPEED * 1.8
        ENEMY_SPEED = 0.5   # zamiast 0.3 → 0.5

        # wolniejsza animacja Goombów i inne sprite’y
        goomba_frames = ["textures/grzyb3.png", "textures/grzyb4.png"]
        goomba_anim_speed = 0.05  # połowa normalnej prędkości

        # losowe kaszlnięcie – rzadko
        if random.randint(1, 2000000067) == 67:
            pygame.mixer.Sound(random.choice(["sounds/cough1.mp3", "sounds/cough2.mp3"])).play()

    elif FAZA == 4:
        background_img = pygame.image.load("textures/background4.png").convert()
        ACCELERATION = 0.05
        MAX_SPEED = 2.5
        RUN_ACCELERATION = ACCELERATION * 1.75
        RUN_MAX_SPEED = MAX_SPEED * 1.8
        ENEMY_SPEED = 0
        enemies.clear()   # usuń wszystkich przeciwników

        # kaszel częściej
        if random.randint(1, 2000000067) == 67:   # szansa 1/50 na klatkę
            pygame.mixer.Sound(random.choice(["sounds/cough1.mp3", "sounds/cough2.mp3"])).play()

    elif FAZA == 5:
        background_img = pygame.image.load("textures/background5.png").convert()
        ACCELERATION = 0.02
        MAX_SPEED = 0.5
        RUN_ACCELERATION = ACCELERATION * 1.75
        RUN_MAX_SPEED = MAX_SPEED * 1.8
        ENEMY_SPEED = 1.0

        # ustaw czas wyzwolenia śmierci Mario
        mario_death_trigger_time = pygame.time.get_ticks() + 10000  # 10 sekund od startu fazy

    # skalowanie
    background_img = pygame.transform.scale(
        background_img,
        (223 * TILE * SCALE // 3, 15 * TILE * SCALE // 3)
    )


def draw_hud(screen, player, coins=0, world="1-1", time_left=400):
    # teksty
    labels = ["SCORE", "COINS", "WORLD", "TIME", "LIVES"]
    values = [f"{player.score:06}", f"{COIN_COUNT:02}", world, f"{timer_value:03}", f"{LIVES:01}"]

    # pozycje dla każdego bloku (dla prostoty dzielimy ekran)
    off = 200
    positions = [
        (WIDTH * (1/5) - off, 10),
        (WIDTH * (2/5) - off, 10),
        (WIDTH * (3/5) - off, 10),
        (WIDTH * (4/5) - off, 10),
        (WIDTH * (5/5) - off, 10)
    ]
    under = 40
    for i, (label, value) in enumerate(zip(labels, values)):
        x, y = positions[i]
        # cień
        lbl_shadow = font.render(label, True, shadow_color)
        val_shadow = font.render(value, True, shadow_color)
        screen.blit(lbl_shadow, (x+1, y+1))
        screen.blit(val_shadow, (x+1, y+under+1))  # value poniżej label

        # właściwy tekst
        lbl = font.render(label, True, hud_color)
        val = font.render(value, True, hud_color)
        screen.blit(lbl, (x, y))
        screen.blit(val, (x, y+under))

# Camera
class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    def update(self, target_rect):
        x = target_rect.centerx - WIDTH // 2.2
        if x > self.offset.x:
            self.offset.x = x
        max_x = len(LEVEL_MAP[0]) * TILE - WIDTH
        if self.offset.x > max_x:
            self.offset.x = max_x
        self.offset.y = 0
    def reset(self):
     self.offset = pygame.Vector2(0, 0)
    

# Tile
class Tile:
    def __init__(self, x, y, type='ground'):
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.type = type
        self.y_base = y
        self.bounce = 0
        self.bounce_speed = 0
        self.image = ground_image
        if type == 'plate':
            self.image = plate_image
        if type == 'pipeleft':
            self.image = pipe_l_image
        if type == 'piperight':
            self.image = pipe_r_image
        if type == 'piperightend':
            self.image = pipe_r_end_image
        if type == 'pipeleftend':
            self.image = pipe_l_end_image
        if type == 'flag1':
            self.image = flag1_image
        if type == 'flag2':
            self.image = flag2_image
        if type == 'flag3':
            self.image = flag3_image
        if type == 'pole':
            self.image = pole_image
        if type == 'flag_end':
            self.image = flag_end_image
        if type == 'brick':
            self.image = brick_image
        self.bounce_strength = 0

    def update(self, player=None):
        # podskok przy uderzeniu od dołu
        if player and self.type == 'brick':
            if player.vel.y < 0 and player.rect.top <= self.rect.bottom and player.rect.bottom > self.rect.bottom:
                if player.rect.centerx >= self.rect.left and player.rect.centerx <= self.rect.right:
                    self.bounce_speed = self.bounce_strength
                    player.vel.y = 2  # odbicie gracza w dół

        # aktualizacja podskoku
        if self.bounce_speed != 0:
            self.bounce += self.bounce_speed
            self.bounce_speed += 1  # "grawitacja" podskoku
            if self.bounce > 0:  # wraca na miejsce
                self.bounce = 0
                self.bounce_speed = 0

        self.rect.y = self.y_base + self.bounce

    def draw(self, surf, cam):
        r = cam.apply(self.rect)
        surf.blit(self.image, r)

# Player
# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 12*SCALE, 16*SCALE)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.score = 0
        self.dead = False
        self.death_timer = 0
        self.in_cutscene = False
        self.cutscene_stage = None
        self.cutscene_timer = 0
        self.last_direction_clicked = "right"

        # --- Wczytanie grafik do jednego słownika ---
        self.images = {
            "idle": pygame.image.load("textures/mario_idle.png").convert_alpha(),
            "jump": pygame.image.load("textures/mario_jump.png").convert_alpha(),
            "change": pygame.image.load("textures/mario_change.png").convert_alpha(),
            "die": pygame.image.load("textures/mario_death.png").convert_alpha(),
            "pipe1": pygame.image.load("textures/mario_pipe_1.png").convert_alpha(),
            "pipe2": pygame.image.load("textures/mario_pipe_2.png").convert_alpha(),
            "run": [
                pygame.image.load("textures/mario1.png").convert_alpha(),
                pygame.image.load("textures/mario2.png").convert_alpha(),
                pygame.image.load("textures/mario3.png").convert_alpha()
            ]
        }

        # --- Skalowanie grafik ---
        for key, img in self.images.items():
            if isinstance(img, list):
                self.images[key] = [pygame.transform.scale(i, (self.rect.width, self.rect.height)) for i in img]
            else:
                self.images[key] = pygame.transform.scale(img, (self.rect.width, self.rect.height))

        # --- Animacja startowa ---
        self.current_image = self.images["idle"]
        self.animation_index = 0
        self.animation_timer = 0

    def die(self):
        if not self.dead:
            pygame.mixer.music.stop()
            death_sound.play()
            self.dead = True
            self.death_timer = pygame.time.get_ticks()
            self.current_state = "die"
            self.current_image = self.images["die"]
            self.vel = pygame.Vector2(0, DEATH_JUMP)



    def handle_input(self, keys):
        sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        accel = RUN_ACCELERATION if sprinting else ACCELERATION
        max_speed = RUN_MAX_SPEED if sprinting else MAX_SPEED
        friction = RUN_FRICTION if sprinting else FRICTION

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.vel.x > 0: 
                self.vel.x -= 0.01
            if self.vel.x > -max_speed: 
                self.vel.x -= accel
            self.last_direction_clicked = "left"   # zapamiętaj kierunek
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.vel.x < 0: 
                self.vel.x += 0.01
            if self.vel.x < max_speed: 
                self.vel.x += accel
            self.last_direction_clicked = "right"  # zapamiętaj kierunek
        else:
            self.vel.x *= friction

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = JUMP_VELOCITY
            self.on_ground = False
            jump_sound.play()

        if self.rect.left < camera.offset.x:
            self.rect.left = camera.offset.x
            self.vel.x = 0


    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > 20: self.vel.y = 20

    def jump_cut(self):
        if self.vel.y < 0:
            self.vel.y *= 0.9

    def update(self, tiles, enemies, lucky_blocks):
             

        if self.dead:
            
            # brak sterowania, tylko grawitacja i spadek
            self.vel.y += DEATH_GRAVITY
            self.rect.y += self.vel.y
            if FAZA == 5:
                if pygame.time.get_ticks() - self.death_timer > 10000:
                    global GAME_OVER_START, GAME_OVER_SCREEN
                    if not GAME_OVER_SCREEN:
                        GAME_OVER_SCREEN = True
                        GAME_OVER_START = pygame.time.get_ticks()

                   
                    return  # zatrzymujemy da
            else:
                if pygame.time.get_ticks() - self.death_timer > 4000:
                    global LIVES
                    LIVES -= 1
                    if LIVES <= 0:
                        game_over()
                    else:
                        camera.reset()
                        reset_level()
                        self.dead = False
            return
        if self.in_cutscene:
            self.play_cutscene()
            return
        
        if FAZA == 5 and not self.dead:
            if 'mario_death_trigger_time' in globals() and pygame.time.get_ticks() >= mario_death_trigger_time:
                self.die()
                return

        for t in tiles:
            if t.type in ["flag1", "flag3", "flag_end"]:
                if self.rect.colliderect(t.rect):
                    print("TAK - dotknięcie flagi")
                    self.in_cutscene = True
                    self.cutscene_stage = "pipe"
                    self.cutscene_timer = 0
                    return
        # --- kolizje poziome ---
        self.rect.x += self.vel.x
        for t in tiles + lucky_blocks:
            # pomijamy flag2 (@)
            if getattr(t, "type", "") == "flag2":
                continue
            if self.rect.colliderect(t.rect):
                if self.vel.x > 0 and self.rect.right > t.rect.left and self.rect.left < t.rect.left:
                    self.rect.right = t.rect.left
                    self.vel.x = 0
                elif self.vel.x < 0 and self.rect.left < t.rect.right and self.rect.right > t.rect.right:
                    self.rect.left = t.rect.right
                    self.vel.x = 0

        # --- kolizje pionowe ---
        self.rect.y += self.vel.y
        self.on_ground = False
        for t in tiles + lucky_blocks:
            # pomijamy flag2 (@)
            if getattr(t, "type", "") == "flag2":
                continue
            if self.rect.colliderect(t.rect):
                if self.vel.y > 0 and self.rect.bottom > t.rect.top and self.rect.top < t.rect.top:
                    self.rect.bottom = t.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0 and self.rect.top < t.rect.bottom and self.rect.bottom > t.rect.bottom:
                    self.rect.top = t.rect.bottom
                    self.vel.y = 0

# --- sprawdzanie dotknięcia flagi ---



        # --- kolizje z przeciwnikami ---
        for e in enemies[:]:
            if self.rect.colliderect(e.rect):
                if self.vel.y > 0 and self.rect.bottom - e.rect.top < 20:
                    enemies.remove(e)
                    goomba_sound.play()
                    self.vel.y = JUMP_VELOCITY / 1.8
                    self.score += 100
                else:
                    self.die()

        # --- sprawdzanie czy stoi na ziemi ---
        self.on_ground = self.check_on_ground(tiles, lucky_blocks)

    # --- sprawdzanie czy stoi na ziemi ---


    def respawn(self, tiles):
        for r, row in enumerate(LEVEL_MAP):
            for c, ch in enumerate(row):
                if ch == 'P':
                    self.rect.topleft = (c*TILE, r*TILE)
                    self.vel = pygame.Vector2(0, 0)
                    return
    
        def play_cutscene(self):
            # etap 1: animacja pipe (Mario wchodzi w dół)
            if self.cutscene_stage == "pipe":
                self.cutscene_timer += 1
                # przełączanie sprite pipe1/pipe2
                if self.cutscene_timer % 20 < 10:
                    self.current_image = self.images["pipe1"]
                else:
                    self.current_image = self.images["pipe2"]

                # Mario powoli schodzi w dół
                self.rect.y += 1

                # po osiągnięciu pewnego Y przechodzimy do marszu
                if self.rect.y >= HEIGHT - 6*TILE:  # przykładowa wysokość
                    self.cutscene_stage = "walk"
                    self.cutscene_timer = 0

            # etap 2: marsz do zamku
            elif self.cutscene_stage == "walk":
                self.rect.x += 2  # idzie w prawo
                # animacja biegu
                self.animation_timer += 0.15
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.animation_index = (self.animation_index + 1) % len(self.images["run"])
                self.current_image = self.images["run"][self.animation_index]

                # jeśli dotarł do końca ekranu → koniec gry
                if self.rect.x > WIDTH - TILE*2:
                    pygame.mixer.Sound("sounds/level_end.mp3").play()
                    pygame.time.delay(3000)
                    pygame.quit()
                    sys.exit()

    def animate(self, keys):
        # jeśli Mario jest martwy, zawsze pokazuj sprite śmierci
        if self.dead:
            self.current_image = self.images["die"]
            return

        state = "idle"

        # skok / spadanie
        if not self.on_ground:
            state = "jump"

        # zmiana kierunku
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.vel.x > 0:
            state = "change"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.vel.x < 0:
            state = "change"

        # normalne bieganie
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
            state = "run"
        

        self.current_state = state

        # wybór grafiki
        if state == "jump":
            self.current_image = self.images["jump"]
        elif state == "run":
            self.animation_timer += 0.15
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.images["run"])
            self.current_image = self.images["run"][self.animation_index]
        elif state == "change":
            self.current_image = self.images["change"]
        else:
            self.current_image = self.images["idle"]

        # odbicie w zależności od kierunku
        if self.last_direction_clicked == "left":
            self.current_image = pygame.transform.flip(self.current_image, True, False)




    def draw(self, surf, cam):
        r = cam.apply(self.rect)
        surf.blit(self.current_image, r)

    def check_on_ground(self, tiles, lucky_blocks):
        foot_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 5)
        for t in tiles + lucky_blocks:
            # pomijamy flag2 (@)
            if getattr(t, "type", "") == "flag2":
                continue
            if foot_rect.colliderect(t.rect):
                return True
        return False


# Lucky Block
class LuckyBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # animacje "?" bloku
        self.images = [
            pygame.transform.scale(pygame.image.load("textures/lucky1.png").convert_alpha(), (TILE, TILE)),
            pygame.transform.scale(pygame.image.load("textures/lucky2.png").convert_alpha(), (TILE, TILE)),
            pygame.transform.scale(pygame.image.load("textures/lucky3.png").convert_alpha(), (TILE, TILE)),
            pygame.transform.scale(pygame.image.load("textures/lucky2.png").convert_alpha(), (TILE, TILE)),
            pygame.transform.scale(pygame.image.load("textures/lucky1.png").convert_alpha(), (TILE, TILE)),
        ]
        self.used_image = pygame.transform.scale(pygame.image.load("textures/lucky4.png").convert_alpha(), (TILE, TILE))
        self.image = self.images[0]
        self.rect = pygame.Rect(x, y, TILE, TILE)

        # animacja
        self.animation_index = 0
        self.animation_speed = 0.05
        self.timer = 0

        # bounce
        self.y_base = y
        self.bounce = 0
        self.bounce_speed = 0

        self.used = False

        # nagroda
        self.reward_pending = None
        self.reward_timer = 0
        self.reward_delay = 0
        self.milisekundy = 50
    def update(self, dt, player):
        global FIRST_REWARD, rewards

        # --- animacja "?" ---
        if not self.used:
            self.timer += self.animation_speed
            if self.timer >= 1:
                self.timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.images)
                self.image = self.images[self.animation_index]

        # --- uderzenie od dołu ---
        if not self.used:
            if player.rect.top <= self.rect.bottom and player.rect.bottom > self.rect.bottom:
                if self.rect.left <= player.rect.centerx <= self.rect.right:
                    self.used = True
                    self.image = self.used_image
                    self.bounce_speed = -8
                    player.vel.y = 2  # lekkie odbicie w dół

                    # ustaw nagrodę, ale nie wypuszczaj od razu
                    if FIRST_REWARD:
                        self.reward_pending = "mushroom"
                        self.reward_delay = self.milisekundy  # ms
                        FIRST_REWARD = False
                    else:
                        if random.randint(1, 10) == 1:
                            self.reward_pending = "mushroom"
                            self.reward_delay = self.milisekundy
                        else:
                            self.reward_pending = "coin"
                            self.reward_delay = self.milisekundy

        # --- bounce animacja ---
        if self.bounce != 0 or self.bounce_speed != 0:
            self.bounce += self.bounce_speed
            self.bounce_speed += 1
            if self.bounce > 0:
                self.bounce = 0
                self.bounce_speed = 0
                # bounce skończony → start odliczania
                if self.reward_pending and self.reward_timer == 0:
                    self.reward_timer = pygame.time.get_ticks()

        # --- sprawdzanie czy minęło opóźnienie ---
        if self.reward_pending and self.reward_timer > 0:
            if pygame.time.get_ticks() - self.reward_timer >= self.reward_delay:
                if self.reward_pending == "mushroom":
                    rewards.add(Mushroom(self.rect.x, self.rect.y - TILE))
                    pygame.mixer.Sound("sounds/appear.mp3").play()
                elif self.reward_pending == "coin":
                    rewards.add(Coin(self.rect.x, self.rect.y - TILE))
                    pygame.mixer.Sound("sounds/coin.mp3").play()
                    global COIN_COUNT
                    COIN_COUNT += 1
                self.reward_pending = None
                self.reward_timer = 0

        self.rect.y = self.y_base + self.bounce

        # --- kolizje blokujące gracza ---
        if player.rect.colliderect(self.rect):
            if player.vel.y >= 0 and player.rect.bottom <= self.rect.top + 10:
                player.rect.bottom = self.rect.top
                player.vel.y = 0
                player.on_ground = True
            elif player.vel.y < 0 and player.rect.top < self.rect.bottom:
                player.rect.top = self.rect.bottom
                player.vel.y = 0
            elif player.vel.x > 0 and player.rect.left < self.rect.right:
                player.rect.right = self.rect.left
                player.vel.x = 0
            elif player.vel.x < 0 and player.rect.right > self.rect.left:
                player.rect.left = self.rect.right
                player.vel.x = 0

    def draw(self, surf, cam):
        r = cam.apply(self.rect)
        surf.blit(self.image, r)





class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = pygame.image.load("textures/pieczarka.png").convert_alpha()
        self.image = pygame.transform.scale(img, (TILE, TILE))
        self.rect = self.image.get_rect(topleft=(x, y + TILE))

        # parametry ruchu
        self.vel = pygame.Vector2(0, 0)
        self.gravity = 0.6
        self.speed_x = 1.2

        # animacja wynurzania się
        self.spawn_timer = 0
        self.spawn_duration = TILE
        self.spawning = True

    def update(self, tiles, player, lucky_blocks):
        if self.spawning:
            # powolne wynurzanie się z lucky blocka
            self.spawn_timer += 1
            self.rect.y -= 1
            if self.spawn_timer >= self.spawn_duration:
                self.spawning = False
                self.vel.x = self.speed_x
            return

        # --- ruch poziomy ---
        self.rect.x += self.vel.x
        for t in tiles + lucky_blocks:  # teraz lucky blocki też liczymy jako platformy
            if self.rect.colliderect(t.rect):
                if self.vel.x > 0:  # ruch w prawo → odbicie w lewo
                    self.rect.right = t.rect.left
                    self.vel.x = -self.speed_x
                elif self.vel.x < 0:  # ruch w lewo → odbicie w prawo
                    self.rect.left = t.rect.right
                    self.vel.x = self.speed_x

        # --- grawitacja ---
        self.vel.y += self.gravity
        if self.vel.y > 8:
            self.vel.y = 8
        self.rect.y += self.vel.y

        # --- kolizja pionowa (podłoże, lucky blocki) ---
        for t in tiles + lucky_blocks:
            if self.rect.colliderect(t.rect):
                if self.vel.y > 0:  # spadanie
                    self.rect.bottom = t.rect.top
                    self.vel.y = 0

        # --- zebranie przez gracza ---
        if self.rect.colliderect(player.rect):
            global LIVES
            LIVES += 1
            pygame.mixer.Sound("sounds/mushroom.mp3").play()
            self.kill()




class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [
            pygame.image.load("textures/coin1.png").convert_alpha(),
            pygame.image.load("textures/coin2.png").convert_alpha(),
            pygame.image.load("textures/coin3.png").convert_alpha(),
            pygame.image.load("textures/coin4.png").convert_alpha()
        ]
        self.frame_index = 0
        self.image = pygame.transform.scale(self.frames[self.frame_index], (8 * SCALE, 14 * SCALE))
        # startuje dokładnie w środku lucky blocka
        self.rect = self.image.get_rect(topleft=(x + 4 * SCALE, y + TILE))

        # animacja ruchu
        self.start_y = self.rect.y
        self.target_up = self.start_y - 3 * TILE   # 4 kafle w górę
        self.target_down = self.start_y            # wróci na dół

        self.state = "up"      # zaczyna od ruchu w górę
        self.timer = 0

        # prędkości (dopasowane do FPS=60)
        self.up_duration = FPS * 0.35      # 1 sekunda
        self.pause_duration = int(FPS * 0.0)  # 0.2 sekundy
        self.down_duration = FPS * 0.35     # 1 sekunda

    def update(self, tiles, player, lucky_blocks):
        self.timer += 1

        # --- animacja klatek monety ---
        if self.timer % 5 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.frame_index], (8 * SCALE, 14 * SCALE))

        # --- ruch w górę ---
        if self.state == "up":
            step = (3 * TILE) / self.up_duration
            self.rect.y -= step
            if self.timer >= self.up_duration:
                self.state = "pause"
                self.timer = 0

        # --- pauza na górze ---
        elif self.state == "pause":
            if self.timer >= self.pause_duration:
                self.state = "down"
                self.timer = 0

        # --- ruch w dół ---
        elif self.state == "down":
            step = (3 * TILE) / self.down_duration
            self.rect.y += step
            if self.timer >= self.down_duration:
                self.kill()



# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # --- wybór grafik zależnie od fazy ---
        if FAZA == 3:
            frames = ["textures/grzyb3.png", "textures/grzyb4.png"]
            self.animation_speed = 0.05   # wolniejsza animacja
        else:
            frames = ["textures/grzyb1.png", "textures/grzyb2.png"]
            self.animation_speed = 0.1

        self.frames = [pygame.transform.scale(pygame.image.load(f).convert_alpha(), (TILE, TILE)) for f in frames]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # parametry ruchu
        self.direction = -1
        self.vel_y = 0
        self.gravity = 0.6

        # animacja
        self.animation_timer = 0

    def update(self, tiles):
        # --- kaszel w fazie 3 i 4 ---
        if FAZA == 3:
            if random.randint(1, 10000) == 1:  # rzadko
                pygame.mixer.Sound(random.choice(["sounds/cough1.mp3", "sounds/cough2.mp3"])).play()
        elif FAZA == 4:
            if random.randint(1, 2500) == 1:   # częściej
                pygame.mixer.Sound(random.choice(["sounds/cough1.mp3", "sounds/cough2.mp3"])).play()

        # --- ruch poziomy zależny od ENEMY_SPEED ---
        self.rect.x += self.direction * ENEMY_SPEED
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.direction > 0:
                    self.rect.right = t.rect.left
                    self.direction = -1
                else:
                    self.rect.left = t.rect.right
                    self.direction = 1

        # --- grawitacja ---
        self.vel_y += self.gravity
        if self.vel_y > 8:
            self.vel_y = 8
        self.rect.y += self.vel_y

        # --- kolizja pionowa ---
        for t in tiles:
            if self.rect.colliderect(t.rect):
                if self.vel_y > 0:
                    self.rect.bottom = t.rect.top
                    self.vel_y = 0

        # --- animacja chodzenia ---
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def stomp(self):
        # wywołane gdy Mario skacze na Goombę
        goomba_sound.play()
        self.kill()  # od razu usuń przeciwnika

    def draw(self, surf, cam):
        r = cam.apply(self.rect)
        surf.blit(self.image, r)

# Build world
def game_over():
    # czarny ekran
    screen.fill((0, 0, 0))

    # napis GAME OVER na środku
    text_surface = font2.render("GAME OVER", True, (200, 200, 200))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # odtwórz dźwięk
    game_over_sound.play()

    # poczekaj aż skończy się dźwięk + 3 sekundy
    duration = int(game_over_sound.get_length() * 1000) + 3000
    pygame.time.delay(duration)

    # zamknij grę
    pygame.quit()
    sys.exit()











def draw_fog(screen):
    if FOG:  # tylko jeśli mgła jest włączona
        fog_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        fog_surface.fill((100, 100, 100, 128 * FOG))  # szary z alfa 128 ≈ 50%
        screen.blit(fog_surface, (0, 0))



def next_phase():  
    global PHASE, FAZA, FOG
    FAZA += 1
    if FAZA > 2:
        FOG += 0.6
    PHASE = "faza" + str(FAZA)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(f"music/{PHASE}.mp3")
    pygame.mixer.music.play(-1)   # -1 oznacza nieskończoną pętlę
    pygame.mixer.music.set_volume(0.5)  # głośność 0.0–1.0
   
    print(PHASE)

def reset_level():
    global tiles, lucky_blocks, enemies, player, rewards, FIRST_REWARD, start_time, timer_value

    tiles = []
    lucky_blocks = []
    enemies = []
    FIRST_REWARD = True

    pygame.mixer.music.stop()
    pygame.mixer.music.load(f"music/{PHASE}.mp3")
    pygame.mixer.music.play(-1)   # -1 oznacza nieskończoną pętlę
    pygame.mixer.music.set_volume(0.5)  # głośność 0.0–1.0

    for r, row in enumerate(LEVEL_MAP):
        for c, ch in enumerate(row):
            x, y = c * TILE, r * TILE
            if ch == '#':
                tiles.append(Tile(x, y, 'ground'))
            elif ch == 'B':
                tiles.append(Tile(x, y, 'brick'))
            elif ch == '|':
                tiles.append(Tile(x, y, 'pole'))
            elif ch == '!':
                tiles.append(Tile(x, y, 'flag1'))
            elif ch == '@':
                tiles.append(Tile(x, y, 'flag2'))
            elif ch == '`':
                tiles.append(Tile(x, y, 'flag3'))
            elif ch == '~':
                tiles.append(Tile(x, y, 'flag_end'))
            elif ch == 'Q':
                tiles.append(Tile(x, y, 'plate'))    
            elif ch == '?':
                lucky_blocks.append(LuckyBlock(x, y))
            elif ch == 'E':
                enemies.append(Enemy(x + 6, y + 6))
            elif ch == 'P':
                player = Player(x, y)
            elif ch == '+':
                tiles.append(Tile(x, y, 'piperightend'))
            elif ch == '-':
                tiles.append(Tile(x, y, 'pipeleftend'))
            elif ch == ']':
                tiles.append(Tile(x, y, 'piperight'))
            elif ch == '[':
                tiles.append(Tile(x, y, 'pipeleft'))

    if player is None:
        player = Player(TILE, TILE)

    # reset czasu i punktów
    start_time = pygame.time.get_ticks()
    timer_value = 400
    player.score = 0
    camera.reset()
    rewards.empty()


tiles = []
enemies = []
player = None
lucky_blocks = []



for r, row in enumerate(LEVEL_MAP):
    for c, ch in enumerate(row):
        x, y = c * TILE, r * TILE
        if ch == '#':
            tiles.append(Tile(x, y, 'ground'))
        elif ch == 'B':
            tiles.append(Tile(x, y, 'brick'))
        elif ch == '|':
            tiles.append(Tile(x, y, 'pole'))
        elif ch == '!':
            tiles.append(Tile(x, y, 'flag1'))
        elif ch == '@':
            tiles.append(Tile(x, y, 'flag2'))
        elif ch == '`':
            tiles.append(Tile(x, y, 'flag3'))
        elif ch == '~':
            tiles.append(Tile(x, y, 'flag_end'))
        elif ch == 'Q':
            tiles.append(Tile(x, y, 'plate'))    
        elif ch == '?':
            lucky_blocks.append(LuckyBlock(x, y))
        elif ch == 'E':
            enemies.append(Enemy(x + 6, y + 6))
        elif ch == 'P':
            player = Player(x, y)
        elif ch == '+':
            tiles.append(Tile(x, y, 'piperightend'))
        elif ch == '-':
            tiles.append(Tile(x, y, 'pipeleftend'))
        elif ch == ']':
            tiles.append(Tile(x, y, 'piperight'))
        elif ch == '[':
            tiles.append(Tile(x, y, 'pipeleft'))

if player is None:
    player = Player(TILE, TILE)

world_width = len(LEVEL_MAP[0]) * TILE
world_height = len(LEVEL_MAP) * TILE
camera = Camera(world_width, world_height)

# Main loop
running = True
while running:

    if GAME_OVER_SCREEN:
        screen.fill((0, 0, 0))
        elapsed = pygame.time.get_ticks() - GAME_OVER_START

        if elapsed < 4500:  # 0–3 sekundy
            text = minifont.render("TO TYLKO KWESTIA CZASU ZANIM TO STANIE SIE Z NAMI", True, (255, 255, 255))
        elif elapsed < 9000:  # 3–6 sekund
            text = font.render("ZANIECZYSZCZENIE TO NIE PRZELEWKI", True, (255, 255, 255))
        else:  # po 6 sekundach
            text = font.render("ZACZNIJ DZIAŁAĆ", True, (255, 255, 255))

        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)
        pygame.display.flip()
        continue

    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player.jump_cut()

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.apply_gravity()
    player.update(tiles, enemies, lucky_blocks)
    player.animate(keys)
    camera.update(player.rect)


    # aktualizacja nagród


    # HUD timer
    elapsed_ms = pygame.time.get_ticks() - start_time
    timer_value = 400 - elapsed_ms // 1000
    if elapsed_ms // 1000 == 400 or player.rect.y > HEIGHT + 200:
        player.die()
    # --- RYSOWANIE ---
    screen.fill(COLOR_BG)
    screen.blit(background_img, (-camera.offset.x, 0))

    for t in tiles:
        t.draw(screen, camera)
    for reward in rewards:
        screen.blit(reward.image, camera.apply(reward.rect))
    for lb in lucky_blocks:
        lb.update(dt, player)
        lb.draw(screen, camera)
    for e in enemies:
        e.update(tiles)
        e.draw(screen, camera)
    rewards.update(tiles, player, lucky_blocks)
    


    player.draw(screen, camera)
    draw_hud(screen, player)
    if player.rect.x > 9400:
        reset_level()
        next_phase()
        
        load_background()
    draw_fog(screen)
    pygame.display.flip()


pygame.quit()
