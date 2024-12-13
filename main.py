import pygame

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1000
screen = pygame.display.set_mode((screen_width, screen_width))
square_size = screen_width // 8

running = True
dragging_piece = None  # Currently dragged piece


# Load piece images
pieces_images = {
    "queen": pygame.transform.scale(pygame.image.load("./pieces/b_queen_png_shadow_512px.png"), (square_size, square_size)),
    "bishop": pygame.transform.scale(pygame.image.load("./pieces/b_bishop_png_shadow_512px.png"), (square_size, square_size)),
    "bishop2": pygame.transform.scale(pygame.image.load("./pieces/b_bishop_png_shadow_512px.png"), (square_size, square_size)),
    "bishop3": pygame.transform.scale(pygame.image.load("./pieces/b_bishop_png_shadow_512px.png"), (square_size, square_size)),
}

# Initial positions of pieces
pieces_positions = {
    "queen": [4, 4],
    "bishop": [2, 3],
    "bishop2": [5, 6],
    "bishop3": [1, 7]
}

# Draw a chess grid by coloring every other square. 
def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = pygame.Color("#d5c9bb") if (row + col) % 2 == 0 else pygame.Color("#b2a696")
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

# Draw a piece by taking the piece image and initial cordonates
def draw_piece(piece_name, x, y):
    image = pieces_images[piece_name]
    pos_x = (x * square_size) + (square_size - image.get_width()) // 2
    pos_y = (y * square_size) + (square_size - image.get_height()) // 2
    rect = pygame.Rect(pos_x, pos_y, image.get_width(), image.get_height())
    screen.blit(image, (pos_x, pos_y))
    return rect

def handle_drag_and_drop():
    global dragging_piece

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        # Detect mouse button down to start dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for piece_name, (piece_x, piece_y) in pieces_positions.items():
                piece_rect = draw_piece(piece_name, piece_x, piece_y)
                if piece_rect.collidepoint(mouse_x, mouse_y):
                    dragging_piece = piece_name
                    break

        # Detect mouse button up to drop the piece
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left button
            if dragging_piece:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Snap the piece to the nearest square
                new_x, new_y = mouse_x // square_size, mouse_y // square_size
                pieces_positions[dragging_piece] = [new_x, new_y]
                dragging_piece = None

    return True

# Main loop
while running:
    running = handle_drag_and_drop()

    # Draw chessboard
    draw_chessboard()

    # Draw all pieces
    for piece_name, (piece_x, piece_y) in pieces_positions.items():
        if piece_name == dragging_piece:
            # If dragging, move the piece with the mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pos_x = mouse_x - (square_size // 2)
            pos_y = mouse_y - (square_size // 2)
            screen.blit(pieces_images[piece_name], (pos_x, pos_y))
        else:
            draw_piece(piece_name, piece_x, piece_y)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
