import pygame
import random

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

BLACK = ("#fafafa")
WHITE = ("#ababab")

player_size = 50
player_pos = [screen_width // 2, screen_height - player_size]
player_speed = 10

enemy_size = 50
enemies = []
enemy_speed = 1
score = 0
score_for_speed_increase = 1000

missile_size = [20, 20]
missiles = []
missile_speed = 10

enemy_missile_size = [20, 20]
enemy_missiles = []

player_image = pygame.transform.scale(pygame.image.load('player.png'), (player_size, player_size))
enemy_image = pygame.transform.scale(pygame.image.load('enemy.png'), (enemy_size, enemy_size))
missile_image = pygame.transform.scale(pygame.image.load('bullet.png'), (missile_size[0], missile_size[1]))

font = pygame.font.Font(None, 36)

def draw_text(text, color, position):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def drop_enemies():
    delay = random.randint(1, 5)
    if len(enemies) < 10 and random.randint(1, delay) == 1:
        x_pos = random.randint(0, screen_width - enemy_size)
        y_pos = 0
        enemies.append([x_pos, y_pos])

def update_enemy_positions():
    global score, enemy_speed
    for idx, enemy_pos in enumerate(enemies):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += enemy_speed
            if (
                player_pos[1] < enemy_pos[1] + enemy_size
                and player_pos[0] < enemy_pos[0] + enemy_size
                and player_pos[0] + player_size > enemy_pos[0]
            ):
                return True
            if random.randint(1, 100) == 1:
                enemy_missiles.append([enemy_pos[0] + enemy_size // 2, enemy_pos[1] + enemy_size // 2])

        else:
            enemies.pop(idx)
            score += 10
            if score % score_for_speed_increase == 0:
                enemy_speed += 1

def move_missiles():
    for missile in missiles:
        missile[1] -= missile_speed
        if missile[1] < 0:
            missiles.remove(missile)

def move_enemy_missiles():
    for missile in enemy_missiles:
        missile[1] += missile_speed
        if missile[1] > screen_height:
            enemy_missiles.remove(missile)

def collision_check():
    global score, game_over
    for enemy in enemies[:]:
        for missile in missiles[:]:
            if (
                missile[0] >= enemy[0]
                and missile[0] < enemy[0] + enemy_size
                and missile[1] >= enemy[1]
                and missile[1] < enemy[1] + enemy_size
            ):
                enemies.remove(enemy)
                missiles.remove(missile)
                score += 10  # Add 10 points for each hit

    for missile in enemy_missiles[:]:
        if (
            missile[0] >= player_pos[0]
            and missile[0] < player_pos[0] + player_size
            and missile[1] >= player_pos[1]
            and missile[1] < player_pos[1] + player_size
        ):
            game_over = True
            return

def draw_elements():
    screen.fill(BLACK)
    screen.blit(player_image, (player_pos[0], player_pos[1]))
    for enemy_pos in enemies:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))
    for missile in missiles:
        screen.blit(missile_image, (missile[0], missile[1]))
    for missile in enemy_missiles:
        screen.blit(missile_image, (missile[0], missile[1]))
    draw_text('Score: ' + str(score), WHITE, (screen_width // 2, 10))

def game_loop():
    global player_pos, game_over, score, enemy_speed, missiles

    player_pos = [screen_width // 2, screen_height - player_size]
    enemies = []
    missiles = []
    enemy_missiles = []
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    missiles.append([player_pos[0] + player_size // 2, player_pos[1]])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size - player_speed:
            player_pos[0] += player_speed

        drop_enemies()
        if update_enemy_positions():
            game_over = True

        move_missiles()
        move_enemy_missiles()
        collision_check()

        draw_elements()
        pygame.display.update()
        clock.tick(30)

    screen.fill(BLACK)
    draw_text('GAME OVER', WHITE, (screen_width / 2, screen_height / 2 - 50))
    draw_text('Score: ' + str(score), WHITE, (screen_width / 2, screen_height / 2 + 20))
    draw_text('Press Enter to Restart', WHITE, (screen_width / 2, screen_height / 2 + 70))
    pygame.display.update()
    pygame.time.wait(1000)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    enemy_speed = 1
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Main game loop
restart = True
while restart:
    game_over = False
    score = 0
    player_pos = [screen_width // 2, screen_height - player_size]
    enemies = []
    missiles = []
    enemy_missiles = []
    restart = game_loop()

pygame.quit()
