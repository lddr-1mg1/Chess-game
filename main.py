import json
import pygame
from collections import Counter

with open("pieces.json") as f:
    pieces = json.load(f)  # Import every pieces settings

# Initialize pygame
pygame.init()

# Screen settings
screen_width = 1300
square_size = screen_width // 8
light_square_color = "#d5c9bb"
dark_square_color = "#b2a696"
screen = pygame.display.set_mode((screen_width, screen_width))
blured_background = pygame.transform.scale(pygame.image.load("./images/blured_background.jpg"), (screen_width, screen_width))

# Game settings
current_player = "White"
running = True
dragging_piece = None
positions_already_have = []

# Sliced pieces informations (types, colors, positions, moves, images)
pieces_types = {}
pieces_colors = {}
pieces_positions = {}
pieces_moves = {}
pieces_images = {}

# Slicing pieces informations and put into dictionaries
for piece in pieces["pieces"]:
    piece_id = piece["id"]
    pieces_types[piece_id] = piece["type"]
    pieces_colors[piece_id] = piece["color"]
    pieces_positions[piece_id] = piece["position"]
    pieces_moves[piece_id] = piece["moves"]
    img = pygame.image.load(piece["image"])
    pieces_images[piece_id] = pygame.transform.scale(img, (square_size, square_size))

# Draw the chessboard
def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = pygame.Color(light_square_color) if (row + col) % 2 == 0 else pygame.Color(dark_square_color) # Alternating colors
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size)) # Draw the square

# Draw the pieces
def draw_piece(piece_id, piece_x_position, piece_y_position):
    piece_image = pieces_images[piece_id]
    grid_x_position = (piece_x_position * square_size) + (square_size - piece_image.get_width()) // 2 # x center the piece on the square
    grid_y_position = (piece_y_position * square_size) + (square_size - piece_image.get_height()) // 2 # y center the piece on the square
    screen.blit(piece_image, (grid_x_position, grid_y_position)) # Draw the piece on the screen

def draw_by_lack_of_pieces(): # pas exactement correcte
    nb_pieces = len(pieces_positions)
    if nb_pieces == 2:
        draw_text("Nulle par manque de matériel") # Draw the text "Nulle par manque de materiel"


def draw_by_repitition():
    immutable_positions = tuple(sorted((piece_id, tuple(piece_position)) for piece_id, piece_position in pieces_positions.items())) # Convert the dict to a tuple of tuples wich can be hashed (By cha)
    positions_already_have.append(immutable_positions) #Add the current position to the list of positions already have
    counter = Counter(positions_already_have) # Count the number of times each position appears
    if any(count == 3 for count in counter.values()): # If a position appears 3 times 
        draw_text("DRAW BY REPETITION") # Draw the text "Draw by repitition"

def draw_text(text):
    screen.blit(blured_background, (0, 0))  # Display the background
    font = pygame.font.SysFont("Segoe_ui", 66, bold=True)  # Create a font 
    message = font.render(text, True, pygame.Color("#FFFFFF")) # Create text
    text_rect = message.get_rect(center=(screen_width // 2, screen_width // 2)) # Center the text
    screen.blit(message, text_rect.topleft)  # Display the text
    pygame.display.flip()  # Update screen
    pygame.time.wait(5000)  # Wait 10 seconds
    pygame.quit()  # Quit pygame

def is_within_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8  # Check if the position is within the board

def is_cell_occuped(x, y):
    for position in pieces_positions.values(): # For each position in the pieces positions
        if position == [x, y]: # Check if the position is occupied
            return True
    return False

def turn(piece_id):
    return pieces_colors[piece_id] == current_player # Check if its the current player turn

def is_path_clear(piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    # Calculate the difference between the new position and the current position
    difference_x = new_piece_x_position - piece_x_position
    difference_y = new_piece_y_position - piece_y_position

    # Calculate the direction of the movement (1 or -1)
    direction_x = difference_x // abs(difference_x) if difference_x != 0 else 0
    direction_y = difference_y // abs(difference_y) if difference_y != 0 else 0
    
    # Move one time in the direction of the movement
    movement_x = piece_x_position + direction_x
    movement_y = piece_y_position + direction_y
    
    while (movement_x, movement_y) != (new_piece_x_position, new_piece_y_position):
        if [movement_x, movement_y] in pieces_positions.values(): # If the cell is occupied return false
            return False
        # Increases the movement by the direction
        movement_x += direction_x 
        movement_y += direction_y
    return True # If no piece is on the path return True

def catch_piece(piece_id, new_piece_x_position, new_piece_y_position):
    # Slice the new position to get x and y
    new_piece_position = [new_piece_x_position, new_piece_y_position]
    # Get piece color
    piece_color = pieces_colors[piece_id]
    
    for target_id, target_position in list(pieces_positions.items()): 
        # If the target position is the new position and the target is not the piece
        if target_position == new_piece_position and target_id != piece_id:
            # If the target color is different from the piece color
            if piece_color != pieces_colors[target_id]: 
                del pieces_positions[target_id] # Delete the target piece
            else:
                return False
    return True

def can_someone_move(color):
    legal_moves = []
    for cell in accessible_cells(color):
        if not is_cell_checked(cell, color):
            legal_moves.append(cell)
    print(legal_moves)
    if legal_moves == 0:
        print("False")
        return False
    else:
        print("true")
        return True
# Return the accessible cells of all pieces for a color
def accessible_cells(color):
    accessibles_cells = [] # Contains all the accessible cells
    for piece_id in pieces_positions: # For each piece
        if pieces_colors[piece_id] == color: # If the piece color is the same as the color
            piece_x_position, piece_y_position = pieces_positions[piece_id] # Slice the piece position
            piece_type = pieces_types[piece_id] # Get the piece type
            # Basically the as the different pieces movements but instead of moving the piece we append the accessible cells
            if "rook" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if (x_cell == piece_x_position or y_cell == piece_y_position) and is_path_clear(piece_x_position, piece_y_position, x_cell, y_cell):
                            accessibles_cells.append([x_cell, y_cell])

            elif "knight" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if ((abs(x_cell - piece_x_position) == 2 and abs(y_cell - piece_y_position) == 1) or
                            (abs(x_cell - piece_x_position) == 1 and abs(y_cell - piece_y_position) == 2)):
                            accessibles_cells.append([x_cell, y_cell])

            elif "bishop" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if abs(x_cell - piece_x_position) == abs(y_cell - piece_y_position) and is_path_clear(piece_x_position, piece_y_position, x_cell, y_cell):
                            accessibles_cells.append([x_cell, y_cell])

            elif "queen" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if (abs(x_cell - piece_x_position) == abs(y_cell - piece_y_position)
                                or x_cell == piece_x_position
                                or y_cell == piece_y_position):
                            if is_path_clear(piece_x_position, piece_y_position, x_cell, y_cell):
                                accessibles_cells.append([x_cell, y_cell])
            
            # We only calculate the catching movements for the pawns because this function is only used for the check
            elif "pawn" in piece_type:
                direction = -1 if "Black_pawn" in piece_type else 1
                left_diag = [piece_x_position - 1, piece_y_position + direction]
                right_diag = [piece_x_position + 1, piece_y_position + direction]
                if is_within_board(left_diag[0], left_diag[1]):
                    accessibles_cells.append(left_diag)
                if is_within_board(right_diag[0], right_diag[1]):
                    accessibles_cells.append(right_diag)

            elif "king" in piece_type:
                for x_cell in range(8):
                    for y_cell in range(8):
                        if abs(x_cell - piece_x_position) <= 1 and abs(y_cell - piece_y_position) <= 1:
                            accessibles_cells.append([x_cell, y_cell])
    
    return accessibles_cells # Return every pieces accessible cells

def is_cell_checked(cell_position, target_color):
    opponent_color = "White" if target_color == "Black" else "Black" # Get the opponent color
    return cell_position in accessible_cells(opponent_color) # Check if the cell is in the opponent accessible cells if it is the cell is checked

def is_prise_en_passant_legit(pawn_id, new_piece_x_position, new_piece_y_position):
    piece_x_position, piece_y_position = pieces_positions[pawn_id] # Get the pawn position
    pawn_color = pieces_colors[pawn_id] # Get the pawn color
    direction = 1 if pawn_color == "White" else -1 # Get the direction of the pawn

    # If the pawn moves diagonally
    if (new_piece_x_position, new_piece_y_position) in [
        (piece_x_position + 1, piece_y_position + direction),
        (piece_x_position - 1, piece_y_position + direction)
    ]:
        # Get the adjacent cells
        adjacents_positions = [
            (piece_x_position + 1, piece_y_position),
            (piece_x_position - 1,piece_y_position)
        ]

        # For each adjacent cell
        for adjacent_x, adjacent_y in adjacents_positions:
            # For each piece on the board
            for target_id, target_position in pieces_positions.items():
                # If the target position is the adjacent cell and the target is a pawn
                if target_position == [adjacent_x, adjacent_y] and pieces_types[target_id] in {"Black_pawn", "White_pawn"}:
                    # If the target color is different from the pawn color and the target has never moved (so possibly moved 2 squares)
                    if pieces_colors[target_id] != pawn_color and pieces_moves[target_id] == 1:
                        if new_piece_x_position == target_position[0]:
                            del pieces_positions[target_id] # Delete the target piece
                            return True
    return False

def pawn_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "pawn" not in pieces_types[piece_id]:
        return
    
    direction = -1 if "Black_pawn" in pieces_types[piece_id] else 1 # Get the direction of the pawn (1 or -1)
    steps = [1, 2] if pieces_moves[piece_id] == 0 else [1] # If the pawn has never moved it can move 2 squares else 1 square
    allowed_moves = [(piece_x_position, piece_y_position + direction * step) for step in steps] # Calculate the allowed moves
    
    # Get diagonal moves for captguring
    diagonal_captures = [
        (piece_x_position - 1, piece_y_position + direction),
        (piece_x_position + 1, piece_y_position + direction)
    ]

    # Strait movement, if the new position is allowed 
    if (new_piece_x_position, new_piece_y_position) in allowed_moves:
        # If the new position is not occupied
        if [new_piece_x_position, new_piece_y_position] not in pieces_positions.values():
            move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
            return

    # Diagonal capture, if the new position is a diagonal
    if (new_piece_x_position, new_piece_y_position) in diagonal_captures:
        # Sclice the new position
        new_piece_position = [new_piece_x_position, new_piece_y_position]
        # For each piece on the board
        for target_id, position in pieces_positions.items():
            # If the target position is the new position and the target is not the piece
            if position == new_piece_position and pieces_colors[target_id] != pieces_colors[piece_id]:
                move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
                return

    # Prise en passant
    if is_prise_en_passant_legit(piece_id, new_piece_x_position, new_piece_y_position):
        move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def rook_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "rook" not in pieces_types[piece_id]:
        return
    if not (new_piece_x_position == piece_x_position or new_piece_y_position == piece_y_position):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)


def knight_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "knight" not in pieces_types[piece_id]:
        return
    if not ((abs(new_piece_x_position - piece_x_position) == 2 and abs(new_piece_y_position - piece_y_position) == 1) or
            (abs(new_piece_x_position - piece_x_position) == 1 and abs(new_piece_y_position - piece_y_position) == 2)):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

def bishop_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "bishop" not in pieces_types[piece_id]:
        return
    if not abs(piece_x_position - new_piece_x_position) == abs(piece_y_position - new_piece_y_position):
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)


def queen_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "queen" not in pieces_types[piece_id]:
        return
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)

# ----------------------- NOT FINISHED ----------------------- YES Iit's finished !!!!
def king_movement(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if "king" not in pieces_types[piece_id]: # Checks if the piece is a king
        return
        
    if(pieces_moves[8] == 0 and pieces_moves[1] == 0 and dragging_piece == 8) and new_piece_x_position == 1 and not is_king_in_check("White"):
        print("le")
        if [2, 0] in accessible_cells("Black"):
            return
        if not (new_piece_x_position - piece_x_position) >= -2 and (new_piece_x_position - piece_x_position) <= 1 and abs(new_piece_y_position - piece_y_position) <= 1:
            return
            
    elif(pieces_moves[24] == 0 and pieces_moves[17] == 0 and dragging_piece == 24) and new_piece_x_position == 1 and not is_king_in_check("Black"):
        print("la")
        if [2, 7] in accessible_cells("White"):
            return
        if not (new_piece_x_position - piece_x_position) >= -2 and (new_piece_x_position - piece_x_position) <= 1 and abs(new_piece_y_position - piece_y_position) <= 1:
            return
    
    elif ((pieces_moves[8] == 0 and pieces_moves[2] == 0) and new_piece_y_position == 0) and not is_king_in_check("White"):
        print("da")
        if not (new_piece_x_position - piece_x_position) <= 2 and (new_piece_y_position - piece_y_position) <= 1:
            return
        if is_cell_occuped(6, 0) and new_piece_x_position == 5:
            return
        if [4, 0] in accessible_cells("Black") or [5, 0] in accessible_cells("Black"):
            return

    elif ((pieces_moves[24] == 0 and pieces_moves[18] == 0) and new_piece_y_position == 7) and not is_king_in_check("Black"):
        print("kjgn")
        if is_cell_occuped(6, 7) and new_piece_x_position == 5:
            return
        if not (new_piece_x_position - piece_x_position) <= 2 and (new_piece_y_position - piece_y_position) <= 1:
            return
        if [4, 7] in accessible_cells("White") or [5, 7] in accessible_cells("White"):
            return
    
    # Checks king if movement is for the king.
    else:
        print("de")
        if not (abs(new_piece_x_position - piece_x_position) <= 1 and abs(new_piece_y_position - piece_y_position) <= 1):
            return
    
    print("ICI")
    move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position)
    little_castle(pieces_positions[dragging_piece])
    big_castle(pieces_positions[dragging_piece])

def little_castle(position_of_the_king):
    if pieces_moves[8] == 1: # If the white king has not moved
        if position_of_the_king == [1, 0]:
            pieces_positions[1] = [2, 0]  # Tour blanche
    elif pieces_moves[24] == 1: # If the black king has not moved
        if position_of_the_king == [1, 7]:
            pieces_positions[17] = [2, 7]  # Tour noire

def big_castle(position_of_the_king):
    if pieces_moves[8] == 1: # If the white king has not moved
        if position_of_the_king == [5, 0]:
            pieces_positions[2] = [4, 0]
    if pieces_moves[24] == 1: # If the black king has not moved
        if position_of_the_king == [5, 7]:
            pieces_positions[18] = [4, 7]

def check_promotion(piece_id, piece_y_position):
    piece_type = pieces_types[piece_id] # Get the piece type
    if piece_type == "White_pawn" and piece_y_position == 7: # If the piece is a white pawn and is at the end of the board
        promote_piece(piece_id, "White")
    elif piece_type == "Black_pawn" and piece_y_position == 0: # If the piece is a black pawn and is at the end of the board
        promote_piece(piece_id, "Black")

def promote_piece(piece_id, piece_color):
    # Get potential pieces to promote to
    options = ["queen", "bishop", "rook", "knight"]
    # Remove prefix
    prefix = "w" if piece_color == "White" else "b"
    options = [f"{prefix}_{option}" for option in options]
    # Import font
    font = pygame.font.SysFont("Segoe_ui", screen_width // 18, bold=True)
    
    def draw_promotion_screen():
        screen.blit(blured_background, (0, 0))  # Display the blurred background on the screen.
        message = font.render("Promote your piece!", True, pygame.Color("#FFFFFF"))  # Create the promotion message text.
        message_rect = message.get_rect(center=(screen_width // 2, screen_width // 3))  # Define a centered rectangle to position the text.
        screen.blit(message, message_rect)  # Display the text on the screen, centered using `message_rect`.
        
        button_width, button_height = screen_width // 5, screen_width // 9  # Set the dimensions of the buttons.
        total_buttons_width = len(options) * button_width + (len(options) - 1) * 20  # Calculate the total width of all buttons, including spaces between them.
        start_x = (screen_width - total_buttons_width) // 2  # Calculate the starting x position to center the buttons.
        button_y = screen_width // 2  # Set the y position of the buttons.
        
        button_rects = []  # Initialize an empty list to store the button rectangles.
        for i, option in enumerate(options):  # Iterate over each promotion option.
            # Draw the button
            button_x = start_x + i * (button_width + 20)  # Calculate the x position of the current button.
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)  # Create the rectangle for the button.
            button_rects.append(button_rect)  # Add the rectangle to the list of button rectangles.
            pygame.draw.rect(screen, pygame.Color("#FFFFFF"), button_rect, border_radius=15)  # Draw the button with rounded corners.
            
            # Draw the text on the button.
            option_text = font.render(option.split('_')[1], True, pygame.Color("#000000"))  # Create the text for the button using the option name.
            text_rect = option_text.get_rect(center=button_rect.center)  # Center the text within the button rectangle.
            screen.blit(option_text, text_rect)  # Display the text on the button.
        
        # Update the screen to display all elements.
        pygame.display.flip()
        
        # Return the list of button rectangles for future interaction.
        return button_rects

    button_rects = draw_promotion_screen() # Get the butttons rectangles
    running_promotion = True
    choice = None
    while running_promotion:
        # Prevents from crashing
        for event_p in pygame.event.get():
            if event_p.type == pygame.QUIT:
                pygame.quit()
            # If a mouse click is detected     
            if event_p.type == pygame.MOUSEBUTTONDOWN and event_p.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos() # Get the mouse position
                for i, button_rect in enumerate(button_rects): # For each button rectangle
                    if button_rect.collidepoint(mouse_x, mouse_y): # If the mouse is on the button
                        choice = options[i] # Set the choice to the button option
                        running_promotion = False # Stop the promotion screen
    
    pieces_types[piece_id] = choice # Set the piece type to the choice
    image_path = f"./images/{choice}_png_shadow_512px.png" # Change the piece image
    pieces_images[piece_id] = pygame.transform.scale(pygame.image.load(image_path), (square_size, square_size)) # Set the correct piece image

def is_king_in_check(color):
    for piece_id, piece_position in pieces_positions.items():
        if pieces_colors[piece_id] == color and "king" in pieces_types[piece_id]:
            return is_cell_checked(piece_position, color)
    return False

def move_piece(piece_id, piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
    if not turn(piece_id): 
        return 

    # Save current piece position
    old_piece_x_position, old_piece_y_position = piece_x_position, piece_y_position

    # Looking for a piece to capture
    piece_capturee_id = None
    for target_id, target_position in pieces_positions.items():
        if target_position == [new_piece_x_position, new_piece_y_position] and target_id != piece_id:
            piece_capturee_id = target_id
            break

    if not catch_piece(piece_id, new_piece_x_position, new_piece_y_position):
        return

    # Verify if the path is clear
    if "knight" not in pieces_types[piece_id]:
        if not is_path_clear(piece_x_position, piece_y_position, new_piece_x_position, new_piece_y_position):
            return

    # Verify if the new position is within the board
    if not is_within_board(new_piece_x_position, new_piece_y_position):
        return

    # Move the piece
    pieces_positions[piece_id] = [new_piece_x_position, new_piece_y_position]

    # Verify if the king is in check
    color = pieces_colors[piece_id]
    if is_king_in_check(color):
        # Cancel the move
        pieces_positions[piece_id] = [old_piece_x_position, old_piece_y_position]
        # Cancel the capture if needed
        if piece_capturee_id is not None:
            pieces_positions[piece_capturee_id] = [new_piece_x_position, new_piece_y_position]
        return

    global current_player
    # If the piece has correctly moved
    if (new_piece_x_position, new_piece_y_position) != (old_piece_x_position, old_piece_y_position):
        # Check promotion
        check_promotion(piece_id, new_piece_y_position)
        # Change the current player
        current_player = "Black" if current_player == "White" else "White"
        # Increment the number of moves for the piece
        pieces_moves[piece_id] += 1
        # Check draw
        draw_by_repitition()
        draw_by_lack_of_pieces()
        can_someone_move(current_player)

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

            if is_cell_checked(white_king_position, "White") or is_cell_checked(black_king_position, "Black"):
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
