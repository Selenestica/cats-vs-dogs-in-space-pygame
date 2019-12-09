import pygame
pygame.init()

screen_width = 640
screen_height = 380
win = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("First Game")

walk_right = [pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png'), pygame.image.load('SPACECATIII.png')]
walk_left = [pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png'), pygame.image.load('SPACECATII (1).png')]
bg = pygame.image.load('space-planet-bg-1.png')

walk_right_dog = [pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png'), pygame.image.load('SPACEDOGGOII (1).png')]
walk_left_dog = [pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png'), pygame.image.load('SPACEDOGGO.png')]

clock = pygame.time.Clock()

#cat character
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not(self.standing):
            if self.left:
                win.blit(walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walk_right[0], (self.x, self.y))
            else:
                win.blit(walk_left[0], (self.x, self.y))

#dog character
class dog(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not(self.standing):
            if self.left:
                win.blit(walk_left_dog[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right_dog[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walk_right_dog[0], (self.x, self.y))
            else:
                win.blit(walk_left_dog[0], (self.x, self.y))

#cat projectile
class projectile(object): 
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 12 * facing 
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

#dog projectile
class barrage(object): 
    def __init__(self, x, y, radius, color, dog_facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dog_facing = dog_facing
        self.velocity = 12 * dog_facing 
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
#game window
def redraw_game_window():
    win.blit(bg, (0, 0))
    man.draw(win)
    doggo.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    for missile in missiles:
        missile.draw(win)
    pygame.display.update()


#mainloop
man = player(0, 300, 64, 48)
doggo = dog(590, 300, 64, 48)
bullets = []
missiles = []
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 700 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    for missile in missiles:
        if missile.x < 700 and missile.x > 0:
            missile.x += missile.velocity
        else:
            missiles.pop(missiles.index(missile))

    keys = pygame.key.get_pressed()

#kitty code
    if keys[pygame.K_RCTRL]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (255, 255, 0), facing))

    if keys[pygame.K_LEFT] and man.x > man.velocity:
        man.x -= man.velocity + 4
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.width:
        man.x += man.velocity + 4
        man.right = True 
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walk_count = 0

    if not (man.is_jump):
        if keys[pygame.K_UP] and man.y > man.velocity:
            man.y -= man.velocity + 4
        if keys[pygame.K_DOWN] and man.y < screen_height - man.height:
           man.y += man.velocity + 4
        if keys[pygame.K_SPACE]:
            man.is_jump = True 
            man.right = False
            man.left = False
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            neg = 1
            if man.jump_count < 0:
                neg = -1
            man.y -= (man.jump_count ** 2) * 0.5 * neg
            man.jump_count -= 1
        else:
            man.is_jump = False
            man.jump_count = 10 

#doggo code
    if keys[pygame.K_LSHIFT]:
        if doggo.left:
            dog_facing = -1
        else:
            dog_facing = 1
        if len(missiles) < 5:
            missiles.append(barrage(round(doggo.x + doggo.width // 2), round(doggo.y + doggo.height // 2), 6, (255, 0, 0), dog_facing))

    if keys[pygame.K_a] and doggo.x > doggo.velocity:
        doggo.x -= doggo.velocity + 4
        doggo.left = True
        doggo.right = False
        doggo.standing = False
    elif keys[pygame.K_d] and doggo.x < screen_width - doggo.width:
        doggo.x += doggo.velocity + 4
        doggo.right = True 
        doggo.left = False
        doggo.standing = False
    else:
        doggo.standing = True
        doggo.walk_count = 0

    if not (doggo.is_jump):
        if keys[pygame.K_w] and doggo.y > doggo.velocity:
            doggo.y -= doggo.velocity + 4
        if keys[pygame.K_s] and doggo.y < screen_height - doggo.height:
           doggo.y += doggo.velocity + 4
        if keys[pygame.K_j]:
            doggo.is_jump = True 
            doggo.right = False
            doggo.left = False
            doggo.walk_count = 0
    else:
        if doggo.jump_count >= -10:
            neg = 1
            if doggo.jump_count < 0:
                neg = -1
            doggo.y -= (doggo.jump_count ** 2) * 0.5 * neg
            doggo.jump_count -= 1
        else:
            doggo.is_jump = False
            doggo.jump_count = 10 

    redraw_game_window()

pygame.quit()


















