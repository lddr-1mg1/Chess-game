import json # fichier json pas écrit à la main / chat gpt
import pygame

with open("pieces.json") as f:
    pieces = json.load(f)

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1000
screen = pygame.display.set_mode((screen_width, screen_width))
square_size = screen_width // 8

running = True
dragging_piece = None  # Currently dragged piece


pieces_images =  {} # création d'un dictionnaire
pieces_positions = {}

for piece in pieces["pieces"]:
        piece_id = piece["id"] # un ID différent pour chaque pièce pour eviter de reécrire par dessus 
        image = pygame.image.load(piece["image"]) # prend l'image de chaque pièce
        pieces_images[piece_id] = pygame.transform.scale(image, (square_size, square_size)) # redimensionne l'image
        pieces_positions[piece_id] = piece["position"] # prend la position de chaque pièce

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

def move_piece(piece_id, new_position): # déplace une pièce et capture une autre si necessaire
    global pieces_positions #Accède à la variable globale pieces_positions qui contient les positions actuelles de toutes les pièces
    
    for target_id, target_pos in pieces_positions.items(): # parcourt toutes les pièces du jeu
        if target_pos == new_position and target_id != piece_id: #si la position de la cible est la même que la nouvelle position de la pièce jouée et qu'elles ne sont pas les mêmes  
            del pieces_positions[target_id] # capture
            break # arrête la bouvle dès qu'une pièce est mangée

    pieces_positions[piece_id] = new_position # met à jour la position
                 

def handle_drag_and_drop():
    global dragging_piece

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        # Detect mouse button down to start dragging
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for piece_id, (piece_x, piece_y) in pieces_positions.items():
                piece_rect = draw_piece(piece_id, piece_x, piece_y)
                if piece_rect.collidepoint(mouse_x, mouse_y):
                    dragging_piece = piece_id
                    break

        # Detect mouse button up to drop the piece
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left button
            if dragging_piece:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Snap the piece to the nearest square
                new_x, new_y = mouse_x // square_size, mouse_y // square_size
                if 0 <= new_x < 8 and 0 <= new_y < 8: # limite de l'echiquié
                    pieces_positions[dragging_piece] = [new_x, new_y]
                    move_piece(dragging_piece, [new_x, new_y]) # appelle la fonction move_piece pour les captures
                    dragging_piece = None
                else:
                    print("mouvement invalide")

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
