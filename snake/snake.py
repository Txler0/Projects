import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

#game canvas   
canvas = tkinter.Canvas(window, bg = "black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
#format "(width)x(height)+(x)+(y)"
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")

#initialize snakes and food
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #this will create a singular tile for snake head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE) #snake food respectively
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
game_paused = False
on_main_menu = True
score = 0

def show_main_menu(event):
    global on_main_menu, game_over, game_paused, play_button, settings_button
    on_main_menu = True
    game_over = False
    game_paused = False
    print("show_main_menu")
    # Clear the canvas
    canvas.delete("all")
    
    # Draw the main menu options
    canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, font=("Arial", 24), text="Snake Game", fill="white")
    canvas.create_rectangle(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2, WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2 + 50, fill="gray")
    play_button = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 25, font=("Arial", 16), text="Play", fill="white")
    canvas.create_rectangle(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 70, WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2 + 120, fill="gray")
    settings_button = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 95, font=("Arial", 16), text="Settings", fill="white")
    
    # Bind the click events to the menu options
    canvas.tag_bind(play_button, "<Button-1>", start_game)
    canvas.tag_bind(settings_button, "<Button-1>", show_settings)
        
def start_game(event):
    global on_main_menu
    print("start_game")
    on_main_menu = False
    # Remove the menu options
    canvas.delete("all")
    
    # Start the game
    draw_snake()

def show_settings(event):
    global back_button
    # Remove the menu options
    canvas.delete("all")
    
    # Draw the settings menu
    canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, font=("Arial", 24), text="Settings", fill="white")
    canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font=("Arial", 16), text="Coming soon...", fill="white")
    canvas.create_rectangle(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 70, WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2 + 120, fill="gray")
    back_button = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 95, font=("Arial", 16), text="Back", fill="white")
    
    # Bind the click event to go back to the main menu
    canvas.tag_bind(back_button, "<Button-1>", show_main_menu)

def pause_game(e):
    global game_paused
    
    if e.keysym == "space":
        game_paused = True if not game_paused else False

def restart_game(event):
        global snake, snake_body, food, score, game_over, game_paused, on_main_menu, velocityX, velocityY
        print("restart_game")
        canvas.delete("all")
        snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
        snake_body = []
        food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
        score = 0
        velocityX = 0
        velocityY = 0   
        game_over = False
        game_paused = False
        on_main_menu = True
        show_main_menu(event=None)

def change_direction(e):
    # print(e)
    global velocityX, velocityY, game_over
    if (game_over):
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move_snake():
    global snake, game_over, food, snake_body, score
    if game_over:
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #collision check
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, (COLS-1)) * TILE_SIZE
        food.y = random.randint(0, (ROWS-1)) * TILE_SIZE
        score += 1

    #move the snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            previous_tile = snake_body[i-1]
            tile.x = previous_tile.x
            tile.y = previous_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def handle_key_release(event):
    change_direction(event)
    pause_game(event)

def draw_snake():
    global snake, snake_body, food, score, game_over, on_main_menu, game_paused, restart_button
    # print("draw_snake")
    if (not game_paused):
        move_snake()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if (game_paused and not game_over and not on_main_menu):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = ("Arial", 24), text = "Game Paused", fill = "white")

    if (game_over):
    #    print("Game Over")
       restart_button = canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = ("Arial", 24), text = f"       Game Over \n          Score: {score}\n Click here to restart!", fill = "white")
       canvas.tag_bind(restart_button, "<Button-1>", restart_game)
       return
    else:
        #TODO fix
        canvas.create_text(50, 20, font = ("Arial", 16), text = f"Score: {score}", fill = "white")

    canvas.create_text(WINDOW_WIDTH - 150, 20, font=("Arial", 11), text="Press space to pause the game", fill="white")

    window.after(100, draw_snake) # Add this line to continuously update the game state

    
show_main_menu(event= None)

window.bind("<KeyRelease>", handle_key_release)

window.mainloop()