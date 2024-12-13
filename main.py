import pygame
# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1000
screen_height = screen_width
screen = pygame.display.set_mode((screen_width, screen_height))
square_size = screen_width // 8

running = True

# Function to display a piece on the board
def display_piece(x, y, image):
    # Calculate the top-left position for the piece
    pos_x = (x * square_size) + (square_size - image.get_width()) // 2
    pos_y = (y * square_size) + (square_size - image.get_height()) // 2
    screen.blit(image, (pos_x, pos_y))

def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = pygame.Color("#d5c9bb") if (row + col) % 2 == 0 else pygame.Color("#b2a696")
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Set background to white
    screen.fill("white")

    # Draw the chessboard
    draw_chessboard()

    # Load and resize the piece image
    image = pygame.image.load("./pieces/b_bishop_png_shadow_512px.png")
    image = pygame.transform.scale(image, (square_size, square_size))

    image2 = pygame.image.load("./pieces/b_queen_png_shadow_512px.png")
    image2 = pygame.transform.scale(image2, (square_size, square_size))

    # Display the piece at position (6, 4)
    display_piece(4, 6, image)
    display_piece(2, 3, image)
    display_piece(3, 0, image2)

    # Update the display
    pygame.display.flip()

    print(image.get_rect())

# Quit Pygame
pygame.quit()
