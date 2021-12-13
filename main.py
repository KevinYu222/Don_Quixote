import pygame, sys, random, json

pygame.init()
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 30)

#Game variables
gravity = 0.15
char_movement = 0
game_active = True
score = 0
with open('score_keep.json', 'r') as f:
    high_score = f.read()
game_state = "menu"
background = pygame.image.load('Assets/prison.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT - 150))

base = pygame.image.load('Assets/base.png').convert()
base = pygame.transform.scale(base, (WIDTH, 150))
base_x_pos = 0

don_quixote = pygame.image.load('Assets/Don_Quixote.png')
don_quixote = pygame.transform.flip(pygame.transform.scale(don_quixote, (70, 80)), True, False)
char_rect = don_quixote.get_rect(center = (100, HEIGHT/2))

mirror_surface = pygame.image.load('Assets/mirror.jpg')
mirror_surface = pygame.transform.scale(mirror_surface, (70, 120))
mirror_list = []
SPAWNMIRROR = pygame.USEREVENT
pygame.time.set_timer(SPAWNMIRROR, 1800)
mirror_height = [120, 200, 280]

game_over_surface = pygame.image.load('Assets/windmill.png')
game_over_rect = game_over_surface.get_rect(center = (WIDTH/2, HEIGHT/2))

def draw_base():
    screen.blit(base, (base_x_pos, 500))
    screen.blit(base, (base_x_pos + WIDTH, 500))


def create_mirror():
    random_mirror_pos = random.choice(mirror_height)
    bottom_mirror = mirror_surface.get_rect(midtop = (900, random_mirror_pos))
    top_mirror = mirror_surface.get_rect(midbottom = (900, random_mirror_pos - 300))
    return top_mirror, bottom_mirror


def move_mirrors(mirrors):
    for mirror in mirrors:
        mirror.centerx -= 5
    return mirrors


def draw_mirrors(mirrors):
    for mirror in mirrors:
        screen.blit(mirror_surface, mirror)


def check_collision(mirrors):
    for mirror in mirrors:
        if char_rect.colliderect(mirror):
            return False

    if char_rect.top < -100 or char_rect.bottom >= 600:
        return False
    return True


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f'Score: {str(int(score))}', False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (75, 50))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f'Score: {str(int(score))}', False, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (75, 50))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {str(int(high_score))}', False, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center = (108, 90))
        screen.blit(high_score_surface, high_score_rect)
        
        with open("score_keep.json", "w") as f:
            json.dump(int(high_score), f, indent=4)


def menu_display():
    message_surface = game_font.render(f'Welcome', False, (255, 255, 255))
    message_rect = message_surface.get_rect(center = (WIDTH/2, HEIGHT/2))
    start_surface = game_font.render(f'Press SPACE to Start', False, (255, 255, 255))
    start_rect = message_surface.get_rect(center = (WIDTH/2, HEIGHT/2 + 40))
    screen.blit(message_surface, message_rect)
    screen.blit(start_surface, start_rect)

running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "main_game"
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    char_movement = 0
                    char_movement -= 6
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    mirror_list.clear()
                    char_rect.center = (100, 325)
                    char_movement = 0
                    score = 0

            if event.type == SPAWNMIRROR:
                mirror_list.extend(create_mirror())
    # screen.blit(background, (0, 0))
    if game_state != "menu":
        screen.fill((255, 153, 0))
    else:
        screen.blit(background, (0, 0))
        menu_display()
        

    #Char
    if game_active and game_state != "menu":
        char_movement += gravity
        char_rect.centery += char_movement
        screen.blit(don_quixote, char_rect)
        game_active = check_collision(mirror_list)

        #Mirrors
        mirror_list = move_mirrors(mirror_list)
        draw_mirrors(mirror_list)
        score += 0.01
        score_display("main_game")
    else:
        if game_state != "menu":
            screen.blit(game_over_surface, game_over_rect)
            if int(score) >= int(high_score):
                high_score = score
            score_display("game_over")


    base_x_pos -= 1
    draw_base()
    if base_x_pos <= - 500:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(60)
