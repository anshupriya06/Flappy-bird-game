import pygame
import random

# The imports look correct for a basic Flappy Bird game using Pygame.
# No changes are needed here.

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Bird properties
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe properties
pipe_width = 70
pipe_gap = 200
pipe_x = WIDTH
pipe_speed = 3
pipes = []

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True

def draw_bird():
    pygame.draw.circle(screen, WHITE, (bird_x, int(bird_y)), bird_radius)

def create_pipe():
    gap_y = random.randint(100, HEIGHT - 100 - pipe_gap)
    pipes.append({'x': pipe_x, 'top': gap_y - pipe_gap // 2, 'bottom': gap_y + pipe_gap // 2})

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, pipe_width, pipe['top']))
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['bottom'], pipe_width, HEIGHT - pipe['bottom']))

def check_collision():
    for pipe in pipes:
        if (pipe['x'] < bird_x + bird_radius < pipe['x'] + pipe_width and
            (bird_y - bird_radius < pipe['top'] or bird_y + bird_radius > pipe['bottom'])):
            return True
    if bird_y + bird_radius > HEIGHT or bird_y - bird_radius < 0:
        return True
    return False

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_speed
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_speed = 1.0
    create_pipe()

create_pipe()

# Initialize game speed
game_speed = 1.0

# Function to adjust game speed
def adjust_game_speed(speed):
    global pipe_speed, gravity, jump_strength
    pipe_speed = 3 * speed
    gravity = 0.5 * speed
    jump_strength = -10 * speed

# Set initial game speed
adjust_game_speed(game_speed)

def game_loop():
    global running, bird_velocity, bird_y, score, game_speed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
                elif event.key == pygame.K_UP:
                    game_speed = min(2.0, game_speed + 0.1)
                    adjust_game_speed(game_speed)
                elif event.key == pygame.K_DOWN:
                    game_speed = max(0.5, game_speed - 0.1)
                    adjust_game_speed(game_speed)

        # Update bird position
        bird_velocity += gravity
        bird_y += bird_velocity

        # Move and create pipes
        for pipe in pipes:
            pipe['x'] -= pipe_speed
        if pipes and pipes[0]['x'] < -pipe_width:
            pipes.pop(0)
            score += 1
        if pipe_x - pipes[-1]['x'] > 200:
            create_pipe()

        # Check for collisions
        if check_collision():
            game_over()
            if not running:
                break

        # Draw everything
        screen.fill(BLACK)
        draw_bird()
        draw_pipes()
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        speed_text = font.render(f"Speed: {game_speed:.1f}x", True, WHITE)
        screen.blit(speed_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)

def game_over():
    global running, score, game_speed
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    speed_text = font.render(f"Speed: {game_speed:.1f}x", True, WHITE)
    retry_text = font.render("Press R to Retry or Q to Quit", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                elif event.key == pygame.K_q:
                    running = False
                    return
        
        screen.fill(BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 25))
        screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, HEIGHT // 2 + 25))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 100))
        pygame.display.flip()
        clock.tick(60)

game_loop()
pygame.quit()
