import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SUBMARINE_COLOR = (100, 100, 255)
FPS = 60

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Underwater Shooter")

# Submarine setup
submarine_width, submarine_height = 60, 40
submarine_x = WIDTH // 2 - submarine_width // 2
submarine_y = HEIGHT - submarine_height - 10
submarine_speed = 5

# Bullet setup
bullet_width, bullet_height = 5, 10
bullets = []
bullet_speed = -10

# Enemy setup
enemy_width, enemy_height = 50, 30
enemies = []
enemy_speed = 2
spawn_rate = 30  # Spawn an enemy every 30 frames
frames_since_last_spawn = 0

# Font setup
font = pygame.font.SysFont(None, 40)

# Game variables
score = 0
math_problem = ""
correct_answer = 0
wrong_answers = []
game_over = False

# Generate a new math problem
def generate_math_problem():
    global math_problem, correct_answer, wrong_answers
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    math_problem = f"{num1} x {num2}"
    correct_answer = num1 * num2
    wrong_answers = [correct_answer + random.randint(-10, 10) for _ in range(3)]
    wrong_answers[random.randint(0, 2)] = correct_answer

# Submarine object
def draw_submarine(x, y):
    pygame.draw.rect(screen, SUBMARINE_COLOR, (x, y, submarine_width, submarine_height))

# Bullet object
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))

# Enemy object (math answers)
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, BLUE, (enemy['x'], enemy['y'], enemy_width, enemy_height))
        text = font.render(str(enemy['value']), True, WHITE)
        screen.blit(text, (enemy['x'] + 10, enemy['y'] + 5))

# Check collision between two rectangles
def is_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

# Main game loop
def main():
    global submarine_x, bullets, enemies, score, frames_since_last_spawn, game_over

    clock = pygame.time.Clock()
    generate_math_problem()

    while not game_over:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Submarine movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and submarine_x > 0:
            submarine_x -= submarine_speed
        if keys[pygame.K_RIGHT] and submarine_x < WIDTH - submarine_width:
            submarine_x += submarine_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 3:  # Limit number of bullets on screen
                bullets.append([submarine_x + submarine_width // 2 - bullet_width // 2, submarine_y])

        # Update bullets
        for bullet in bullets:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Update enemies
        frames_since_last_spawn += 1
        if frames_since_last_spawn >= spawn_rate:
            x = random.randint(0, WIDTH - enemy_width)
            value = random.choice(wrong_answers)
            enemies.append({'x': x, 'y': 0, 'value': value})
            frames_since_last_spawn = 0

        for enemy in enemies:
            enemy['y'] += enemy_speed
            if enemy['y'] > HEIGHT:
                enemies.remove(enemy)

        # Check for collisions
        for bullet in bullets:
            for enemy in enemies:
                if is_collision((bullet[0], bullet[1], bullet_width, bullet_height),
                                (enemy['x'], enemy['y'], enemy_width, enemy_height)):
                    if enemy['value'] == correct_answer:
                        score += 1
                        generate_math_problem()
                        enemies.clear()
                        bullets.clear()
                    else:
                        game_over = True
                    bullets.remove(bullet)
                    break

        # Drawing
        draw_submarine(submarine_x, submarine_y)
        draw_bullets()
        draw_enemies()

        # Display math problem
        problem_text = font.render(f"Solve: {math_problem}", True, WHITE)
        screen.blit(problem_text, (10, HEIGHT - 40))

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
