import tkinter as tk
import random
from collections import deque
import os

class SnakeGame:
    def __init__(self, master, width=400, height=400, size=20):
        self.master = master
        self.master.title("Snake Game")
        self.width = width
        self.height = height
        self.size = size
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.ai_snake = [(200, 200), (210, 200), (220, 200)]
        self.direction = "Right"
        self.food = self.create_food()
        self.paused = False

        # Create a top bar with restart, pause, and score label
        self.top_bar = tk.Frame(self.master, bg="#ecf0f1")  # Light grey color
        self.top_bar.pack(fill=tk.X, padx=10, pady=5)

        self.restart_button = tk.Button(self.top_bar, text="Restart", command=self.restart_game, padx=10, bg="#2ecc71", fg="white", relief=tk.FLAT)
        self.restart_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.top_bar, text="Pause", command=self.toggle_pause, padx=10, bg="#e74c3c", fg="white", relief=tk.FLAT)
        self.pause_button.pack(side=tk.LEFT)

        self.master.bind("<Key>", self.on_key_press)
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.update()

    def create_food(self):
        x = random.randint(0, (self.width - self.size) // self.size) * self.size
        y = random.randint(0, (self.height - self.size) // self.size) * self.size
        return x, y

    def draw_snake(self, snake, color):
        for segment in snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill=color)

    def draw_food(self):
        x, y = self.food
        self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill="#e74c3c")  # Red color

    def move(self):
        self.move_snake(self.snake, self.direction)
        self.move_ai_snake()

        if self.check_collision():
            self.handle_game_over()
        else:
            self.canvas.delete("all")
            self.draw_snake(self.snake, "#2ecc71")  # Green color
            self.draw_snake(self.ai_snake, "orange")  # Orange color
            self.draw_food()
            self.master.after(150, self.update)  # Increase the time delay

    def move_snake(self, snake, direction):
        x, y = snake[0]
        if direction == "Up":
            y -= self.size
        elif direction == "Down":
            y += self.size
        elif direction == "Left":
            x -= self.size
        elif direction == "Right":
            x += self.size
        new_head = (x, y)
        snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.create_food()
        else:
            snake.pop()

    def move_ai_snake(self):
        # AI Snake follows the path to the food using breadth-first search
        start = self.ai_snake[0]
        goal = self.food
        path = self.bfs(start, goal)

        if path:
            next_position = path[-1]
            if len(path) > 1:
                direction = self.get_direction(self.ai_snake[0], next_position)
                self.move_snake(self.ai_snake, direction)

                # Check if AI snake has collided with player snake
                if self.ai_snake[0] in self.snake:
                    self.reset_ai_snake()

                # Check if AI snake has eaten the food
                elif self.ai_snake[0] == self.food:
                    self.food = self.create_food()

    def reset_ai_snake(self):
        # Reset AI snake to its initial state
        self.ai_snake = [(200, 200), (210, 200), (220, 200)]

    def bfs(self, start, goal):
        queue = deque([(start, [])])
        visited = set()

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path + [current]

            if current not in visited:
                visited.add(current)
                neighbors = self.get_neighbors(current)
                for neighbor in neighbors:
                    queue.append((neighbor, path + [current]))

        return []

    def get_neighbors(self, position):
        x, y = position
        neighbors = [
            ((x + self.size) % self.width, y),  # Right
            ((x - self.size) % self.width, y),  # Left
            (x, (y + self.size) % self.height),  # Down
            (x, (y - self.size) % self.height)   # Up
        ]
        return neighbors

    def get_direction(self, current, next_position):
        x1, y1 = current
        x2, y2 = next_position

        if x1 < x2:
            return "Right"
        elif x1 > x2:
            return "Left"
        elif y1 < y2:
            return "Down"
        elif y1 > y2:
            return "Up"

    def check_collision(self):
        return (
            self.snake[0] in self.snake[1:] or
            self.snake[0] in self.ai_snake or
            self.snake[0][0] < 0 or self.snake[0][0] >= self.width or
            self.snake[0][1] < 0 or self.snake[0][1] >= self.height
        )

    def update(self):
        if not self.paused:
            self.move()

    def handle_game_over(self):
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="Game Over!", fill="white", font=("Helvetica", 16)
        )

    def on_key_press(self, event):
        key = event.keysym
        if key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.direction = "Right"

    def restart_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.ai_snake = [(200, 200), (210, 200), (220, 200)]
        self.direction = "Right"
        self.food = self.create_food()
        self.paused = False
        self.pause_button.config(text="Pause")  # Reset the Pause button text
        self.canvas.delete("all")  # Clear the canvas
        self.update()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume", bg="#3498db")  # Blue color
        else:
            self.pause_button.config(text="Pause", bg="#e74c3c")  # Red color
            self.update()


if __name__ == "__main__":
    root = tk.Tk()
    snake_game = SnakeGame(root)
    root.mainloop()
