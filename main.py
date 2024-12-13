import pygame

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1000
screen = pygame.display.set_mode((screen_width, screen_width))
square_size = screen_width // 8

running = True

def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = pygame.Color("#d5c9bb") if (row + col) % 2 == 0 else pygame.Color("#b2a696")
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

def draw_piece(x, y, image):
    pos_x = (x * square_size) + (square_size - image.get_width()) // 2
    pos_y = (y * square_size) + (square_size - image.get_height()) // 2
    screen.blit(image, (pos_x, pos_y))

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the chessboard
    screen.fill("white")
    draw_chessboard()

    # Load and resize the pieces
    bishop = pygame.image.load("./pieces/b_bishop_png_shadow_512px.png")
    bishop = pygame.transform.scale(bishop, (square_size, square_size))

    queen = pygame.image.load("./pieces/b_queen_png_shadow_512px.png")
    queen = pygame.transform.scale(queen, (square_size, square_size))

    # Draw the pieces directly
    draw_piece(4, 4, queen)
    draw_piece(7, 2, bishop)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
