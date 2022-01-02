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
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
FPS = 50
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    fon = pygame.transform.scale(load_image('fon_start.jpg'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
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


all_sprites = pygame.sprite.Group()

for i in range(0, 1281, 128):
    all_sprites.add(BlockGreen((i, 0)))
    all_sprites.add(BlockRed((i, 64)))
    all_sprites.add(BlockBlue((i, 128)))


player = Player((512, 637))
ball = Ball((620, 603))
all_sprites.add(ball)
all_sprites.add(player)
running = True

while running:
    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()





