import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_pos_x,900))
    screen.blit(floor_surface, (floor_pos_x + 576,900))

def create_pipe():

    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((576, 1024))
running = True
clock = pygame.time.Clock()
game_font = pygame.font.Font('venv/lib/python3.8/site-packages/pygame/04B_19__.TTF', 40)

#Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

MAX_FPS = 120
background_surface = pygame.transform.scale2x(pygame.image.load('sprites/background-day.png').convert())

floor_surface = pygame.transform.scale2x(pygame.image.load('sprites/base.png').convert())
floor_pos_x = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('sprites/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('sprites/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('sprites/yellowbird-downflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
# bird_surface = pygame.image.load('sprites/yellowbird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100, 512))

pipe_surface = pygame.transform.scale2x(pygame.image.load('sprites/pipe-green.png'))
pipes = []
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('sprites/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

# flap_sound = pygame.mixer.Sound('audio/wing.ogg')
# death_sound = pygame.mixer.Sound('audio/hit.wav')
# score_sound = pygame.mixer.Sound('audio/point.wav')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                bird_movement = 0
                bird_movement -= 10

        if event.type == pygame.KEYDOWN and game_active == False:
            game_active = True
            pipes.clear()
            bird_rect.center = (100, 512)
            #bird_movement = 0
            score = 0

        if event.type == spawn_pipe:
            pipes.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()


    screen.blit(background_surface, (0,0))

    if game_active:
        #BIRD
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipes)

        #PIPE
        pipes = move_pipes(pipes)
        draw_pipes(pipes)
        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    #FLOOR
    floor_pos_x -= 1
    draw_floor()
    if floor_pos_x <= -576:
        floor_pos_x = 0

    pygame.display.update()
    clock.tick(MAX_FPS)
