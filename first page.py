import pygame
import random
from pygame import mixer
from fighter import Fighter

# Initialize mixer and pygame
mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)

# Game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Function for the front page
def front_page():
    clock = pygame.time.Clock()
    gradient_speed = 2  # Adjust this for slower or faster gradient effect
    while True:
        screen.fill(DARK_BLUE)  # Background color

        # Draw a gradient background
        for i in range(0, SCREEN_HEIGHT, gradient_speed):
            color_value = 255 - (255 // SCREEN_HEIGHT) * i
            color = (color_value, color_value, 255)
            pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

        # Draw title with shadow
        draw_text("Street Fighter Game", pygame.font.Font("assets/fonts/turok.ttf", 70), YELLOW, SCREEN_WIDTH / 6, SCREEN_HEIGHT / 4)

        # Draw button-like text for start
        draw_text("Press ENTER to Start", pygame.font.Font("assets/fonts/turok.ttf", 40), WHITE, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game when ENTER is pressed
                    return  # Exit the front page loop to start the game

        pygame.display.update()
        clock.tick(30)  # Control the frame rate

# Game loop
def game_loop():
    global intro_count, last_count_update, round_over, score  # Use global variables

    # Create two instances of fighters
    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # Game loop
    run = True
    while run:
        clock.tick(FPS)

        # Draw background
        draw_bg()

        # Show player stats
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        # Update countdown
        if intro_count <= 0:
            # Move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            # Display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            # Update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # Update fighters
        fighter_1.update()
        fighter_2.update()

        # Draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # Check for player defeat
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            # Display victory image
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update display
        pygame.display.update()

# Start the game
while True:
    front_page()  # Show the front page
    game_loop()   # Start the game loop

# Exit pygame
pygame.quit()
