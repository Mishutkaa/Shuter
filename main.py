from msilib.schema import SelfReg
from pygame import *
from random import randint
if_boss = False
# фонова музика

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('laser_fire.ogg')
death_sound = mixer.Sound("deathsound.ogg")
# шрифти і написи
font.init()
score_text = font.SysFont("Arial", 30)
score_text2 = font.SysFont("Arial", 30)
score = 0
score2 = 0
lost_text = font.SysFont("Arial", 30)
lost = 0
lose_text = font.SysFont("Arial", 30)
win_text = font.SysFont("Arial", 30)
suma_score = font.SysFont("Arial", 30)


win_width = 700
win_height = 500
display.set_caption("ufo")
window = display.set_mode((win_width, win_height))

background = transform.scale(
    image.load("galaxy.jpg"), 
    (win_width, win_height)
)



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
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
        bullet = Bullet('Blaster_bullet.png', self.rect.centerx, self.rect.top, 10, 60, -15)
        bullets.add(bullet)


class Player2(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        

    def fire2(self):
        bullet2 = Bullet('Blaster_bullet.png', self.rect.centerx, self.rect.top, 10, 60, -15)
        bullets2.add(bullet2)









# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class asteroidi(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0



# клас спрайта-кулі   
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()
        if sprite.groupcollide(asteroids, bullets, False, True):
            self.kill()
        if sprite.groupcollide(asteroids, bullets2, False, True):
            self.kill()
        
        
ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)
ship2 = Player2("rocket.png", 600, win_height - 100, 80, 100, 10)
bullets = sprite.Group()
bullets2 = sprite.Group()
monsters = sprite.Group()
asteroids= sprite.Group()
for i in range(1, 2):
    asteroid = asteroidi("asteroid"+ str(randint(1, 3)) +".png", randint(80, win_width - 80), -40, 80, 80, 6)
    asteroids.add(asteroid)
for i in range(1, 7):
    monster = Enemy("ufo" + str(randint(1, 6)) + ".png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

run = True
game_over = False
is_win = False
color_1 = ((255, 255, 255))
color_2 = ((255, 255, 255))
while run:

    window.blit(background, (0, 0))
    text1 = score_text.render("1 Рахунок: " + str(score), 1, (color_1))
    text3 = score_text.render("2 Рахунок: " + str(score2), 1, (color_1))
    window.blit(text1, (10, 20))
    text2 = lost_text.render("Життя: 10/" + str(10 - lost), 1, (color_2))
    window.blit(text2, (260, 20))
    window.blit(text3, (540, 20))

    if lost >= 7:
        color_2 = ((255, 0, 0))
        text2 = lost_text.render("Життя: 10/" + str(10 - lost), 1, (color_2))
        text2.blit(text2, (10, 20))



    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if game_over == False:
                if e.key == K_w:
                    fire_sound.play()
                    ship.fire()
                if e.key == K_UP:
                    fire_sound.play()
                    ship2.fire2()

    if game_over == False:






        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy("ufo" + str(randint(1, 6)) + ".png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroid = asteroidi("asteroid"+ str(randint(1, 3)) +".png", randint(80, win_width - 80), -40, 80, 80, 6)
            monsters.add(monster)
        collides2 = sprite.groupcollide(monsters, bullets2, True, True)
        for b in collides2:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score2 = score2 + 1
            print(score2)
            monster = Enemy("ufo" + str(randint(1, 6)) + ".png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroid = asteroidi("asteroid"+ str(randint(1, 3)) +".png", randint(80, win_width - 80), -40, 80, 80, 6)
            monsters.add(monster)
        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        if sprite.spritecollide(ship, monsters, True) or lost == 10:  
            death_sound.play()
            if lost == 10:
                game_over = 10
            else:
                lost += 2
        if sprite.spritecollide(ship, asteroids, True):
            death_sound.play()
            game_over = True
        if sprite.spritecollide(ship2, monsters, True) or lost == 10:  
            death_sound.play()
            if lost == 10:
                game_over = True
            else:
                lost += 2
        if sprite.spritecollide(ship2, asteroids, True):
            death_sound.play()
            game_over = True



        if score >= 50 or score2 >= 50:
            game_over = True
            is_win = True

        # рухи спрайтів
        ship.update()
        ship2.update()
        monsters.update()
        bullets.update()
        bullets2.update()
        asteroids.update()

    else:
        if is_win == True:
            text4 = win_text.render("Ви перемогли", 1, (255, 255, 255))
            all_suma = score + score2
            text5 = suma_score.render("Разом: " + str(all_suma), 1, (225, 255, 255))
            window.blit(text4, (200, 200))
            window.blit(text5, (200, 300))
        else:
            text3 = lose_text.render("Ви програли", 1, (255, 255, 255))
            all_suma = score + score2
            text5 = suma_score.render("Разом: " + str(all_suma), 1, (225, 255, 255))
            window.blit(text3, (200, 200))
            window.blit(text5, (200, 240))

    # оновлюємо їх у новому місці при кожній ітерації циклу
    
    ship.reset()
    ship2.reset()
    monsters.draw(window)
    bullets.draw(window)
    bullets2.draw(window)
    asteroids.draw(window)
    display.update()
    time.delay(60)