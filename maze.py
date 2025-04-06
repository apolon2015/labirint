import pygame as pg 
pg.mixer.init()

class GameSprite(pg.sprite.Sprite):
    def __init__(self, filename, w,h,x,y,speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, ( self.rect.x,  self.rect.y))

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <=  400:
            self.direction = 'right'
        if self.rect.x >= w - 100:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Player(GameSprite):
    def update(self):
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_UP] and self.rect.y > 0:
            self.rect.y -= 10
        if keys_pressed[pg.K_DOWN] and self.rect.y < h - w/10:
            self.rect.y += 10
        if keys_pressed[pg.K_RIGHT] and self.rect.x < w - w/10 :
            self.rect.x += 10
        if keys_pressed[pg.K_LEFT] and self.rect.x > 0:
            self.rect.x -= 10

class Wall(pg.sprite.Sprite):
    def __init__(self, color, w, h, x, y):
        super().__init__()
        self.color = color
        self.w = w
        self.h = h
        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


w = 1000
h = int(w / 7 * 5)
win = pg.display.set_mode((w,h))
pg.display.set_caption('Лабиринт')

image = pg.image.load('background.jpg')
bg = pg.transform.scale(image,(w, h))

icon = pg.image.load('hero.png')
pg.display.set_icon(icon)

hero = Player('hero.png', w/10,w/10, 5, h - (w/10) , 10)
gold = GameSprite('treasure.png', w/10,w/10, w - w/10, h - (w/10), 0)
cyborg = Enemy('cyborg.png', w/10,w/10, w/3*2, h - w/5, 10)
cyborg.direction = 'left'
wall1 = Wall((34,77, 46), 25, h-150, 150, 150)
wall2 = Wall((34,77, 46), w/2.5, 25, 175, 150)
wall3 = Wall((34,77, 46), 25, h-150, w/2+75, 150)
wall4 = Wall((34,77, 46), w/4, 25, w-w/4, h/2+100)


finish = False
run = True
Clock = pg.time.Clock()

pg.mixer.music.load('jungles.ogg')
pg.mixer.music.play()
loser_sound = pg.mixer.Sound('kick.ogg')
winner_sound = pg.mixer.Sound('money.ogg')
clock = pg.time.Clock()
while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
    if not finish:
        win.blit(bg, (0,0))
        hero.reset()
        cyborg.reset()
        gold.reset()
        cyborg.update()
        hero.update()
        wall1.reset()
        wall2.reset()
        wall3.reset()
        wall4.reset()
        if pg.sprite.collide_rect(hero, cyborg):
            loser_sound.play()
            finish = True
            lose = True
        if pg.sprite.collide_rect(hero, wall1):
            loser_sound.play()
            finish = True
            lose = True
        if pg.sprite.collide_rect(hero, wall2):
            loser_sound.play()
            finish = True
            lose = True
        if pg.sprite.collide_rect(hero, wall3):
            loser_sound.play()
            finish = True
            lose = True
        if pg.sprite.collide_rect(hero, wall4):
            winner_sound.play()
            finish = True
            lose = True
        if pg.sprite.collide_rect(hero, gold):
            winner_sound.play()
            finish = True
            lose = False
    else:
        win.blit(bg, (0,0))
        hero.reset()
        cyborg.reset()
        gold.reset()
        wall1.reset()
        wall2.reset()
        wall3.reset()
        wall4.reset()
        if not lose:
            res = GameSprite('youwin.png', w/3, h/3, w/2-w/4, h/2-h/6, 0)
        else:
            res = GameSprite('youlose.png', w/2, h/3, w/2-w/4, h/2-h/6, 0)
        res.reset()
    pg.display.update()
    clock.tick(60)
