import tkinter
import random

WINDOW_BG = 'black'
CANVAS_BG = 'green'
TILE_SIZE = 16
LINE_COLOR = 'red'
FPS = 10
COLOR_SNAKE = 'red'
COLOR_FOOD = 'orange'
SECTION_COLOR = 'blue'

class App():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.attributes('-fullscreen', True)
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()

        self.window['bg'] = WINDOW_BG
        self.window.bind('<Key>', self.on_key) #на любую клавишу вызываем метод
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.width // TILE_SIZE * TILE_SIZE,
            height=self.height // TILE_SIZE * TILE_SIZE,
            bg=CANVAS_BG,
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        self.canvas.update()
        self.draw_lines()
        self.game = Game(self.canvas)

        self.window.mainloop()
    
    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()
        else:
            self.game.on_key(event)

    def draw_lines(self):
        for i in range(1, int(self.width // TILE_SIZE)):
            self.canvas.create_line(
                i * TILE_SIZE,
                0,
                i * TILE_SIZE,
                self.height,
                fill=LINE_COLOR
            )

        for i in range(1, int(self.height // TILE_SIZE)):
            self.canvas.create_line(
                0,
                i * TILE_SIZE,
                self.width,
                i * TILE_SIZE,
                fill=LINE_COLOR
            )

class Game:
    def __init__(self, canvas: tkinter.Canvas):
        self.canvas = canvas
        self.cols = self.canvas.winfo_width() // TILE_SIZE
        self.rows = self.canvas.winfo_height() // TILE_SIZE
        self.snake = Snake(
            self.cols // 2,
            self.rows // 2,
            self.canvas,
            "Up",
            "Down",
            "Right",
            "Left"
        )
        self.food = None
        self.update()
    

    def on_key(self, event: tkinter.Event) -> None:
        self.snake.on_key(event)

    #очки (сколько еды съела)

    def update(self):
        if not self.food:
            self.food = Food(
                self.canvas,
                random.randint(0, self.cols - 1),
                random.randint(0, self.rows - 1)
            )
            self.food.draw()
        self.snake.collide_borders()
        self.snake.eat_food(self)
        if self.snake.is_active:
            self.snake.move()
            self.canvas.after(1000 // FPS, self.update)
        self.snake.draw()

class Snake:
    def __init__(
            self,
            col: int,
            row: int,
            canvas: tkinter.Canvas,
            key_up: str,
            key_down: str,
            key_right: str,
            key_left: str
    ):
        self.col = col
        self.row = row
        self.canvas = canvas
        self.key_up = key_up
        self.key_down = key_down
        self.key_right = key_right
        self.key_left = key_left
        self.direction = (1, 0)
        self.max_col = self.canvas.winfo_width() // TILE_SIZE  - 1
        self.max_row = self.canvas.winfo_height() // TILE_SIZE  - 1
        self.tag = 'snake'
        self.body = []
        self.is_active = True



    def draw(self):
        self.canvas.delete(self.tag)
        for section in self.body:
            self.canvas.create_rectangle(
                section[0] * TILE_SIZE,
                section[1] * TILE_SIZE,
                section[0] * TILE_SIZE + TILE_SIZE,
                section[1] * TILE_SIZE + TILE_SIZE,
                fill=SECTION_COLOR,
                tags=self.tag
            )
        self.canvas.create_rectangle(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            self.col * TILE_SIZE + TILE_SIZE,
            self.row * TILE_SIZE + TILE_SIZE,
            fill=COLOR_SNAKE,
            tags=self.tag
        )
    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == self.key_right:
            self.change_direction((1, 0))
        if event.keysym == self.key_left:
            self.change_direction((-1, 0))
        if event.keysym == self.key_up:
            self.change_direction((0, -1))
        if event.keysym == self.key_down:
            self.change_direction((0, 1))

    def change_direction(self, direction):
        if self.direction[0] == direction[0] * -1:
            return
        if self.direction[1] == direction[1] * -1:
            return
        self.direction = direction

    def move(self):
        """движение змеи"""
        if self.body:
            self.body = [(self.col, self.row)] + self.body[:-1]
        self.col += self.direction[0]
        self.row += self.direction[1]

    def collide_borders(self):
        """проверяет столкновеня с границами холста"""
        if self.col == self.max_col:
            self.canvas['bg'] = 'yellow'
            self.is_active = False
        if self.col == 0:
            self.canvas['bg'] = 'yellow'
            self.is_active = False
        if self.row == 0:
            self.canvas['bg'] = 'yellow'
            self.is_active = False
        if self.row == self.max_row:
            self.canvas['bg'] = 'yellow'
            self.is_active = False
    
    def eat_food(self, game: Game):
        """здесь съедается еда и растет тело"""
        if self.col == game.food.col:
            if self.row == game.food.row:
                self.body.append((game.food.col, game.food.row))
                self.canvas.delete(game.food.tag)
                game.food = None
          

class Food:
    """Еда, которую поглощает змея"""
    def __init__(
        self,
        canvas: tkinter.Canvas,
        col: int,
        row: int,
    ):
        self.canvas = canvas
        self.col = col
        self.row = row
        self.tag = 'food'

    def draw(self):
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            self.col * TILE_SIZE + TILE_SIZE,
            self.row * TILE_SIZE + TILE_SIZE,
            fill=COLOR_FOOD,
            tags=self.tag
        )
App()