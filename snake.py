import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
BORDER_COLOR = (100, 100, 100)
GRID_COLOR = (200, 200, 200)  # Light gray for gridlines

# Define display width and height
DIS_WIDTH = 600
DIS_HEIGHT = 400

# Set up the display
DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control game speed
clock = pygame.time.Clock()

# Define snake block size and game speed
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Font for displaying messages
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 10)

# Function to display the score
def your_score(score):
    value = score_font.render("Score: " + str(score), True, BLACK)
    DIS.blit(value, [10, 0])  # Display the score inside the border

# Function to display the high score
def high_score():
    try:
        with open("highscore.txt", "r") as f:
            high = int(f.read())
    except:
        high = 0
    return high

# Function to update the high score
def update_high_score(score):
    try:
        with open("highscore.txt", "r") as f:
            high = int(f.read())
    except:
        high = 0
    if score > high:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(DIS, GREEN, [x[0], x[1], snake_block, snake_block])

# Function to display a message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    DIS.blit(mesg, [DIS_WIDTH / 6, DIS_HEIGHT / 3])

# Function to draw the border
def draw_border():
    pygame.draw.rect(DIS, BORDER_COLOR, [0, 0, DIS_WIDTH, DIS_HEIGHT], 20)  # Thicker border

# Function to draw gridlines
def draw_grid():
    # Draw vertical gridlines
    for x in range(20, DIS_WIDTH, SNAKE_BLOCK):
        pygame.draw.line(DIS, GRID_COLOR, (x, 20), (x, DIS_HEIGHT - 20))  # Exclude border

    # Draw horizontal gridlines
    for y in range(20, DIS_HEIGHT, SNAKE_BLOCK):
        pygame.draw.line(DIS, GRID_COLOR, (20, y), (DIS_WIDTH - 20, y))  # Exclude border

# Game loop function
def gameLoop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    # Movement of the snake
    x1_change = 0
    y1_change = 0

    # Snake's body
    snake_List = []
    Length_of_snake = 1

    # Create the food inside the border
    foodx = round(random.randrange(20, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(20, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    while not game_over:

        while game_close:
            DIS.fill(BLUE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            your_score(Length_of_snake - 1)
            current_high_score = high_score()
            high_score_msg = "High Score: " + str(current_high_score)
            high_score_text = font_style.render(high_score_msg, True, BLACK)
            DIS.blit(high_score_text, [DIS_WIDTH / 6, DIS_HEIGHT / 4])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Check if the snake hits the boundaries
        if x1 >= DIS_WIDTH - 20 or x1 < 20 or y1 >= DIS_HEIGHT - 20 or y1 < 20:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        DIS.fill(BLUE)

        # Draw the border
        draw_border()

        # Draw the grid
        draw_grid()

        # Draw the food (inside the border)
        pygame.draw.rect(DIS, RED, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # Move the snake
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake
        our_snake(SNAKE_BLOCK, snake_List)

        # Display the current score inside the border
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if the snake eats the food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(20, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(20, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            Length_of_snake += 1

        # Update the high score
        update_high_score(Length_of_snake - 1)

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# Start the game
gameLoop()