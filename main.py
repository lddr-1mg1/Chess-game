import pygame

pygame.init()

# Screen settings
screen_width = 1000
screen_height = screen_width
screen = pygame.display.set_mode((screen_width, screen_height))

running = True

# Show a circle in a certain point
def display_piece(x, y, coulour):
    pygame.draw.circle(screen, coulour, ((screen_width*x/8)-screen_width/16, screen_height*y/8 + screen_height/16), 20, 10)


while running:
    # Prevents from crashing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Set background to white
    screen.fill("white")

    # Show a 8x8 grid with cells 1/8 of the screen witdth
    for i in range(0, screen_width, int(screen_width/8)):
        pygame.draw.line(screen, "gray", (0, i), (screen_width, i))
        pygame.draw.line(screen, "gray", (i, 0), (i, screen_width))
    

    display_piece(6, 4, "red")
    display_piece(6, 5, "blue")

    # Display pygame window
    pygame.display.flip()

    # Debugging
    print(screen_width*3/10, screen_height*5/10, "Mouse pos: ", pygame.mouse.get_pos())
pygame.quit()