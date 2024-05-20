import pygame
import random

# pygame setup
pygame.init()
screen_width = 1280
screen_height = 720
pixel_width = 50
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36, bold=True, italic=False)
running = True
game_started = False


def generate_start():
    x_range = (pixel_width // 2, screen_width - pixel_width // 2, pixel_width)
    y_range = (pixel_width // 2, screen_height - pixel_width // 2, pixel_width)
    return [random.randrange(*x_range), random.randrange(*y_range)]

def reset():
    pygame.key.set_mods(0)
    target.center = generate_start()
    snake_pixel.center = generate_start()
    return snake_pixel.copy()
    
def border():
    return snake_pixel.bottom > screen_height or snake_pixel.top < 0 \
        or snake_pixel.left < 0 or snake_pixel.right > screen_width
        
def start_screen():
    screen.fill((0, 0, 0))
    text1 = font.render("Nacisnij spacje, aby rozpoczac gre!", True, (255, 255, 255))
    text2 = font.render(" Twoj poprzedni wynik to: " + str(len(snake) - 1) , True, (255, 255, 255))
    text_rect1 = text1.get_rect(center=(screen_width //2, screen_height // 2))
    text_rect2 = text2.get_rect(center=(screen_width //2, screen_height // 3))
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    pygame.display.flip()
    

#snake
snake_pixel = pygame.rect.Rect([0, 0, pixel_width, pixel_width])
snake_pixel.center = generate_start()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1


#target
target = pygame.rect.Rect([0, 0, pixel_width, pixel_width])
target.center = generate_start()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True

    if not game_started:
        start_screen()
        continue
    
    else:
        screen.fill((18, 108, 100))

        if border():
            
            game_started = False
            snake_length = 1
            target.center = generate_start()
            snake_pixel.center = generate_start()
            snake = [snake_pixel.copy()]
            pygame.key.set_mods(0)
            continue 

    
    if snake_pixel.center == target.center:
        target.center = generate_start()
        snake_length += 1
        snake.append(snake_pixel.copy())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and snake_direction != (0, pixel_width):  
        snake_direction = (0, -pixel_width)
    elif keys[pygame.K_a] and snake_direction != (pixel_width, 0):
        snake_direction = (-pixel_width, 0)
    elif keys[pygame.K_s] and snake_direction != (0, -pixel_width):
        snake_direction = (0, pixel_width)
    elif keys[pygame.K_d] and snake_direction != (-pixel_width, 0):
        snake_direction = (pixel_width, 0)


    for snake_part in snake:
        pygame.draw.rect(screen, (128, 0, 128), snake_part)

    pygame.draw.rect(screen, "red", target)
    

    snake_pixel.move_ip(snake_direction)
    snake.insert(0, snake_pixel.copy())
    if len(snake) > snake_length:
        snake.pop()  

    text = font.render( "score: " + str(len(snake) - 1), True, (255,255,255))
    screen.blit(text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 10

pygame.quit()