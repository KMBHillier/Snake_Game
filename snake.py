import pygame
import time
import random
import sys

pygame.init()

# Define some colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

dis_width = 800
dis_height = 800

border_size = 30  # Define the size of the border
inner_width = dis_width - 2 * border_size  # Adjust width
inner_height = dis_height - 2 * border_size  # Adjust height


dis = pygame.display.set_mode((dis_width, dis_width))
pygame.display.set_caption(f"Kevin's Snake Game")

game_over = False

x1 = dis_width / 2
y1 = dis_height / 2

snake_block = 10

x1_change = 0
y1_change = 0

clock = pygame.time.Clock()
snake_speed = 30

font_style = pygame.font.SysFont("bahnschrift", 25)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def custom_message(msg, color, y_displace=0, size="small"):
    font_sizes = {"small": 25,  "large": 50}

    if size in font_sizes:
        font_size = font_sizes[size]
    else:
        font_size = 25  # default size

    font_style = pygame.font.SysFont("bahnschrift", font_size)
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displace))
    dis.blit(mesg, text_rect)


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, BLUE, [x[0], x[1], snake_block, snake_block])


def create_food():
    food_x = round(random.randrange(border_size, inner_width - snake_block + border_size) / 10.0) * 10.0
    food_y = round(random.randrange(border_size, inner_height - snake_block + border_size) / 10.0) * 10.0
    return food_x, food_y


def death_block_position(snake_list, food_position):
    while True:
        posx = round(random.randrange(0, inner_width - snake_block) / 10.0) * 10.0 + border_size
        posy = round(random.randrange(0, inner_height - snake_block) / 10.0) * 10.0 + border_size
        if [posx, posy] not in snake_list and [posx, posy] != food_position:
            return posx, posy


def game_start():
    start_game = False
    while not start_game:
        dis.fill(BLACK)
        # Creating a white rectangle for play area
        pygame.draw.rect(dis, WHITE, [border_size, border_size, inner_width, inner_height])
        custom_message("Welcome to Kevin's Snake Game!", RED, y_displace=-100, size="large")
        custom_message("Press any arrow key to begin", RED, y_displace=100, size="small")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    start_game = True


def game_loop():
    global snake_speed

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    snake_speed = 10

    food_x, food_y = create_food()


    while not game_over:

        while game_close == True:
            # Filling the whole display black including border
            dis.fill(BLACK)
            # Creating a white rectangle for play area
            pygame.draw.rect(dis, WHITE, [border_size, border_size, inner_width, inner_height])
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width - border_size or x1 < border_size or y1 >= dis_height - border_size or y1 < border_size:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)

        # Creating a white rectangle for play area
        pygame.draw.rect(dis, WHITE, [border_size, border_size, inner_width, inner_height])

        pygame.draw.rect(dis, GREEN, [food_x, food_y, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x, food_y = create_food()
            Length_of_snake += 1
            snake_speed = min(40, snake_speed + 3)

        clock.tick(snake_speed)

    pygame.quit()
    quit()


game_start()
game_loop()
