import tkinter as tk
import random

# Game settings
WIDTH = 500
HEIGHT = 500
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
BG_COLOR = "#000000"

# Color choices
SNAKE_COLORS = ["#00FF00", "#1ABC9C", "#3498DB", "#9B59B6", "#E74C3C"]
FOOD_COLORS = ["#FF0000", "#F39C12", "#E67E22", "#2ECC71", "#F1C40F"]

score = 0

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.color = random.choice(SNAKE_COLORS)

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.color = random.choice(FOOD_COLORS)
        self.food = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="food")

def next_turn(snake, food):
    global score, direction

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake.color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(WIDTH / 2, HEIGHT / 2 - 30, font=('consolas', 30), text=f"GAME OVER", fill="red")
    canvas.create_text(WIDTH / 2, HEIGHT / 2 + 10, font=('consolas', 20), text=f"Final Score: {score}", fill="white")

    restart_button.place(x=WIDTH / 2 - 50, y=HEIGHT / 2 + 50)

def restart_game():
    global snake, food, score, direction

    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")
    canvas.delete("all")
    restart_button.place_forget()

    snake = Snake()
    food = Food()
    next_turn(snake, food)

# GUI Setup
window = tk.Tk()
window.title("Snake Game - Upgraded!")
window.resizable(False, False)

direction = "down"

label = tk.Label(window, text=f"Score: {score}", font=("consolas", 16))
label.pack()

canvas = tk.Canvas(window, bg=BG_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

restart_button = tk.Button(window, text="Play Again", font=("consolas", 12), command=restart_game)

window.update()

snake = Snake()
food = Food()
next_turn(snake, food)

# Controls
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))

window.mainloop()
