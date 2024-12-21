import json # Json file generated by ChatGPT
import pygame # Import pygame to create a GUI

with open("pieces.json") as f:
    pieces = json.load(f) # Set pieces settings

screen_width = 1000 # Set the width (and the height) of the window
square_size = screen_width // 8 # Set the width and the height of the squares
light_square_color = "#d5c9bb" # Light Squares color
dark_square_color = "#b2a696" # Dark Squares color

screen = pygame.display.set_mode((screen_width, screen_width)) # Apply the height to the window

current_player = "White" # The whites start
running = True # Main loop variable
dragging_piece = None # Contains the piece that is beeing dragged

# These are empty dictionaries that will be filled later in the code
pieces_types = {} # Create a dictionary with every piece type
pieces_colors = {} # Create a dictionary with every piece color
pieces_positions = {} # Create a dictionary with every piece position
pieces_moves = {} # Create a dictionary with every piece move count
pieces_images = {} # Create a dictionary with every piece image
accessibles_cells = []

# Get precises pieces settings
for piece in pieces["pieces"]:
    piece_id = piece["id"] # Get piece id 
    pieces_types[piece_id] = piece["type"] # Get piece type and add it into the pieces_colors dictionary
    pieces_colors[piece_id] = piece["color"] # Get piece color and add it into the pieces_colors dictionary
    pieces_positions[piece_id] = piece["position"] # Get piece position and add it into the pieces_position dictionary
    pieces_moves[piece_id] = piece["moves"] # Get the piece number of moves during the party
    piece_image = pygame.image.load(piece["image"]) # Get the image path
    pieces_images[piece_id] = pygame.transform.scale(piece_image, (square_size, square_size)) # Transform image to the right size and add it into pieces_image dictionary

# Draws a chess grid by coloring every squares. 
def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = pygame.Color(light_square_color) if (row + col) % 2 == 0 else pygame.Color(dark_square_color) # Determines the color of the square if the square "coordinate" is odd or even
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size)) # Draws the square 

def draw_piece(piece_id, piece_x_position, piece_y_position):
    piece_image = pieces_images[piece_id] # Get precise image path
    grid_x_position = (piece_x_position * square_size) + (square_size - piece_image.get_width()) // 2 # Get the correct column
    grid_y_position = (piece_y_position * square_size) + (square_size - piece_image.get_width()) // 2 # Get tje correct row
    screen.blit(piece_image, (grid_x_position, grid_y_position)) # Display the piece on the screen

def is_within_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def can_move(piece_id):
    piece_color = pieces_colors[piece_id] 
    return piece_color == current_player # Verifies if it the player's turn

def is_path_clear(piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):

    difference_x = new_piece_x_position - piece_x_position # Gets the number of cell that the piece aims to reach for x 
    difference_y = new_piece_y_position - piece_y_position # Gets the number of cell that the piece aims to reach for y

    distance_x = (difference_x // abs(difference_x)) if difference_x != 0 else 0 # Check if the piece has moved forward/backward or not in the x axis
    distance_y = (difference_y // abs(difference_y)) if difference_y != 0 else 0 # Check if the piece has moved forward/backward or not in the x axis

    x, y = piece_x_position + distance_x, piece_y_position + distance_y 
    
    while (x, y) != (new_piece_x_position, new_piece_y_position): # Test all cells one by one
        if [x, y] in pieces_positions.values(): # If the on cell on the path is already busy
            return False # Blocked path
        x += distance_x
        y += distance_y

    return True

def move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if can_move(piece_id) and catch_piece(piece_id, new_piece_x_position,new_piece_y_position):
        # Ignore path clearing for knights
        if "knight" not in pieces_types[piece_id]:
            if not is_path_clear(piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
                return

        # Move the piece
        if is_within_board(new_piece_x_position, new_piece_y_position):
            pieces_positions[piece_id] = [new_piece_x_position, new_piece_y_position]
            global current_player

            if (new_piece_x_position, new_piece_y_position) != (piece_x_position, piece_y_position):  # If the new cell is not the same with the current cell
                current_player = "Black" if current_player == "White" else "White"  # Change player
                pieces_moves[piece_id] = pieces_moves[piece_id] + 1  # Add one move to the piece
        
def catch_piece(piece_id, new_piece_x_position, new_piece_y_position):
    new_piece_position = [new_piece_x_position, new_piece_y_position]
    piece_color = pieces_colors[piece_id]

    for target_id, target_position in list(pieces_positions.items()):
        if target_position == new_piece_position and target_id != piece_id:
            if piece_color != pieces_colors[target_id]:
                del pieces_positions[target_id]  # Catch piece
            else:
                return False  # Can't catch his own piece
    return True

def accessible_cells(color):
    for piece_id in pieces_positions:
        if pieces_colors[piece_id] != color: # prend en compte que les pièce de la couleur donnée
            for x_cell in range(8):
                for y_cell in range(8):
                    if "rook" in pieces_types[piece_id]: # Checks if the piece is a rook
                        if (x_cell == pieces_positions[piece_id][0] or y_cell == pieces_positions[piece_id][1]) and is_path_clear(pieces_positions[piece_id][0], pieces_positions[piece_id][1], x_cell, y_cell):
                            accessibles_cells.append([x_cell, y_cell])
                
                    elif "knight" in pieces_types[piece_id]:
                        if  ((abs(x_cell - pieces_positions[piece_id][0]) == 2 and abs(y_cell - pieces_positions[piece_id][1]) == 1) or
                            (abs(x_cell - pieces_positions[piece_id][0]) == 1 and abs(y_cell - pieces_positions[piece_id][1]) == 2)):
                            accessibles_cells.append([x_cell, y_cell])
                
                    elif "bishop" in pieces_positions[piece_id]:
                        if (abs(x_cell - pieces_positions[piece_id][0]) == abs(pieces_positions[piece_id][0]) and is_path_clear(pieces_positions[piece_id][0], pieces_positions[piece_id][1], x_cell, y_cell)):
                            accessibles_cells.append([x_cell, y_cell])
                
                    elif "queen" in pieces_positions[piece_id]:
                        if (((abs(x_cell - pieces_positions[piece_id][0]) == abs(pieces_positions[piece_id][0])) or (x_cell == pieces_positions[piece_id][0] or y_cell == pieces_positions[piece_id][1])) and is_path_clear(pieces_positions[piece_id][0], pieces_positions[piece_id][1], x_cell, y_cell)):
                            accessibles_cells.append([x_cell, y_cell])
                    
                    elif "king" in pieces_positions[piece_id]:
                        if ((abs(x_cell - pieces_positions[piece_id][0]) <= 1 and abs(y_cell - pieces_positions[piece_id][1]) <= 1) and is_path_clear(pieces_positions[piece_id][0], pieces_positions[piece_id][1], x_cell, y_cell)):
                            accessibles_cells.append([x_cell, y_cell])
                
                    elif "pawn" in pieces_positions[piece_id]:
                        direction = 1 if color == "white" else -1
                        if ((x_cell - pieces_positions[piece_id][0] == -1 or x_cell - pieces_positions[piece_id][0] == -1) and pieces_positions[piece_id][1] == y_cell + direction):
                            accessibles_cells.append([x_cell, y_cell])
                
                y_cell += 1
            x_cell += 1
    
    print(accessibles_cells)

def pawn_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "Pawn" not in pieces_types[piece_id]:
        return

    direction = -1 if "Black_Pawn" in pieces_types[piece_id] else 1
    steps = [1, 2] if pieces_moves[piece_id] == 0 else [1]

    allowed_moves = [(piece_x_position, piece_y_position + direction * step) for step in steps]

    diagonal_captures = [
        (piece_x_position - 1, piece_y_position + direction),
        (piece_x_position + 1, piece_y_position + direction),
    ]

    if (new_piece_x_position, new_piece_y_position) in allowed_moves:
        if [new_piece_x_position, new_piece_y_position] not in pieces_positions.values():
            move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            return

    if (new_piece_x_position, new_piece_y_position) in diagonal_captures:
        target_position = [new_piece_x_position, new_piece_y_position]
        for target_id, position in pieces_positions.items():
            if position == target_position and pieces_colors[target_id] != pieces_colors[piece_id]:
                move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                return

def rook_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "rook" not in pieces_types[piece_id]: # Checks if the piece is a rook
        return
    print("Les cases accescibles de la tour sont ", accessibles_cells)

    if not (new_piece_x_position == piece_x_position or new_piece_y_position == piece_y_position): # If the movement is not a strait line the movement is not allowed
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
    

def knight_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "knight" not in pieces_types[piece_id]: # Check if the piece is a knight
        return
    
    if not ((abs(new_piece_x_position - piece_x_position) == 2 and abs(new_piece_y_position - piece_y_position) == 1) or
            (abs(new_piece_x_position - piece_x_position) == 1 and abs(new_piece_y_position - piece_y_position) == 2)):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def bishop_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "bishop" not in pieces_types[piece_id]: # Check if the piece is a bishop
        return
    
    if not abs(piece_x_position - new_piece_x_position) == abs(piece_y_position - new_piece_y_position):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def queen_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "queen" not in pieces_types[piece_id]: # Check if the piece is a queen
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def king_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "King" not in pieces_types[piece_id]: # Check if the piece is a king
        return
    
    if not (abs(new_piece_x_position - piece_x_position) <= 1 and abs(new_piece_y_position - piece_y_position) <= 1):
        return

    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def check_promotion(piece_id, piece_y_position):
    piece_type = pieces_types[piece_id]

    if piece_type == "White_Pawn" and piece_y_position == 7:
        promote_piece(piece_id, "White")
    elif piece_type == "Black_Pawn" and piece_y_position == 0:
        promote_piece(piece_id, "Black")

def promote_piece(piece_id, piece_color):
    options = ["queen", "bishop", "rook", "knight"]
    prefix = "w" if piece_color == "White" else "b"
    options = [f"{prefix}_{option}" for option in options]
    font = pygame.font.Font(None, screen_width//12)

    def draw_promotion_screen():
        # Charger et redimensionner l'image de fond
        bg = pygame.image.load("./images/blured_background.jpg")
        bg = pygame.transform.scale(bg, (screen_width, screen_width))
        screen.blit(bg, (0, 0))
        
        # Afficher le message centré
        message = font.render("Promote your piece!", True, pygame.Color("#FFFFFF"))
        message_rect = message.get_rect(center=(screen_width // 2, screen_width // 3))
        screen.blit(message, message_rect)
        
        # Calculer les dimensions et positions des boutons
        button_width, button_height = screen_width//5, screen_width//9
        total_buttons_width = len(options) * button_width + (len(options) - 1) * 20  # Inclure les espaces entre les boutons
        start_x = (screen_width - total_buttons_width) // 2  # Point de départ pour centrer les boutons horizontalement
        button_y = screen_width // 2  # Position verticale des boutons
        
        button_rects = []
        for i, option in enumerate(options):
            # Calculer la position de chaque bouton
            button_x = start_x + i * (button_width + 20)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_rects.append(button_rect)

            # Dessiner les boutons avec des bords arrondis
            pygame.draw.rect(screen, pygame.Color("#FFFFFF"), button_rect, border_radius=15)

            # Ajouter le texte centré dans chaque bouton
            option_text = font.render(option.split('_')[1], True, pygame.Color("#000000"))
            text_rect = option_text.get_rect(center=button_rect.center)
            screen.blit(option_text, text_rect)
    
        # Rafraîchir l'affichage
        pygame.display.flip()
        return button_rects

    button_rects = draw_promotion_screen() # afficher l'ecran une seule fois
    
    running = True
    choice = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        choice = options[i]
                        running = False


    pieces_types[piece_id] = choice
    image_path = f"./images/{choice}_png_shadow_512px.png"
    pieces_images[piece_id] = pygame.transform.scale(pygame.image.load(image_path), (square_size, square_size))

    draw_chessboard()
    for piece_name, (piece_x, piece_y) in pieces_positions.items():
        draw_piece(piece_name, piece_x, piece_y)
 
    pygame.display.flip()

def handle_drag_and_drop():
    global dragging_piece

    mouse_x_coordinate, mouse_y_coordinate = pygame.mouse.get_pos()  # Get x, y coordinates of the mouse

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Detect if left mouse button is pressed
        for piece_id, (piece_x_position, piece_y_position) in pieces_positions.items(): # Get every pieces x, y position on pieces_positions

            piece_image = pieces_images[piece_id]
            grid_x_position = (piece_x_position * square_size) + (square_size - piece_image.get_width()) // 2 # Get the correct column
            grid_y_position = (piece_y_position * square_size) + (square_size - piece_image.get_height()) // 2 # Get the correct row
            piece_rect = pygame.Rect(grid_x_position, grid_y_position, piece_image.get_width(), piece_image.get_height()) # Get the rectangle of the piece
            
            if piece_rect.collidepoint(mouse_x_coordinate, mouse_y_coordinate): # Verify if the piece collide with the mouse
                dragging_piece = piece_id # Set the piece as beeing dragged

    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        if dragging_piece: # Check if a piece is beeing dragged
            new_piece_x_position, new_piece_y_position = mouse_x_coordinate // square_size, mouse_y_coordinate // square_size # Set the new coordinates into a square

            if is_within_board(new_piece_x_position, new_piece_y_position):
                piece_x_position, piece_y_position = pieces_positions[dragging_piece]
            
                # Test every movements
                pawn_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                rook_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                knight_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                bishop_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                queen_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                king_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

                check_promotion(dragging_piece, new_piece_y_position)

            dragging_piece = None

# Initialize Pygame 
pygame.init()            

while running:
    # Prevents from crashing
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    # Draws the chessboard
    draw_chessboard()

    #accessible_cells() # Future -> Call when the king moves
    # pygame.quit()
    # Handle drag and drop
    handle_drag_and_drop()

    # Draws the pieces 
    for piece_id, (piece_x_position, piece_y_position) in pieces_positions.items(): 
        if piece_id == dragging_piece:
            mouse_x_coordinate, mouse_y_coordinate = pygame.mouse.get_pos() # Get x, y coordinates of the mouse
            piece_x_position = mouse_x_coordinate - (square_size // 2)
            piece_y_position = mouse_y_coordinate - (square_size // 2)
            screen.blit(pieces_images[piece_id], (piece_x_position, piece_y_position)) # Draws the piece at the new place, we can't use the draw_piece function because that will make disapear the piece while dragged.
        else :
            draw_piece(piece_id, piece_x_position, piece_y_position) # Draws the piece

    # Display the window 
    pygame.display.flip()

# Quit Pygame
pygame.quit()