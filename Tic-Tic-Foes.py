import tkinter as tk
from tkinter import ttk
import random

# to do list 
# add a numbered grid later 
# add online multiplayer 
# add turn indicator 
# make buttons nicer 
# add logic to determine draw detection and detection for if the game is 100% won 
# add a way to highlight won boards for classic and ultimate game mode 
# add animated loading screen 
# none of this is version controlled on github yet 
# refactor code to reduce number of functions and make code more readable 
# consider using classes???

# Global variables
button_generated = True # the button has not been generated yet but the syntax of the function makes it easier to invert the value. this button is agnostic of gamemode 
mode = 0 # 1 is classic 2 is advanced and 3 is ultimate 
user_symbol = ""  # To store player's chosen symbol agnostic of gamemode 
ai_symbol = ""  # To store AI's symbol agnostic of gamemode 
player1_turn = True # agnostic of gamemode since all games run on turns
game_started = False # agnostic of gamemode will be set to true when the game starts and set to false when the game ends
player2_exists = False # determine if player 2 exists, along side player1 turn, we have all the info we need to handle turn switching 
user_chosen = False
ai_chosen = False
prev_board = 20 # this is a variable that tracks what the board the previous move was made on 0 to 8. set to 20 to be invalid 

def screen_destroy():
    # clear the screen and restart
    # replace all of these with a screen_destroy() function
    for widget in root.winfo_children():
        widget.destroy()
# splash screen or title screen 
def splash_screen():

    # reset global variables if returning to splash screen
    global button_generated, mode, user_symbol, ai_symbol, player1_turn, game_started, player2_exists,user_chosen,ai_chosen,prev_board
    button_generated = True # reset
    mode = 0 # reset
    user_symbol = ""  # reset
    ai_symbol = ""  # reset
    player1_turn = True # reset
    game_started = False # reset
    player2_exists = False # reset
    user_chosen = False
    ai_chosen = False
    prev_board = 20

    screen_destroy()

    # Create the splash screen frame
    splash_screen = tk.Frame(root, bg="#1e1e2e")  # Set background color
    splash_screen.pack(fill="both", expand=True)

    # Adjust window size
    root.geometry("400x400")
    root.configure(bg="#1e1e2e")  # Set the main window background
    center_window(root)

    # Title label with larger font and color
    splash_label = tk.Label(splash_screen, text="Welcome to Tic-Tac-Foes!", font=("Arial", 18, "bold"), fg="white", bg="#1e1e2e")
    splash_label.pack(pady=20)

    # Larger buttons with styling
    button_style = {"font": ("Arial", 14), "width": 15, "height": 2, "bg": "#3b3b58", "fg": "white"}
    
    # Buttons with mode assignment
    classic_button = tk.Button(splash_screen, text="Classic", command=lambda: set_mode(1), **button_style)
    classic_button.pack(pady=10)

    advanced_button = tk.Button(splash_screen, text="Advanced", command=lambda: set_mode(2), **button_style)
    advanced_button.pack(pady=10)

    ultimate_button = tk.Button(splash_screen, text="Ultimate", command=lambda: set_mode(3), **button_style)
    ultimate_button.pack(pady=10)
    
# Function to set the mode based on button click
def set_mode(new_mode):
    global mode
    mode = new_mode
    player_selection_screen()  # Proceed to symbol selection after setting the mode agnostic of gamemode 

def player_selection_screen():
    global player2_exists
    screen_destroy()
    # create the player selection frame
    player_selection_screen = tk.Frame(root, bg="#1e1e2e")  # Set background color
    player_selection_screen.pack(fill="both", expand=True)

    # Adjust window size
    root.geometry("400x400")
    root.configure(bg="#1e1e2e")  # Set the main window background
    center_window(root)

    # Title label with larger font and color
    player_selection_label = tk.Label(player_selection_screen, text="How do you want to play?", font=("Arial", 18, "bold"), fg="white", bg="#1e1e2e")
    player_selection_label.pack(pady=20)

    # Larger buttons with styling
    button_style = {"font": ("Arial", 14), "width": 15, "height": 2, "bg": "#3b3b58", "fg": "white"}
    
    # Buttons with mode assignment
    tk.Button(player_selection_screen, text="Vs AI", 
              command=lambda: [globals().__setitem__('player2_exists', False), symbol_selector()], 
              **button_style).pack(pady=20)

    tk.Button(player_selection_screen, text="2 player game", 
              command=lambda: [globals().__setitem__('player2_exists', True), symbol_selector()], 
              **button_style).pack(pady=20)

def symbol_selector():
    global symbol_selector_label, symbol_selector_label2,player2_exists  # Make labels global to allow them to be called and edited in on_key_press

    # Clear the screen and restart
    screen_destroy()

    if player2_exists:

        # Create the selection screen frame with dark theme
        symobol_selector_frame = tk.Frame(root, bg="#1e1e2e")
        symobol_selector_frame.pack(fill="both", expand=True)

        # Title label with larger font and color
        title_label = tk.Label(symobol_selector_frame, text="Choose Your Symbol", font=("Arial", 18, "bold"), fg="white", bg="#1e1e2e")
        title_label.pack(pady=20)

        # Create labels for symbol selection with text wrapping
        symbol_selector_label = tk.Label(symobol_selector_frame, text="Player 1, choose a symbol:", font=("Arial", 14), fg="white", bg="#1e1e2e",wraplength=350, justify="center")
        symbol_selector_label.pack(pady=10)

        symbol_selector_label2 = tk.Label(symobol_selector_frame, text="Player 2, choose a symbol:", font=("Arial", 14), fg="white", bg="#1e1e2e")
        symbol_selector_label2.pack(pady=10)
    else:
        # Create the selection screen frame with dark theme
        symobol_selector_frame = tk.Frame(root, bg="#1e1e2e")
        symobol_selector_frame.pack(fill="both", expand=True)

        # Title label with larger font and color
        title_label = tk.Label(symobol_selector_frame, text="Choose Your Symbol", font=("Arial", 18, "bold"), fg="white", bg="#1e1e2e")
        title_label.pack(pady=20)

        # Create labels for symbol selection with text wrapping
        symbol_selector_label = tk.Label(symobol_selector_frame, text="Choose a symbol:", font=("Arial", 14), fg="white", bg="#1e1e2e",wraplength=350, justify="center")
        symbol_selector_label.pack(pady=10)

        symbol_selector_label2 = tk.Label(symobol_selector_frame, text="The AI will be:", font=("Arial", 14), fg="white", bg="#1e1e2e")
        symbol_selector_label2.pack(pady=10)

    # Bind keypress event for symbol selection
    root.bind("<KeyPress>", on_key_press)

def on_click_handler(row, col, board, x, y):
    global mode
    if mode == 1: # classic mode 
        on_click_classic(row, col)
    elif mode == 2: # advanceed mode 
        on_click_advanced(board, x, y)
    elif mode == 3: # ultimate mode
        on_click_ultimate(board, x, y)

def on_key_press(event):
    """Handles user key press and updates symbol choices."""

    #global variables required for this function 
    global button_generated, user_symbol, ai_symbol, game_started, player2_exists, user_chosen, ai_chosen,alternate

    # at any point if the user pressed esc, go back to splash screen
    if event.keysym == "Escape":
        splash_screen()
        return
    
    # this block of code handles assigning the user variable, 
    # known bug: when hitting enter, because a .char is used, e is placed as the user symbol which triggers some logic to reprompt the user. this is not intended behaviour 
    # this function occurs everytime there is a keypress and thus allows the user to change their selection at anytime before the game has started
    if game_started:
        pass # this line is just to prevent the user from changing their symbol once the game has started

    elif player2_exists:
        sym_1 = event.char
        if sym_1.strip() and not game_started and not user_chosen: # not game_started ensures that the user does not modify their symbol post game commencement
            user_symbol = sym_1.strip()
            symbol_selector_label.config(text="Player 1 will be : " + str(user_symbol))
            user_chosen = True

        elif sym_1.strip() and not game_started and not ai_chosen:
            if sym_1.strip() != user_symbol:
                ai_symbol = sym_1.strip()
                symbol_selector_label2.config(text="player 2 will be: " + str(ai_symbol))
                ai_chosen = True

        else:
            pass

    else:
        user_symbol = event.char
        if user_symbol.strip() and not game_started: # not game_started ensures that the user does not modify their symbol post game commencement
            symbol_selector_label.config(text="Your chosen symbol is: " + str(user_symbol))
            user_chosen = True
            # this block of code handles assigning the ai its symbol
            ai_symbol = "o" if user_symbol == "x" else "x"
            symbol_selector_label2.config(text="The AI will be: " + str(ai_symbol))
            ai_chosen = True

    # Add "Start Game" button once both players have chosen their symbols
    if user_chosen and ai_chosen and button_generated and user_symbol != ai_symbol: # button generated is True by default
        button_generated = False # prevents more buttons from being generated when a key press occurs
        start_frame = tk.Frame(root, bg="#1e1e2e")
        start_frame.pack(fill="both", expand=True)
        global start_button
        start_button = tk.Button(start_frame, text="Start Game", command=show_turn_selection,font=("Arial", 14, "bold"), width=15, height=2,bg="#ffb86c", fg="black", activebackground="#ffa94d")
        start_button.pack(pady=10)

def show_turn_selection():
    """Creates a screen for the player to choose whether to go first or second."""

    global player1_turn

    # Clear the screen and restart
    screen_destroy()
    
    turn_selection_frame = tk.Frame(root, bg="#1e1e2e")
    turn_selection_frame.pack(fill="both", expand=True)
    
    # Adjust window size
    root.geometry("400x350")
    root.configure(bg="#1e1e2e")  # Set the main window background
    center_window(root)
    if player2_exists:
        label = tk.Label(turn_selection_frame, text="Would player 1 like to go first or second?", fg="white", bg="#1e1e2e", font=("Arial", 14))
        label.pack(pady=20)
    else:
        label = tk.Label(turn_selection_frame, text="Would you like to go first or second?", fg="white", bg="#1e1e2e", font=("Arial", 14))
        label.pack(pady=20)

    button_style = {"font": ("Arial", 14), "width": 15, "height": 2, "bg": "#3b3b58", "fg": "white"}
    # Buttons for selection
    first_button = tk.Button(turn_selection_frame, text="First", command=player_start_first,**button_style)
    first_button.pack(pady=20)

    second_button = tk.Button(turn_selection_frame, text="Second", command=player_start_second,**button_style)
    second_button.pack(pady=20)

def player_start_first():
    loading_screen()

def player_start_second():
    global player1_turn
    player1_turn = False
    loading_screen()
    
def loading_screen():
    # Use the global mode variable 
    global mode,game_started

    game_started = True # this is the point by which the game has virtually begun. Loading screen is just a placeholder to make the game feel natural

    # Clear the screen and restart
    for widget in root.winfo_children():
        widget.destroy()

    # Create the loading screen frame with dark theme
    loading_frame = tk.Frame(root, bg="#1e1e2e")  # Dark background color
    loading_frame.pack(expand=True)

    # Create a label for the loading screen with updated font and color
    loading_label = tk.Label(loading_frame, text="Loading...", font=("Arial", 16, "bold"), fg="white", bg="#1e1e2e")
    loading_label.pack(pady=20)

    # Create the loading bar with updated styling
    progress = ttk.Progressbar(loading_frame, orient="horizontal", length=200, mode="indeterminate")
    progress.pack(pady=20)

    # Start the loading bar animation
    progress.start(16)  # Lower number means faster animation

    # Call the function to load the game after 3 seconds
    if mode == 1:
        root.after(1500, create_cttt_grid)  # 3000 milliseconds = 3 seconds
    elif mode == 2:
        root.after(1500, load_attt_grid)  # 3000 milliseconds = 3 seconds
    elif mode == 3:
        root.after(1500, load_uttt_grid)  # 3000 milliseconds = 3 seconds
    else:
        print("something has gone terribly wrong, contact Reuben")

# this function creates the screen for the classic gamemode
def create_cttt_grid():

    global player1_turn
    # Destroy the loading screen
    screen_destroy()

    root.geometry("600x600")  # Set an initial size for the window (adjustable)
    center_window(root)

    # Set up grid layout to fill 90% of the window size
    root.grid_rowconfigure(0, weight=1, uniform="equal")
    root.grid_rowconfigure(1, weight=1, uniform="equal")
    root.grid_rowconfigure(2, weight=1, uniform="equal")
    root.grid_columnconfigure(0, weight=1, uniform="equal")
    root.grid_columnconfigure(1, weight=1, uniform="equal")
    root.grid_columnconfigure(2, weight=1, uniform="equal")

    # Create the buttons and store them in a list
    global buttons  # Declare 'buttons' as a global variable
    buttons = []
    for row in range(3):
        for col in range(3):
            button = tk.Button(root, bg="#1e1e2e", width=10, height=3, font=("Arial", 100, "bold"), fg="white")
            button.grid(row=row, column=col, sticky="nsew")
            
            # Bind the on_click function, passing the row and column as arguments
            button.config(command=lambda r=row, c=col: on_click_handler(r, c,0,0,0))
            
            button.bind("<Enter>", on_enter_classic)
            button.bind("<Leave>", on_leave_classic)
            buttons.append(button)

    if not player2_exists and not player1_turn:
        classic_ai_turn()

# the following functions handle logic related to interacting with buttons 
def on_enter_classic(event):
    event.widget.config(bg="#ffb86c")  # Change background to orangish when player hovers over valid button

def on_leave_classic(event):
    event.widget.config(bg="#1e1e2e")  # Change background back to purple for buttons that are not highlighted

def on_click_classic(row, col):
    global player1_turn, player2_exists

    index = row * 3 + col

    # Prevent clicking on an already occupied square
    if buttons[index].cget("text") != "":
        return

    # Turn handling logic
    if player1_turn and not player2_exists:
        update_button_classic(index, str(user_symbol))
        player1_turn = False
        # Generate a random delay between 1 and 4 seconds
        delay = random.uniform(1, 2.5)        
        # Use after to call classic_ai_turn with the delay
        root.after(int(delay * 1000), classic_ai_turn)  # Convert delay to milliseconds
    elif player1_turn and player2_exists:
        update_button_classic(index, str(user_symbol))
        player1_turn = False
    elif player2_exists and not player1_turn:
        update_button_classic(index, str(ai_symbol))
        player1_turn = True

    # Check if the game is over
    winner, symbol = check_winner_classic()
    if winner:
        win_screen_classic(symbol)
    elif all(button.cget("text") != "" for button in buttons):  # Check for a draw
        draw_screen_classic()

# Function to update button text and style based on the player's symbol
def update_button_classic(index, symbol):
    buttons[index].config(text=symbol, state="disabled", disabledforeground="white")

def classic_ai_turn():
    global player1_turn

    # Get all empty squares
    empty_squares = [i for i, button in enumerate(buttons) if button.cget("text") == ""]

    if empty_squares:  # Ensure there are empty squares left
        ai_choice = random.choice(empty_squares)  # Pick a random empty square
        # Generate a random delay between 1 and 4 seconds
        delay = random.uniform(1, 2.5)        
        # Use after to call classic_ai_turn with the delay
        root.after(int(delay * 1000), update_button_classic(ai_choice, str(ai_symbol)))  # Convert delay to milliseconds
        player1_turn = True  # Give turn back to player

    # Check if the AI won
    winner, symbol = check_winner_classic()
    if winner:
        win_screen_classic(symbol)
    elif all(button.cget("text") != "" for button in buttons):  # Check for a draw
        draw_screen_classic()


# win_detection for classic mode 
def check_winner_classic():
    """
    This function checks for a winner in a classic 3x3 Tic-Tac-Toe game.
    
    Returns:
        - (True, symbol) if a player has won, where 'symbol' is the winning symbol.
        - (False, "") if there is no winner yet.

    this function is brain dead because i wrote it at 1 am 
    will come back and fix this eventually
    
    """
    
    # Check horizontal rows
    if buttons[0].cget('text') == buttons[1].cget('text') == buttons[2].cget('text') and buttons[0].cget('text') != "":
        return True, str(buttons[0].cget('text'))  # Top row

    if buttons[3].cget('text') == buttons[4].cget('text') == buttons[5].cget('text') and buttons[3].cget('text') != "":
        return True, str(buttons[3].cget('text'))  # Middle row

    if buttons[6].cget('text') == buttons[7].cget('text') == buttons[8].cget('text') and buttons[6].cget('text') != "":
        return True, str(buttons[6].cget('text'))  # Bottom row

    # Check vertical columns
    if buttons[0].cget('text') == buttons[3].cget('text') == buttons[6].cget('text') and buttons[0].cget('text') != "":
        return True, str(buttons[0].cget('text'))  # Left column

    if buttons[1].cget('text') == buttons[4].cget('text') == buttons[7].cget('text') and buttons[1].cget('text') != "":
        return True, str(buttons[1].cget('text'))  # Middle column

    if buttons[2].cget('text') == buttons[5].cget('text') == buttons[8].cget('text') and buttons[2].cget('text') != "":
        return True, str(buttons[2].cget('text'))  # Right column

    # Check diagonal wins
    if buttons[0].cget('text') == buttons[4].cget('text') == buttons[8].cget('text') and buttons[0].cget('text') != "":
        return True, str(buttons[0].cget('text'))  # Top-left to bottom-right

    if buttons[2].cget('text') == buttons[4].cget('text') == buttons[6].cget('text') and buttons[2].cget('text') != "":
        return True, str(buttons[2].cget('text'))  # Top-right to bottom-left

    # No winner
    return False, ""

def win_screen_classic(symbol):

    # destroy the ttt grid 
    screen_destroy()

    # Create the win screen frame
    win_screen = tk.Frame(root, bg="#1e1e2e")  # Set background color
    win_screen.pack(fill="both", expand=True)

    # Adjust window size
    root.geometry("400x400")
    root.configure(bg="#1e1e2e")  # Set the main window background
    center_window(root)

    # Title label with larger font and color
    win_label = tk.Label(win_screen, text=str(symbol) + " is the winner!", font=("Arial", 50, "bold"), fg="white", bg="#1e1e2e", wraplength=350)  # Set wrap length to 350 pixels
    win_label.pack(pady= 50)

    # commentary label
    if user_symbol == str(symbol) and not player2_exists:
        commentary_label = tk.Label(win_screen, text = "(That's you btw good job)", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()
    elif user_symbol == str(symbol) and player2_exists:
        commentary_label = tk.Label(win_screen, text = "Congrats player 1 ", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()    
    elif user_symbol != str(symbol) and player2_exists:
        commentary_label = tk.Label(win_screen, text = "Congrats player 2 ", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()   
    else:
        commentary_label = tk.Label(win_screen, text = "How did you let this happen? The AI is dumber than a bag of rocks", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()


def draw_screen_classic():
    screen_destroy()

    # Create the draw screen frame
    draw_screen = tk.Frame(root, bg="#1e1e2e")  # Set background color
    draw_screen.pack(fill="both", expand=True)

    # Adjust window size
    root.geometry("400x400")
    root.configure(bg="#1e1e2e")  # Set the main window background
    center_window(root)
    # Title label with larger font and color
    draw_label = tk.Label(draw_screen, text="The game is a draw :(", font=("Arial", 50, "bold"), fg="white", bg="#1e1e2e", wraplength=350)  # Set wrap length to 350 pixels
    draw_label.pack(pady= 50)
    commentary_label = tk.Label(draw_screen, text = "C'est la vie", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
    commentary_label.pack()

# this function is a placeholder
def load_attt_grid():
    screen_destroy()
    root.geometry("650x670")
    center_window(root)
    # Create advanced game frame
    game_frame = tk.Frame(root, bg="#1e1e2e")
    game_frame.pack(expand=True, fill="both", padx=20, pady=20)

    global buttons 
    buttons = []  # Store buttons for each board

    for i in range(3):
        for j in range(3):
            board_frame = tk.Frame(game_frame, bg="#1e1e2e")
            board_frame.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)

            board_buttons = []
            for x in range(3):
                for y in range(3):
                    button = tk.Button(board_frame, text="", font=("Arial", 16, "bold"), width=4, height=2,
                                    bg="#5b4279", fg="red", activebackground="#5b4279", activeforeground="white",
                                    relief="flat", highlightthickness=0,)
                    button.grid(row=x, column=y, sticky="nsew", padx=2, pady=2)
                    button.config(command=lambda b=len(buttons), bx=x, by=y: on_click_handler(0, 0, b, bx, by))
                    button.bind("<Enter>", on_enter_classic)
                    button.bind("<Leave>", on_leave_advanced)
                    board_buttons.append(button)

            buttons.append(board_buttons)

    # Make the grid expand properly
    for i in range(3):
        game_frame.columnconfigure(i, weight=1)
        game_frame.rowconfigure(i, weight=1)
    
    if not player2_exists and not player1_turn:
        advanced_ai_turn(20)

def on_click_advanced(board, x, y):
    index = x * 3 + y
    # update_button_advanced(board, index, "x")
    global player1_turn, player2_exists,prev_board
    # Prevent clicking on an already occupied square
    if buttons[board][index].cget("text") != "":
        return

    # Turn handling logic
    if player1_turn and not player2_exists and (prev_board == 20 or board == prev_board):
        update_button_advanced(board,index, str(user_symbol))
        player1_turn = False
        advanced_ai_turn(index)  # Convert delay to milliseconds
    elif player1_turn and player2_exists and (prev_board == 20 or board == prev_board):
        update_button_advanced(board,index, str(user_symbol))
        player1_turn = False
    elif player2_exists and not player1_turn and (prev_board == 20 or board == prev_board):
        update_button_advanced(board,index, str(ai_symbol))
        player1_turn = True

    # Check if the gamestate is won
    winner, symbol = check_winner_advanced()
    if winner:
        win_screen_advanced(symbol)
    elif all(button.cget("text") != "" for row in buttons for button in row):  # Check for a draw
        draw_screen_classic()

def advanced_ai_turn(index):
    global player1_turn
    if index > 8:
        index = random.randint(0, 8)
    # Get all empty squares
    empty_squares = [i for i, button in enumerate(buttons[index]) if button.cget("text") == ""]

    if empty_squares:  # Ensure there are empty squares left
        ai_choice = random.choice(empty_squares)  # Pick a random empty square   
        update_button_advanced(index,ai_choice, str(ai_symbol))
        player1_turn = True  # Give turn back to player

    # Check if the gamestate is won
    winner, symbol = check_winner_advanced()
    if winner:
        win_screen_advanced(symbol)
    elif all(button.cget("text") != "" for row in buttons for button in row):  # Check for a draw
        draw_screen_classic()

def check_winner_advanced():
    """
    This function checks for a winner in the advanced 3x3 Tic-Tac-Toe game.
    
    Returns:
        - (True, symbol) if a player has won, where 'symbol' is the winning symbol.
        - (False, "") if there is no winner yet.
    """
    
    # Loop through each 3x3 grid (sub-grid) in buttons
    for board in range(8):  # We have 9 boards in the global buttons array
        # Check horizontal rows
        if buttons[board][0].cget('text') == buttons[board][1].cget('text') == buttons[board][2].cget('text') and buttons[board][0].cget('text') != "":
            return True, str(buttons[board][0].cget('text'))  # Winning row on this board
        elif buttons[board][3].cget('text') == buttons[board][4].cget('text') == buttons[board][5].cget('text') and buttons[board][3].cget('text') != "":
            return True, str(buttons[board][3].cget('text'))  # Winning row on this board
        elif buttons[board][6].cget('text') == buttons[board][7].cget('text') == buttons[board][8].cget('text') and buttons[board][6].cget('text') != "":
            return True, str(buttons[board][6].cget('text'))  # Winning row on this board
        # Check vertical columns
        elif buttons[board][0].cget('text') == buttons[board][3].cget('text') == buttons[board][6].cget('text') and buttons[board][0].cget('text') != "":
            return True, str(buttons[board][0].cget('text'))  # Winning row on this board
        elif buttons[board][1].cget('text') == buttons[board][4].cget('text') == buttons[board][7].cget('text') and buttons[board][1].cget('text') != "":
            return True, str(buttons[board][1].cget('text'))  # Winning row on this board
        elif buttons[board][2].cget('text') == buttons[board][5].cget('text') == buttons[board][8].cget('text') and buttons[board][2].cget('text') != "":
            return True, str(buttons[board][2].cget('text'))  # Winning row on this board
        # check diagonal lines
        elif buttons[board][0].cget('text') == buttons[board][4].cget('text') == buttons[board][8].cget('text') and buttons[board][0].cget('text') != "":
            return True, str(buttons[board][0].cget('text'))  # Winning row on this board
        elif buttons[board][2].cget('text') == buttons[board][4].cget('text') == buttons[board][6].cget('text') and buttons[board][2].cget('text') != "":
            return True, str(buttons[board][2].cget('text'))  # Winning row on this board
    # No winner
    return False, ""

def white_symbol():
    for i in range(len(buttons)):  # Loop through rows (outer list)
        for j in range(len(buttons[i])):  # Loop through columns (inner list)
            if buttons[i][j].cget('text') != "" and buttons[i][j].cget('fg') == "red":
                buttons[i][j].config(fg="white")

# Function to update button text and style based on the player's symbol
def update_button_advanced(board, index, symbol):
    global prev_board
    prev_board = index
    white_symbol()
    buttons[board][index].config(text=symbol, fg="red")

def on_leave_advanced(event):
    event.widget.config(bg="#5b4279")  # Change background back to purple for buttons that are not highlighted

def win_screen_advanced(symbol):

    # destroy the ttt grid 
    screen_destroy()

    # Create the win screen frame
    win_screen = tk.Frame(root, bg="#1e1e2e")  # Set background color
    win_screen.pack(fill="both", expand=True)

    # Adjust window size
    root.geometry("400x400")
    root.configure(bg="#1e1e2e")  # Set the main window background
    center_window(root)

    # Title label with larger font and color
    win_label = tk.Label(win_screen, text=str(symbol) + " is the winner!", font=("Arial", 50, "bold"), fg="white", bg="#1e1e2e", wraplength=350)  # Set wrap length to 350 pixels
    win_label.pack(pady= 50)

    # commentary label
    if user_symbol == str(symbol) and not player2_exists:
        commentary_label = tk.Label(win_screen, text = "(That's you btw good job)", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()
    elif user_symbol == str(symbol) and player2_exists:
        commentary_label = tk.Label(win_screen, text = "Congrats player 1 ", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()    
    elif user_symbol != str(symbol) and player2_exists:
        commentary_label = tk.Label(win_screen, text = "Congrats player 2 ", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()   
    else:
        commentary_label = tk.Label(win_screen, text = "How did you let this happen? ", font=("Arial", 20, "bold"), fg="white", bg="#1e1e2e", wraplength=350)
        commentary_label.pack()

# this function is a placeholder
def load_uttt_grid():
    screen_destroy()
    root.geometry("650x670")
    center_window(root)
    # Create advanced game frame
    game_frame = tk.Frame(root, bg="#1e1e2e")
    game_frame.pack(expand=True, fill="both", padx=20, pady=20)

    global buttons 
    buttons = []  # Store buttons for each board

    for i in range(3):
        for j in range(3):
            board_frame = tk.Frame(game_frame, bg="#1e1e2e")
            board_frame.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)

            board_buttons = []
            for x in range(3):
                for y in range(3):
                    button = tk.Button(board_frame, text="", font=("Arial", 16, "bold"), width=4, height=2,
                                    bg="#5b4279", fg="red", activebackground="#5b4279", activeforeground="white",
                                    relief="flat", highlightthickness=0,)
                    button.grid(row=x, column=y, sticky="nsew", padx=2, pady=2)
                    button.config(command=lambda b=len(buttons), bx=x, by=y: on_click_handler(0, 0, b, bx, by))
                    button.bind("<Enter>", on_enter_classic)
                    button.bind("<Leave>", on_leave_advanced)
                    board_buttons.append(button)

            buttons.append(board_buttons)

    # Make the grid expand properly
    for i in range(3):
        game_frame.columnconfigure(i, weight=1)
        game_frame.rowconfigure(i, weight=1)
    
    if not player2_exists and not player1_turn:
        ultimate_ai_turn(20)

def on_click_ultimate(board, x, y):
    index = x * 3 + y
    # update_button_advanced(board, index, "x")
    global player1_turn, player2_exists,prev_board
    # Prevent clicking on an already occupied square
    if buttons[board][index].cget("text") != "":
        return

    # handle penalty shots. A penalty shot occurs when the board the next player was sent to is already won. they can choose to play anywhere 
    _, _, p1_boards_won, p2_boards_won = check_winner_ultimate()
    if prev_board in p1_boards_won or prev_board in p2_boards_won or (0 <= prev_board < 9 and all(button.cget("text") != "" for button in buttons[prev_board])):
        prev_board = 20

    # Turn handling logic
    if player1_turn and not player2_exists and (prev_board == 20 or board == prev_board):
        update_button_ultimate(board,index, str(user_symbol))
        player1_turn = False
        ultimate_ai_turn(index)  # Convert delay to milliseconds
    elif player1_turn and player2_exists and (prev_board == 20 or board == prev_board):
        update_button_ultimate(board,index, str(user_symbol))
        player1_turn = False
    elif player2_exists and not player1_turn and (prev_board == 20 or board == prev_board):
        update_button_ultimate(board,index, str(ai_symbol))
        player1_turn = True

    # Check if the gamestate is won
    winner, symbol,_,_ = check_winner_ultimate()
    if winner:
        win_screen_advanced(symbol)
    elif all(button.cget("text") != "" for row in buttons for button in row):  # Check for a draw
        draw_screen_classic()

def check_winner_ultimate():
    # need to update this function to actually add proper win checking 
    # i want this function to return more things 
    # it needs to return (True, symbol,p1_boards_won,p1_symbol,p2_boards_won_p2_symbol) if a player has won, where 'symbol' is the winning symbol
    # i think instead of return True, str(buttons[board][0].cget('text')) after an if check, it should add the board index to a list and then check if a 
    # user has won for example board 0,1,2 (horizontal rows) and what not
    """
    This function checks for a winner in the ultimate 3x3 Tic-Tac-Toe game.
    
    Returns:
        - (True, symbol,p1_boards_won,p2_boards_won) if a player has won, where 'symbol' is the winning symbol.
        - (False, "",p1_boards_won,p2_boards_won) if there is no winner yet.
    """
    global user_symbol, ai_symbol  # Ensure we access player symbols
    symbol = ""
    p1_boards_won = []  # List of boards won by player 1
    p2_boards_won = []  # List of boards won by player 2

    # Loop through each 3x3 grid (sub-grid) in buttons
    for board in range(9):  # We have 9 boards in the global buttons array
        # Check horizontal rows within each 3x3 grid
        if buttons[board][0].cget('text') == buttons[board][1].cget('text') == buttons[board][2].cget('text') and buttons[board][0].cget('text') == user_symbol:
            p1_boards_won.append(board)
        elif buttons[board][3].cget('text') == buttons[board][4].cget('text') == buttons[board][5].cget('text') and buttons[board][3].cget('text') == user_symbol:
            p1_boards_won.append(board)
        elif buttons[board][6].cget('text') == buttons[board][7].cget('text') == buttons[board][8].cget('text') and buttons[board][6].cget('text') == user_symbol:
            p1_boards_won.append(board)        
        elif buttons[board][0].cget('text') == buttons[board][1].cget('text') == buttons[board][2].cget('text') and buttons[board][0].cget('text') == ai_symbol:
            p2_boards_won.append(board)
        elif buttons[board][3].cget('text') == buttons[board][4].cget('text') == buttons[board][5].cget('text') and buttons[board][3].cget('text') == ai_symbol:
            p2_boards_won.append(board)
        elif buttons[board][6].cget('text') == buttons[board][7].cget('text') == buttons[board][8].cget('text') and buttons[board][6].cget('text') == ai_symbol:
            p2_boards_won.append(board)
        
        # Check vertical columns within each 3x3 grid
        elif buttons[board][0].cget('text') == buttons[board][3].cget('text') == buttons[board][6].cget('text') and buttons[board][0].cget('text') == user_symbol:
            p1_boards_won.append(board)
        elif buttons[board][1].cget('text') == buttons[board][4].cget('text') == buttons[board][7].cget('text') and buttons[board][1].cget('text') == user_symbol:
            p1_boards_won.append(board)
        elif buttons[board][2].cget('text') == buttons[board][5].cget('text') == buttons[board][8].cget('text') and buttons[board][2].cget('text') == user_symbol:
            p1_boards_won.append(board)
        elif buttons[board][0].cget('text') == buttons[board][3].cget('text') == buttons[board][6].cget('text') and buttons[board][0].cget('text') == ai_symbol:
            p2_boards_won.append(board)
        elif buttons[board][1].cget('text') == buttons[board][4].cget('text') == buttons[board][7].cget('text') and buttons[board][1].cget('text') == ai_symbol:
            p2_boards_won.append(board)
        elif buttons[board][2].cget('text') == buttons[board][5].cget('text') == buttons[board][8].cget('text') and buttons[board][2].cget('text') == ai_symbol:
            p2_boards_won.append(board)
        
        # Check diagonal lines within each 3x3 grid
        elif buttons[board][0].cget('text') == buttons[board][4].cget('text') == buttons[board][8].cget('text') and buttons[board][0].cget('text') == user_symbol:
            p1_boards_won.append(board)
        elif buttons[board][2].cget('text') == buttons[board][4].cget('text') == buttons[board][6].cget('text') and buttons[board][2].cget('text') == user_symbol:
            p1_boards_won.append(board)
        elif buttons[board][0].cget('text') == buttons[board][4].cget('text') == buttons[board][8].cget('text') and buttons[board][0].cget('text') == ai_symbol:
            p2_boards_won.append(board)
        elif buttons[board][2].cget('text') == buttons[board][4].cget('text') == buttons[board][6].cget('text') and buttons[board][2].cget('text') == ai_symbol:
            p2_boards_won.append(board)

    # check the boards that p1 has won 
    if 0 in p1_boards_won and 1 in p1_boards_won and 2 in p1_boards_won:
        symbol = user_symbol
    elif 3 in p1_boards_won and 4 in p1_boards_won and 5 in p1_boards_won:  
        symbol = user_symbol
    elif 6 in p1_boards_won and 7 in p1_boards_won and 8 in p1_boards_won:
        symbol = user_symbol
    elif 0 in p1_boards_won and 3 in p1_boards_won and 6 in p1_boards_won:
        symbol = user_symbol
    elif 1 in p1_boards_won and 4 in p1_boards_won and 7 in p1_boards_won:
        symbol = user_symbol
    elif 2 in p1_boards_won and 5 in p1_boards_won and 8 in p1_boards_won:
        symbol = user_symbol
    elif 0 in p1_boards_won and 4 in p1_boards_won and 8 in p1_boards_won:
        symbol = user_symbol
    elif 2 in p1_boards_won and 4 in p1_boards_won and 6 in p1_boards_won:
        symbol = user_symbol

    # check the boards that p2 has won 
    if 0 in p2_boards_won and 1 in p2_boards_won and 2 in p2_boards_won:
        symbol = ai_symbol
    elif 3 in p2_boards_won and 4 in p2_boards_won and 5 in p2_boards_won:  
        symbol = ai_symbol
    elif 6 in p2_boards_won and 7 in p2_boards_won and 8 in p2_boards_won:
        symbol = ai_symbol
    elif 0 in p2_boards_won and 3 in p2_boards_won and 6 in p2_boards_won:
        symbol = ai_symbol
    elif 1 in p2_boards_won and 4 in p2_boards_won and 7 in p2_boards_won:
        symbol = ai_symbol
    elif 2 in p2_boards_won and 5 in p2_boards_won and 8 in p2_boards_won:
        symbol = ai_symbol
    elif 0 in p2_boards_won and 4 in p2_boards_won and 8 in p2_boards_won:
        symbol = ai_symbol
    elif 2 in p2_boards_won and 4 in p2_boards_won and 6 in p2_boards_won:
        symbol = ai_symbol
    
    # if the symbol has not been set by this point, no winner yet, play continues 
    if symbol == "":
        return (False, "",p1_boards_won,p2_boards_won)
    else:
        return (True, symbol,p1_boards_won,p2_boards_won)

def ultimate_ai_turn(index):
    global player1_turn

    # Retrieve won boards
    _, _, p1_boards_won, p2_boards_won = check_winner_ultimate()
    won_boards = set(p1_boards_won + p2_boards_won)  # Combine both player's won boards

    # If the next board is won, pick a random valid board
    if index > 8 or index in won_boards:
        valid_boards = [b for b in range(9) if b not in won_boards and any(button.cget("text") == "" for button in buttons[b])]
        if not valid_boards:  # If no valid boards remain, AI has nowhere to play
            return
        index = random.choice(valid_boards)

    # Get all empty squares in the chosen board
    empty_squares = [i for i, button in enumerate(buttons[index]) if button.cget("text") == ""]

    if empty_squares:  # Ensure there are empty squares left
        ai_choice = random.choice(empty_squares)  # Pick a random empty square   
        update_button_ultimate(index, ai_choice, str(ai_symbol))
        player1_turn = True  # Give turn back to player

    # Check if the game state is won
    winner, symbol, _, _ = check_winner_ultimate()
    if winner:
        win_screen_advanced(symbol)
    elif all(button.cget("text") != "" for row in buttons for button in row):  # Check for a draw
        draw_screen_classic()

def update_button_ultimate(board, index, symbol):
    global prev_board
    prev_board = index
    white_symbol()
    buttons[board][index].config(text=symbol, fg="red")

def center_window(window):
    # call this to centre the window 
    window.update_idletasks()  # Ensure window dimensions are updated
    width = window.winfo_width()
    height = window.winfo_height()
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    window.geometry(f"{width}x{height}+{x}+{y}")



# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Foes")

#start the game at the splash screen
splash_screen()

# Start the event loop
root.mainloop()
