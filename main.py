#FIXME: последний ряд и колонна больше чем остальные

import tkinter

WINDOW_BG = 'black'
CANVAS_BG = 'green'
TILE_SIZE = 20
LINE_COLOR = 'red'
FPS = 0

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
        self.draw_lines()
        self.window.mainloop()
    
    def on_key(self, event: tkinter.Event) -> None:
        if event.keysym == 'Escape':
            self.window.destroy()

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
    #очки (сколько еды съела)
    pass

class Snake:
    def __init__(self):
        #размер
        #место начала
        #направления движения
        pass

class Food:
    pass

App()