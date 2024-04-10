#FIXME: последний ряд и колонна больше чем остальные

import tkinter

WINDOW_BG = 'black'
CANVAS_BG = 'green'
TILE_SIZE = 16
LINE_COLOR = 'red'
FPS = 10
COLOR_SNAKE = 'red'

class App():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.attributes('-fullscreen', True)
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.canvas_size = min((self.width, self.height))
        self.tiles_ammount = self.canvas_size // TILE_SIZE
        self.window['bg'] = WINDOW_BG
        self.window.bind('<Key>', self.on_key) #на любую клавишу вызываем метод
        self.canvas = tkinter.Canvas(self.window, width=self.canvas_size, height=self.canvas_size, bg=CANVAS_BG, highlightthickness=0)
        self.canvas.pack()
        self.canvas.update()
        self.draw_lines()
        self.game = Game(self.canvas, self.tiles_ammount)

        self.window.mainloop()
    
    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()
        else:
            self.game.on_key(event)

    def draw_lines(self):
        for i in range(1, int(self.tiles_ammount)):
            self.canvas.create_line(
                i * TILE_SIZE,
                0,
                i * TILE_SIZE,
                self.height,
                fill=LINE_COLOR
            )

        for i in range(1, int(self.tiles_ammount)):
            self.canvas.create_line(
                0,
                i * TILE_SIZE,
                self.width,
                i * TILE_SIZE,
                fill=LINE_COLOR
            )

class Game:
    def __init__(self, canvas: tkinter.Canvas, size: int):
        self.canvas = canvas
        self.size = size
        self.snake = Snake(self.size // 2, self.size // 2, TILE_SIZE, self.canvas, "Up", "Down", "Right", "Left")
        self.update()
    

    def on_key(self, event: tkinter.Event) -> None:
        self.snake.on_key(event)

    #очки (сколько еды съела)

    def update(self):
        self.canvas.delete('snake')
        self.snake.collide_borders()
        if self.snake.is_active:
            self.snake.move()
        self.snake.draw()
        self.canvas.after(1000 // FPS, self.update)

class Snake:
    def __init__(self, col: int, row: int, size: int, canvas: tkinter.Canvas, key_up: str, key_down: str,
        key_right: str,
        key_left: str
    ):
        self.col = col
        self.row = row
        self.size = size
        self.canvas = canvas
        self.key_up = key_up
        self.key_down = key_down
        self.key_right = key_right
        self.key_left = key_left
        self.direction = (1, 0)
        self.max_col = self.canvas.winfo_width() // TILE_SIZE
        self.max_row = self.canvas.winfo_height() // TILE_SIZE
        self.is_active = True

    def draw(self):
        self.canvas.create_rectangle(
            self.col * TILE_SIZE,
            self.row * TILE_SIZE,
            self.col * TILE_SIZE + self.size,
            self.row * TILE_SIZE + self.size,
            fill=COLOR_SNAKE,
            tags='snake'
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
        self.col += 1 * self.direction[0]
        self.row += 1 * self.direction[1]

    def collide_borders(self):
        """проверяет столкновеня с границами холста"""
        if self.col > self.max_col - 2:
            self.is_active = False
        

        

class Food:
    pass

App()