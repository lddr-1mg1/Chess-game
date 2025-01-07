import json
import pygame
from collections import Counter

with open("pieces.json") as f:
    pieces = json.load(f) # Import all pieces settings

# Initialise pygame
pygame.init()

# Display settings
screen_width = 500 
square_size = screen_width // 8 
light_square_color = "#d5c9bb"
dark_square_color = "#b2a696"
screen = pygame.display.set_mode((screen_width, screen_width))

# Game settings
current_player = "White"
running = True
dragging_piece = None

# Pieces settings dictionaries
pieces_types = {}
pieces_colors = {}
pieces_positions = {}
pieces_moves = {}
pieces_images = {}

# Separates the various parameters of the pieces, and add them to the corresponding dictionaries
for piece in pieces["pieces"]:
    piece_id = piece["id"]
    pieces_types[piece_id] = piece["type"]
    pieces_colors[piece_id] = piece["color"]
    pieces_positions[piece_id] = piece["position"]
    pieces_moves[piece_id] = piece["moves"]
    img = pygame.image.load(piece["image"])
    pieces_images[piece_id] = pygame.transform.scale(img, (square_size, square_size)) # Scales the image to fit into a cell.

positions_already_have = [] # I dont know what this is for

# Draw the chess boeard
def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = pygame.Color(light_square_color) if (row + col) % 2 == 0 else pygame.Color(dark_square_color) # Colors the square, every other time black, then white
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size)) # Shows the square

# Draw the piece
def draw_piece(piece_id, piece_x_position, piece_y_position):
    piece_image = pieces_images[piece_id] # Get piece image
    grid_x_position = (piece_x_position * square_size) + (square_size - piece_image.get_width()) // 2 # Calculates the correct x-axis position
    grid_y_position = (piece_y_position * square_size) + (square_size - piece_image.get_height()) // 2 # Calculates the correct y-axis position
    screen.blit(piece_image, (grid_x_position, grid_y_position)) # Shows the piece

# I don't fucking care about this shit that doesn't work !!!
def draw_by_repitition():
    immutable_positions = tuple(sorted((pid, tuple(pos)) for pid, pos in pieces_positions.items()))
    positions_already_have.append(immutable_positions)
    counter = Counter(positions_already_have)
    if any(count == 3 for count in counter.values()):
        screen.fill("#000000")
        font = pygame.font.Font(None, 66)
        message = font.render("partie nulle par répétition", True, pygame.Color("#FFFFFF"))
        screen.blit(message, (70, 200))
        pygame.display.flip()
        pygame.time.wait(10000)
        pygame.quit()

def is_within_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8 # Checks if the cordonates are out of the board

def is_cell_occuped(x, y):
    for position in pieces_positions.values():
       if position == [x, y]:
           return True
    return False
 


def can_move(piece_id):
    return pieces_colors[piece_id] == current_player # Checks if the right player is playing 

# Checks whether the piece encloses a path obstructed by another piece.
def is_path_clear(piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    # Calculates the differcence between the current and new position
    difference_x = new_piece_x_position - piece_x_position 
    difference_y = new_piece_y_position - piece_y_position
     # Calculates the movement direction on the x and y axis (-1, 0, or 1)
    distance_x = difference_x // abs(difference_x) if difference_x != 0 else 0 
    distance_y = difference_y // abs(difference_y) if difference_y != 0 else 0
    # Calculates how far the piece advances on the x and y axes
    movement_x,  movement_y = piece_x_position + distance_x, piece_y_position + distance_y 
    # For each cell advancement, it checks whether there is a piece on it.
    while (movement_x, movement_y) != (new_piece_x_position, new_piece_y_position):
        if [movement_x, movement_y] in pieces_positions.values():
            return False
        movement_x += distance_x
        movement_y += distance_y
    return True

def little_castle(position_of_the_king):
    if pieces_moves[8] == 1:
        if position_of_the_king == [1, 0]:
            pieces_positions[1] = [2, 0] # change la position de la tour      
    elif pieces_moves[24] == 1:
        if position_of_the_king == [1, 7]:
            pieces_positions[17] = [2, 7] # change la position de la tour

def big_castle(position_of_the_king):
    if pieces_moves[8] == 1:
        if position_of_the_king == [5, 0]:
            pieces_positions[2] = [4, 0] # change la position de la tour      
            print(is_cell_occuped(6, 0))

    if pieces_moves[24] == 1:
        if position_of_the_king == [5, 7]:
            pieces_positions[18] = [4, 7] # change la position de la tour

def catch_piece(piece_id, new_piece_x_position, new_piece_y_position):
    # Assembles the new positions variables in an array
    new_piece_position = [new_piece_x_position, new_piece_y_position] 
    # Gets the piece color
    piece_color = pieces_colors[piece_id]
    # Checks if the playing piece goes on a cell already occupied by another piece
    for target_id, target_position in list(pieces_positions.items()): 
        if target_position == new_piece_position and target_id != piece_id: # Checks that the  piece does not eat itself
            if piece_color != pieces_colors[target_id]: # Checks that the  piece does not eat its own color
                del pieces_positions[target_id] # Deletes the piece
            else:
                return False
    return True

def move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if can_move(piece_id) and catch_piece(piece_id, new_piece_x_position, new_piece_y_position):
        if "knight" not in pieces_types[piece_id]: # The knight can jump over the other pieces
            if not is_path_clear(piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
                return
        if is_within_board(new_piece_x_position, new_piece_y_position):
            pieces_positions[piece_id] = [new_piece_x_position, new_piece_y_position]
            global current_player
            if (new_piece_x_position, new_piece_y_position) != (piece_x_position, piece_y_position):
                check_promotion(piece_id, new_piece_y_position) # Check if the piece can be promoted
                current_player = "Black" if current_player == "White" else "White" # Changes player turn
                pieces_moves[piece_id] += 1 # Add one move to the piece
                draw_by_repitition()

def accessible_cells(color):
    accessibles_cells = []
    for piece_id in pieces_positions:
        if pieces_colors[piece_id] == color:
            piece_x_position, piece_y_position = pieces_positions[piece_id]
            piece_type = pieces_types[piece_id]
            # Basicaly the same code as the differents pieces movement functions. Could be optimized.
            if "rook" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if (x_cell == piece_x_position or y_cell == piece_y_position) and is_path_clear(piece_x_position, piece_y_position, x_cell, y_cell):
                            accessibles_cells.append([x_cell, y_cell])

            elif "knight" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if ((abs(x_cell - piece_x_position) == 2 and abs(y_cell - piece_y_position) == 1)
                            or (abs(x_cell - piece_x_position) == 1 and abs(y_cell - piece_y_position) == 2)):
                            accessibles_cells.append([x_cell, y_cell])

            elif "bishop" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if abs(x_cell - piece_x_position) == abs(y_cell - piece_y_position) and is_path_clear(piece_x_position, piece_y_position, x_cell, y_cell):
                            accessibles_cells.append([x_cell, y_cell])

            elif "queen" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if (abs(x_cell - piece_x_position) == abs(y_cell - piece_y_position) or x_cell == piece_x_position or y_cell == piece_y_position):
                            if is_path_clear(piece_x_position, piece_y_position, x_cell, y_cell):
                                accessibles_cells.append([x_cell, y_cell])
            
            elif "pawn" in piece_type:
                direction = -1 if "Black_pawn" in piece_type else 1
                for x_cell in range(8):
                    for y_cell in range(8):
                        if abs(x_cell - piece_x_position) == 1 and (y_cell - piece_y_position) == direction:
                            if [x_cell, y_cell] in pieces_positions.values():
                                for target_id, pos in pieces_positions.items():
                                    if pos == [x_cell, y_cell] and pieces_colors[target_id] != color:
                                        accessibles_cells.append([x_cell, y_cell])

            elif "king" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if abs(x_cell - piece_x_position) <= 1 and abs(y_cell - piece_y_position) <= 1:
                            accessibles_cells.append([x_cell, y_cell])

    return accessibles_cells

def is_king_checked(king_position, king_color):
    opponent_color = "White" if king_color == "Black" else "Black"
    return king_position in accessible_cells(opponent_color)

def pawn_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "pawn" not in pieces_types[piece_id]: # Checks if the piece is a pawn
        return
    
    direction = -1 if "Black_pawn" in pieces_types[piece_id] else 1 # Checks the color of the pawn and set the direction (-1, 1)
    steps = [1, 2] if pieces_moves[piece_id] == 0 else [1] # If the pawn has not moved it can advance by two cells 
    allowed_moves = [(piece_x_position, piece_y_position + direction * step) for step in steps] # Sets the allowed moves
    diagonal_captures = [(piece_x_position - 1, piece_y_position + direction), (piece_x_position + 1, piece_y_position + direction)] # Set the allowed diagnoal moves for capturing
    
    # Checks king if movement is for the pawn.
    if (new_piece_x_position, new_piece_y_position) in allowed_moves: 
        if [new_piece_x_position, new_piece_y_position] not in pieces_positions.values(): # This verification is nessesary.
            move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            return
    
    # Checks if the pawn can catch another piece.
    if (new_piece_x_position, new_piece_y_position) in diagonal_captures:
        new_piece_position = [new_piece_x_position, new_piece_y_position]
        for target_id, position in pieces_positions.items():
            if position == new_piece_position and pieces_colors[target_id] != pieces_colors[piece_id]:
                move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                return

def rook_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "rook" not in pieces_types[piece_id]: # Checks if the piece is a rook
        return
    # Checks king if movement is for the rook.
    if not (new_piece_x_position == piece_x_position or new_piece_y_position == piece_y_position):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def knight_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "knight" not in pieces_types[piece_id]: # Checks if the piece is a knight
        return
    if not ((abs(new_piece_x_position - piece_x_position) == 2 and abs(new_piece_y_position - piece_y_position) == 1) or
            (abs(new_piece_x_position - piece_x_position) == 1 and abs(new_piece_y_position - piece_y_position) == 2)):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def bishop_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "bishop" not in pieces_types[piece_id]: # Checks if the piece is a bishop
        return
    # Checks king if movement is for the bishop.
    if not abs(piece_x_position - new_piece_x_position) == abs(piece_y_position - new_piece_y_position):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def queen_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "queen" not in pieces_types[piece_id]: # Checks if the piece is a queen
        return
    # We don't need any verification because the queen can do every allowed moves.
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position) 

def king_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "king" not in pieces_types[piece_id]: # Checks if the piece is a king
        return
    
    if (pieces_moves[8] == 0 and pieces_moves[1] == 0) or (pieces_moves[24] == 0 and pieces_moves[17] == 0):
        print("Encore la")
        print(new_piece_x_position - piece_x_position)
        if not (new_piece_x_position - piece_x_position) >= -2 and (new_piece_x_position - piece_x_position) <= 1 and abs(new_piece_y_position - piece_y_position) <= 1:
            print("tgrgtr")
            return
    
    elif (pieces_moves[8] == 0 and pieces_moves[2] == 0):
        print(is_cell_occuped(6, 0) is False)
        if is_cell_occuped(6, 0) is False:
            print("ICI")
            if not (new_piece_x_position - piece_x_position) <= 2 and (new_piece_y_position - piece_y_position) <= 1:
                return
    
    elif (pieces_moves[24] == 0 and pieces_moves[18] == 0) and is_cell_occuped(6, 7) is False:
        if is_cell_occuped(6, 7) is False:
            print("LA")
            if not (new_piece_x_position - piece_x_position) <= 2 and (new_piece_y_position - piece_y_position) <= 1:
                return
    
    # Checks king if movement is for the king.
    elif not (abs(new_piece_x_position - piece_x_position) <= 1 and abs(new_piece_y_position - piece_y_position) <= 1):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
    little_castle(pieces_positions[dragging_piece])
    big_castle(pieces_positions[dragging_piece])

# Checks if the piece arrives all on the last line (for its color) of the chess board
def check_promotion(piece_id, piece_y_position):
    piece_type = pieces_types[piece_id]
    if piece_type == "White_pawn" and piece_y_position == 7:
        promote_piece(piece_id, "White")
    elif piece_type == "Black_pawn" and piece_y_position == 0:
        promote_piece(piece_id, "Black")

def promote_piece(piece_id, piece_color):
    options = ["queen", "bishop", "rook", "knight"]
    prefix = "w" if piece_color == "White" else "b"
    options = [f"{prefix}_{option}" for option in options]
    font = pygame.font.Font(None, screen_width // 12)
    
    def draw_promotion_screen():
        bg = pygame.image.load("./images/blured_background.jpg")
        bg = pygame.transform.scale(bg, (screen_width, screen_width))
        screen.blit(bg, (0, 0))
        message = font.render("Promote your piece!", True, pygame.Color("#FFFFFF"))
        message_rect = message.get_rect(center=(screen_width // 2, screen_width // 3))
        screen.blit(message, message_rect)
        button_width, button_height = screen_width // 5, screen_width // 9
        total_buttons_width = len(options) * button_width + (len(options) - 1) * 20
        start_x = (screen_width - total_buttons_width) // 2
        button_y = screen_width // 2
        button_rects = []
        for i, option in enumerate(options):
            button_x = start_x + i * (button_width + 20)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_rects.append(button_rect)
            pygame.draw.rect(screen, pygame.Color("#FFFFFF"), button_rect, border_radius=15)
            option_text = font.render(option.split('_')[1], True, pygame.Color("#000000"))
            text_rect = option_text.get_rect(center=button_rect.center)
            screen.blit(option_text, text_rect)
        pygame.display.flip()
        return button_rects
    button_rects = draw_promotion_screen()
    running = True
    choice = None
    while running:
        for event_p in pygame.event.get():
            if event_p.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event_p.type == pygame.MOUSEBUTTONDOWN and event_p.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        choice = options[i]
                        running = False
    pieces_types[piece_id] = choice
    image_path = f"./images/{choice}_png_shadow_512px.png"
    pieces_images[piece_id] = pygame.transform.scale(pygame.image.load(image_path), (square_size, square_size))

def handle_drag_and_drop():
    global dragging_piece
    mouse_x_coordinate, mouse_y_coordinate = pygame.mouse.get_pos() # Gets mouse position
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Checks if the left mouse button is pressed
        for piece_id, (piece_x_position, piece_y_position) in pieces_positions.items(): # Gets every piece position one by one
            piece_image = pieces_images[piece_id] # Gets piece image
            
            # Converts grid position in cordonates
            grid_x_position = (piece_x_position * square_size) + (square_size - piece_image.get_width()) // 2
            grid_y_position = (piece_y_position * square_size) + (square_size - piece_image.get_height()) // 2 
            piece_rect = pygame.Rect(grid_x_position, grid_y_position, piece_image.get_width(), piece_image.get_height())
            
            # If the mouse is on the piece, set the piece as being dragged
            if piece_rect.collidepoint(mouse_x_coordinate, mouse_y_coordinate):
                dragging_piece = piece_id
    
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Checks if the left mouse button is unpressed
        if dragging_piece:
            # Snaps cordinates the news in the nearest square
            new_piece_x_position, new_piece_y_position = mouse_x_coordinate // square_size, mouse_y_coordinate // square_size 
            
            # Gets current dragging piece position
            piece_x_position, piece_y_position = pieces_positions[dragging_piece]
        
            # Checks every possible movements
            pawn_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            rook_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            knight_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            bishop_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            queen_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            king_movement(dragging_piece, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

            white_king_position = pieces_positions[8]
            black_king_position = pieces_positions[24]

            if is_king_checked(white_king_position, "White") or is_king_checked(black_king_position, "Black"):
                print("Check!")
            else:
                print("No check!")

            # No more dragged piece
            dragging_piece = None

while running:
    # Prevents from crashing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Verifies mouse input
        handle_drag_and_drop()
    
    # Shows the chessboard
    draw_chessboard()

    for piece_id, (piece_x_position, piece_y_position) in pieces_positions.items(): # Gets every piece position one by one
        # If a piece is being dragged, shows the piece at the mouse position,
        if piece_id == dragging_piece: 
            mouse_x_coordinate, mouse_y_coordinate = pygame.mouse.get_pos() # Get mouse position
            # Center the piece on the mouse
            piece_x_position = mouse_x_coordinate - (square_size // 2)
            piece_y_position = mouse_y_coordinate - (square_size // 2)
            # Shows the piece
            screen.blit(pieces_images[piece_id], (piece_x_position, piece_y_position))
        else:
            # Draws the piece at its position
            draw_piece(piece_id, piece_x_position, piece_y_position)
    
    pygame.display.flip()
# Quit pygame if we leave the main loop
pygame.quit()
