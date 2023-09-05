import pygame
from random import randint

ocean= [6,5,4,3,2,1,0,-1,-2,-1,0,1,2,3,4]
crate_loop = 0
freq_loop = 0
score = 0
health = 3
game_active = False
start_time = 0

# initializing pygame
pygame.init()
#Set pygame display size + Font
screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("The Game of Games")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Daydream_3/Daydream.ttf', 10)
small_font = pygame.font.Font(None, 25)
label_font = pygame.font.Font('font/Daydream_3/Daydream.ttf', 15)

#Game Over/ New Game Screen
game_over_surf = pygame.image.load('graphics/bg/gameover.png').convert_alpha()
go_rect = game_over_surf.get_rect(midbottom = (400, 325))
greet_text_surf = label_font.render(f'Ahoy Matey', True, 'Black' )
line1_surf = small_font.render(f"'elp us 'scape Tortuga with our plunder", False, 'Black' )
line2_surf = small_font.render(f"Dodge 'em cannonballs with yer d-pad", False, 'Black' )
line3_surf = small_font.render(f"go left or right, ship don't go no faster", False, 'Black' )
line4_surf = small_font.render(f"and we ain't slow'en down for nothin'", False, 'Black' )
line5_surf = small_font.render(f"might as well pick up crates as we go", False, 'Black' )
line6_surf = small_font.render(f"but watch yer flank, fire the cannons", False, 'Black' )
line7_surf = small_font.render(f"press space to keep em creatures at bay", False, 'Black' )
line8_surf = label_font.render(f"Space to start", True, 'Black' )

#Ship image and rect
ship_surf = pygame.image.load('graphics/ship/pship.png').convert_alpha()
ship_rect = ship_surf.get_rect(midbottom = (400, 350))

#crate image and rect
crate_surf = pygame.image.load('graphics/help/crate.png').convert_alpha()
crate_rect = crate_surf.get_rect(midbottom = (randint(25,775), -50))



#enemy images and rects
cb_surf = pygame.image.load('graphics/enemy/cb.png').convert_alpha()
cb_rect = cb_surf.get_rect(midbottom = (400, 500))

kraken_0 = pygame.image.load('graphics/enemy/k1.tiff').convert_alpha()
kraken_1 = pygame.image.load('graphics/enemy/k2.tiff').convert_alpha()
k = [kraken_0, kraken_1]
k_index = 0

k_surf = k[k_index]
k_rect = k_surf.get_rect(midbottom = (700, 375))

rk_surf = pygame.transform.flip(k_surf, True, False)
rk_rect = rk_surf.get_rect(midbottom = (100, 375))

#enemy logic
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1000)

cb_rect_list = []
k_rect_list = []

def cb_movement(cb_list):
    global health
    ct = int((pygame.time.get_ticks() - start_time)/ 1000)
    if cb_list:
        for cb_rect in cb_list:
            cb_rect.y += 4

            screen.blit(cb_surf, cb_rect)
            if ship_rect.colliderect(cb_rect):
                health -= 1
        cb_list = [cb for cb in cb_list if ship_rect.colliderect(cb) == False]
        cb_list = [cb for cb in cb_list if cb.y < 500]
        return cb_list

    else:
        return []

def k_movement(k_list):
    ct = int((pygame.time.get_ticks() - start_time)/ 1000)
    if k_list:
        for k_rect in k_list:
            if k_rect.left > ship_rect.x:
                k_rect.x -= 4
                screen.blit(k_surf, k_rect)
            else:
                k_rect.x += 4
                screen.blit(rk_surf, rk_rect)
            k_list = [k for k in k_list if ship_rect.colliderect(k) == False]

        return k_list
    else:
        return []

# Animation for moving kraken
def k_sway():
    global k_surf, k_index, rk_surf
    k_index += 0.1
    if k_index >= len(k):
        k_index = 0
    k_surf = k[int(k_index)]
    rk_surf = pygame.transform.flip(k_surf, True, False)


# Background images + score and health images 
score_surf = pygame.image.load('graphics/bg/score.png').convert_alpha()
health_text_surf = test_font.render(f'Health', False, 'Black' )
hp_surf = pygame.image.load('graphics/bg/health.png').convert_alpha()
emp_hp_surf = pygame.image.load('graphics/bg/emp_hp.png').convert_alpha()

def scored():
    global score
    score_text_surf = test_font.render(f'Score: {score}', False, 'Black' )
    if ship_rect.colliderect(crate_rect): 
            score += 1
            crate_rect.y = 500
    screen.blit(score_text_surf, (40,25))


bg_1 = pygame.image.load('graphics/bg/bg1.tiff').convert()
bg_2 = pygame.image.load('graphics/bg/bg2.tiff').convert()
bg_3 = pygame.image.load('graphics/bg/bg3.tiff').convert()
bg_4 = pygame.image.load('graphics/bg/bg4.tiff').convert()
bg_5 = pygame.image.load('graphics/bg/bg5.tiff').convert()
bg_index = 0
bg = [bg_1, bg_2, bg_3, bg_4, bg_5]

# Animation for moving sea
def bg_animation():
    global bg_index, bgd
    bg_index += .2
    if int(bg_index) >= len(bg):
        bg_index = 0
    bgd = bg[int(bg_index)]



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            #key checking and player input
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print('fire')
            if event.type == enemy_timer:
                cb_rect_list.append(cb_surf.get_rect(midbottom = (randint(25, 775), randint(-200, -30))))
                if randint(0,2):
                    k_rect_list.append(k_surf.get_rect(midbottom = (randint(1200, 1800), 375)))
                else:
                    k_rect_list.append(rk_surf.get_rect(midbottom = (randint(-1000, -300), 375)))
        else:
            #game start
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    health = 3
                    score = 0
                    start_time = pygame.time.get_ticks()
    user_input = pygame.key.get_pressed()
    if user_input[pygame.K_LEFT] and ship_rect.x >= -25:
        ship_rect.x -= 3
    if user_input[pygame.K_RIGHT] and ship_rect.x <= 725:
                ship_rect.x += 3
    bg_animation()
    screen.blit(bgd,(0,0))
    screen.blit(score_surf,(0,0))
    k_sway()
    scored()
    if game_active == True:
        if health == 3:
            screen.blit(hp_surf, (20,70))
            screen.blit(hp_surf, (65,70))
            screen.blit(hp_surf, (110,70))
        elif health == 2:
            screen.blit(hp_surf, (20,70))
            screen.blit(hp_surf, (65,70))
            screen.blit(emp_hp_surf, (110,70))
        elif health == 1:
            screen.blit(hp_surf, (20,70))
            screen.blit(emp_hp_surf, (65,70))
            screen.blit(emp_hp_surf, (110,70))
        else:
             game_active = False
             cb_rect.y = -50
             crate_rect.y =-50
        screen.blit(ship_surf, ship_rect)
        cb_rect_list = cb_movement(cb_rect_list)
        k_rect_list = k_movement(k_rect_list)
        screen.blit(ship_surf, ship_rect)

        #crate reinitialize and movement logic 
        if crate_rect.y >= 500:
            crate_rect.y = -50
            crate_rect.x = randint(25, 775)
        if crate_loop >= len(ocean):
            crate_loop = 0
        cs = float(((100 + ((ocean[crate_loop]*5)))/100))
        crate_surf = pygame.image.load('graphics/help/crate.png').convert_alpha()
        crate_surf = pygame.transform.smoothscale_by(crate_surf, cs)    
        if freq_loop == 0:
            crate_rect.y += ocean[crate_loop]
            crate_loop += 1
            freq_loop = 6
        else: 
            crate_rect.y += ocean[crate_loop]
            freq_loop -=1
        screen.blit(crate_surf, crate_rect)

        #ship collides with crate
        scored()
    else:
        screen.blit(game_over_surf, go_rect)
        screen.blit(greet_text_surf, (320, 50))
        screen.blit(line1_surf, (250, 75))
        screen.blit(line2_surf, (250, 95))
        screen.blit(line3_surf, (250, 115))
        screen.blit(line4_surf, (250, 135))
        screen.blit(line5_surf, (250, 155))
        screen.blit(line6_surf, (250, 175))
        screen.blit(line7_surf, (250, 195))
        screen.blit(line8_surf, (290, 220))
        screen.blit(k_surf, k_rect)
        screen.blit(rk_surf, rk_rect)
        screen.blit(ship_surf, ship_rect)
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()