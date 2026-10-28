import pygame
SCREENRECT = pygame.Rect(0, 0, 700, 500)
class Sprite(pygame.sprite.Sprite):

    def __init__(self, file_name, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(file_name), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

class Player(Sprite):
    def __init__(self, speed=10, x=35, y=439):
        super().__init__("hero.png", x , y, 50, 50)
        self.speed = speed
    def update(self, walls):
        x_before, y_before = self.rect.x, self.rect.y  # а где мы стоим до движения?
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a] and SCREENRECT.left < self.rect.left:
            self.rect.x -=self.speed
        if key_pressed[pygame.K_d] and SCREENRECT.right > self.rect.right:
            self.rect.x += self.speed
        if key_pressed[pygame.K_s] and SCREENRECT.bottom > self.rect.bottom:
            self.rect.y += self.speed
        if key_pressed[pygame.K_w] and SCREENRECT.top < self.rect.top:
            self.rect.y -= self.speed
        if pygame.sprite.spritecollide(self, walls, False):  # если после движения мы столкнулись со стеной
            self.rect.x, self.rect.y = x_before, y_before  # возвращаемся в точку до движения

class Monster(Sprite):
    def __init__(self, x, y, x_left, x_right, speed=5, direction='left'):
        super().__init__("cyborg.png", x ,y ,50, 50)
        self.speed = speed
        self.direction = direction
        self.x_left = min(x_left, x_right)
        self.x_right = max(x_left, x_right)
    def update(self, *args):
        if self.rect.x <= self.x_left:
            self.direction = 'right'
        elif self.rect.right > self.x_right:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image.fill((250, 153, 7))

        
class Win(Sprite):
    def __init__(self, x=582, y=433):
        super().__init__("treasure.png", x, y, 60, 60)
    
def main ():
    pygame.init()
    FPS = 60
    screen = pygame.display.set_mode(SCREENRECT.size)
    pygame.mixer.init()
    pygame.mixer.music.load('jungles.ogg')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    pygame.font.init()
    main_font = pygame.font.SysFont('candara', 60)
    you_win = main_font.render('YOU WON', True, (0, 0, 0), (255, 255, 255))
    you_lose = main_font.render("GAME OVER", True, (0, 0, 0), (255, 255, 255))
    clock = pygame.time.Clock()  # счетчик кадров в секунду
    screen_rect = screen.get_rect()  # прямоугольник экрана
    fon = pygame.transform.scale(pygame.image.load('background.jpg'), (SCREENRECT.width, SCREENRECT.height))
    player = Player()
    monster = Monster(590, 300, 500, SCREENRECT.right)
    win = Win()
    all_sprites = pygame.sprite.Group(player, monster, win)
    walls = pygame.sprite.Group()
    walls.add(Wall(7, 4,5, 500),Wall(7, 4,700, 5),Wall(693, 6,5, 500), Wall(14, 488,700, 5), Wall(102, 6,5, 100),Wall(252, 105,5, 100),Wall(255, 201,200, 5), Wall(449, 63,5, 150), Wall(384, 63,135, 5), Wall(138, 203,5, 500), Wall(455, 290,5, 500))
    game = True
    finish = False
    while game:
        for event in pygame.event.get():  # а что произошло?
            if event.type == pygame.QUIT:
                game = False

            elif event.type == pygame.KEYDOWN:  # нажали на какую-то клавишу
                if event.key == pygame.K_SPACE:
                    print('Прыжок')
            elif event.type == pygame.KEYUP:  # отпустили какую-то клавишу
                ...
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # где-то кликнули мышкой (левая кнопка)
                x, y = event.pos  # точка где кликнули
                print(x, y)
        if not finish:
            screen.fill((0, 0, 250))
            screen.blit(fon, (0, 0))
            walls.draw(screen)
            all_sprites.update(walls)
            all_sprites.draw(screen)
            if pygame.sprite.collide_rect(player, win):
                screen.blit(you_win, (174, 241))
                finish = True
            elif pygame.sprite.collide_rect(player, monster):
                screen.blit(you_lose, (174, 241))
                finish = True
        
        pygame.display.flip()  # pygame.display.update()
        clock.tick(FPS)  # обновляемся не чаще чем FPS
if __name__ == '__main__':
    main()
    pygame.quit()