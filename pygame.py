import pygame
import sys
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT_SIZE = 36


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash")


player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5


enemy_size = 50
enemy_speed = 5
enemies = []


bullet_size = 10
bullet_speed = 7
bullets = []


score = 0
health = 3


font = pygame.font.Font(None, FONT_SIZE)


playing = True
game_over = False

def reset_game():
    global player_x, player_y, enemies, bullets, score, health
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT // 2 - player_size // 2
    enemies = []
    bullets = []
    score = 0
    health = 3


clock = pygame.time.Clock()

while playing:
    while game_over:
        
        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {score // FPS}s", True, (0, 0, 0))
        play_again_text = font.render("Play Again", True, (0, 0, 0))
        quit_game_text = font.render("Quit Game", True, (0, 0, 0))

        screen.blit(game_over_text, (WIDTH // 2 - FONT_SIZE * 2, HEIGHT // 4))
        screen.blit(final_score_text, (WIDTH // 2 - FONT_SIZE * 2, HEIGHT // 2 - FONT_SIZE))
        screen.blit(play_again_text, (WIDTH // 2 - FONT_SIZE * 2, HEIGHT // 2))
        screen.blit(quit_game_text, (WIDTH // 2 - FONT_SIZE * 2, HEIGHT // 2 + FONT_SIZE))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (
                    WIDTH // 2 - FONT_SIZE * 2 < mouse_x < WIDTH // 2 + FONT_SIZE * 4
                    and HEIGHT // 2 < mouse_y < HEIGHT // 2 + FONT_SIZE
                ):
                    reset_game()
                    game_over = False
                elif (
                    WIDTH // 2 - FONT_SIZE * 2 < mouse_x < WIDTH // 2 + FONT_SIZE * 4
                    and HEIGHT // 2 + FONT_SIZE < mouse_y < HEIGHT // 2 + 2 * FONT_SIZE
                ):
                    playing = False
                    game_over = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                    game_over = False
            elif event.key == pygame.K_f:
                bullets.append([player_x + player_size, player_y + player_size // 2])

    if not game_over:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
            player_y += player_speed

        
        if random.randint(0, 100) < 5:  
            enemy_y = random.randint(0, HEIGHT - enemy_size)
            enemies.append([WIDTH, enemy_y])

       
        for enemy in enemies:
            enemy[0] -= enemy_speed

       
        for bullet in bullets:
            bullet[0] += bullet_speed

        
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
            if player_rect.colliderect(enemy_rect):
                health -= 1
                enemies.remove(enemy)

                if health <= 0:
                    print("Game Over!")
                    game_over = True

        
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10

        
        enemies = [enemy for enemy in enemies if enemy[0] > 0]
        bullets = [bullet for bullet in bullets if bullet[0] < WIDTH]

        
        score_text = font.render(f"Score: {score // FPS}s", True, (0, 0, 0))

        
        heart_icon = pygame.image.load("heart.png")  
        heart_width, heart_height = 30, 30
        for i in range(health):
            screen.blit(heart_icon, (10 + i * (heart_width + 5), 10))

    
    screen.fill(WHITE)

    if not game_over:
        
        screen.blit(score_text, (10, 10))

        pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, player_size, player_size))

        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

        for bullet in bullets:
            pygame.draw.rect(screen, BLUE, (bullet[0], bullet[1], bullet_size, bullet_size))

    
    pygame.display.flip()

    
    clock.tick(FPS)


pygame.quit()
sys.exit()