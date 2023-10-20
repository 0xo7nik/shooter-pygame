from pygame import *
from random import randint


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet1)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global loss
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            loss = loss + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)

win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_astr = 'asteroid.png'

score = 0
loss = 0
goal = 10
max_lost = 3

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_back), (700, 500))
ship: Player

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width  - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

clock = time.Clock()
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(loss), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.reset()

        ship.update()
        monsters.update()
        bullets.update()

        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 8, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or loss >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        clock.tick(15)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    time.delay(30)        
