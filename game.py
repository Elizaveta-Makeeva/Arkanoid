import pygame
import os
import sys
import time


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
pygame.mixer.init()
pygame.font.init()

sound1 = pygame.mixer.Sound("music_start.mp3")
sound2 = pygame.mixer.Sound("music_crash.mp3")
sound3 = pygame.mixer.Sound("music_win.mp3")
sound4 = pygame.mixer.Sound("music_game_over.mp3")
sound5 = pygame.mixer.Sound("music_lives.mp3")
sound6 = pygame.mixer.Sound("music_hit.mp3")

screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit


def end_screen(delta):
    fon = pygame.transform.scale(load_image('fon_end.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    sound4.play(0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                sound4.stop()

        font = pygame.font.Font(None, 40)
        intro_text1 = f"Score: {str(score)}"
        intro_text2 = f"Time: {str(delta)}"
        text1 = font.render(intro_text1, False, 'white')
        textpos1 = (630, 600)
        screen.blit(text1, textpos1)
        text2 = font.render(intro_text2, False, 'white')
        textpos2 = (630, 650)
        screen.blit(text2, textpos2)
        pygame.display.flip()
        clock.tick(FPS)


def win_screen(delta):
    fon = pygame.transform.scale(load_image('fon_win.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    sound3.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                sound3.stop()

        font = pygame.font.Font(None, 40)
        intro_text1 = f"Score: {str(score)}"
        intro_text2 = f"Lives: {str(lives)}"
        intro_text3 = f"Time: {str(delta)}"
        text1 = font.render(intro_text1, False, 'white')
        text2 = font.render(intro_text2, False, 'white')
        text3 = font.render(intro_text3, False, 'white')
        textpos1 = (540, 500)
        textpos2 = (540, 550)
        textpos3 = (540, 600)
        screen.blit(text1, textpos1)
        screen.blit(text2, textpos2)
        screen.blit(text3, textpos3)

        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    fon = pygame.transform.scale(load_image('fon_start.jpg'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                sound1.stop()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                sound1.stop()
                return

        sound1.play(-1)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

images = {
    'block_red': load_image('block_red.png'),
    'block_green': load_image('block_green.png'),
    'block_blue': load_image('block_blue.png'),
    'ball': load_image('ball.png')}

player_image = load_image('player.png')


class Fon(pygame.sprite.Sprite):
    image = load_image("fon.jpg", color_key=-1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Fon.image
        self.rect = self.image.get_rect()
        self.rect.bottom = height


class Player(pygame.sprite.Sprite):
    image = load_image("player.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.rect.right < 1280:
            self.rect.left += 10
        elif key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= 10


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class BlockGreen(pygame.sprite.Sprite):
    image = load_image("block_green.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = BlockGreen.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class BlockRed(pygame.sprite.Sprite):
    image = load_image("block_red.png", color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = BlockRed.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class BlockBlue(pygame.sprite.Sprite):
    image = load_image('block_blue.png', color_key=-1)

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = BlockBlue.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def detect_collision(dx, dy, ball, x):
    if dx > 0:
        delta_x = ball.rect.right - x.rect.left
    else:
        delta_x = x.rect.right - ball.rect.left
    if dy > 0:
        delta_y = ball.rect.bottom - x.rect.top
    else:
        delta_y = x.rect.bottom - ball.rect.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


all_sprites = pygame.sprite.Group()

for i in range(0, 1281, 128):
    all_sprites.add(BlockGreen((i, 0)))
    all_sprites.add(BlockRed((i, 64)))
    all_sprites.add(BlockBlue((i, 128)))

dx = 6
dy = -6
score = 0
lives = 3
t_start = time.time()
player = Player((512, 637))
ball = Ball((620, 600))
all_sprites.add(player)
all_sprites.add(ball)
running = True


while running:
    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    text_coord = 50
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, (244, 164, 96), (1110, 600, 150, 100))
    font = pygame.font.Font(None, 40)
    intro_text1 = f"Score: {str(score)}"
    intro_text2 = f"Lives: {str(lives)}"
    text1 = font.render(intro_text1, True, 'black')
    text2 = font.render(intro_text2, True, 'black')
    textpos1 = (1120, 610)
    textpos2 = (1120, 650)
    screen.blit(text1, textpos1)
    screen.blit(text2, textpos2)

    pygame.draw.rect(screen, (244, 164, 96), (20, 600, 150, 100))
    font = pygame.font.Font(None, 50)
    t_now = time.time()
    delta = t_now - t_start
    delta = '{:>9.3f}'.format(delta)
    text = font.render(delta, True, 'black')
    textpos = (20, 638)
    screen.blit(text, textpos)

    if ball.rect.x > 1240:
        dx = -dx
    if ball.rect.y < 0:
        dy = -dy
    if ball.rect.x < 0:
        dx = -dx
    if ball.rect.y > 680 and lives > 0:
        lives -= 1
        sound5.play(0)
        dy = -dy
    if lives == 0:
        end_screen(delta)

    if pygame.sprite.collide_mask(ball, player) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, player)
        sound6.play(0)

    for i in all_sprites:
        if pygame.sprite.collide_mask(ball, i) and i != ball and i != player:
            all_sprites.remove(i)
            sound2.play()
            score += 5
            dx, dy = detect_collision(dx, dy, ball, i)
            if len(all_sprites) < 5:
                win_screen(delta)

    if score >= 50 and score < 100:
        if dx > 0 and dy > 0:
            dx = 7
            dy = 7
        elif dx > 0 and dy < 0:
            dx = 7
            dy = -7
        elif dx < 0 and dy > 0:
            dx = -7
            dy = 7
        elif dx < 0 and dy < 0:
            dx = -7
            dy = -7

    if score >= 100 and score < 125:
        if dx > 0 and dy > 0:
            dx = 8
            dy = 8
        elif dx > 0 and dy < 0:
            dx = 8
            dy = -8
        elif dx < 0 and dy > 0:
            dx = -8
            dy = 8
        elif dx < 0 and dy < 0:
            dx = -8
            dy = -8

    if score >= 125:
        if dx > 0 and dy > 0:
            dx = 9
            dy = 9
        elif dx > 0 and dy < 0:
            dx = 9
            dy = -9
        elif dx < 0 and dy > 0:
            dx = -9
            dy = 9
        elif dx < 0 and dy < 0:
            dx = -9
            dy = -9

    ball.rect = ball.rect.move(dx, dy)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()





