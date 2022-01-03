import pygame
import os
import sys


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

sound1 = pygame.mixer.Sound("music_start.mp3")
sound2 = pygame.mixer.Sound("music_crash.mp3")
sound3 = pygame.mixer.Sound("music_win.mp3")
sound4 = pygame.mixer.Sound("music_game_over.mp3")

screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit


def end_screen():
    fon = pygame.transform.scale(load_image('fon_end.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    sound4.play(0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                sound4.stop()
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    fon = pygame.transform.scale(load_image('fon_win.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    sound3.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                sound3.stop()
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

dx = 5
dy = -5
player = Player((512, 637))
ball = Ball((620, 600))
all_sprites.add(player)
all_sprites.add(ball)
running = True

while running:
    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if ball.rect.x > 1240:
        dx = -dx
    if ball.rect.y < 0:
        dy = -dy
    if ball.rect.x < 0:
        dx = -dx
    if ball.rect.y > 680:
        end_screen()
    if pygame.sprite.collide_mask(ball, player) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, player)

    for i in all_sprites:
        if pygame.sprite.collide_mask(ball, i) and i != ball and i != player:
            all_sprites.remove(i)
            sound2.play()
            dx, dy = detect_collision(dx, dy, ball, i)
            if len(all_sprites) < 5:
                win_screen()

    ball.rect = ball.rect.move(dx, dy)
    all_sprites.draw(screen)
    all_sprites.update()
    if len(all_sprites) < 5:
        win_screen()
    pygame.display.flip()
    if len(all_sprites) < 5:
        win_screen()
    clock.tick(50)
pygame.quit()





