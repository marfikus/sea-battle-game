
import tkinter as tk
import random


class MainScreen:
    def __init__(self, settings, game, player):
        self.settings = settings
        # self.settings_screen = None
        # self.input_screen = None

        self.game = game
        self.player = player

        self.root = tk.Tk()
        self.root.title("Sea Battle")
        self.root.resizable(False, False)

        # self.mainmenu = tk.Menu(self.root)
        # self.root.config(menu=self.mainmenu)
        # self.mainmenu.add_command(label="New game", command=self.start_game)
        # self.mainmenu.add_command(label="Settings", command=self.show_settings)

        self.width = None
        self.height = None
        self.game_field = None
        self.c = None
        self.selected_cell = None


    def start_gui(self):
        map_margin = 30
        maps_gap = 40
        lines_margin = 10

        map_size = self.settings.cell_size * self.settings.map_dim
        self.width = (map_size * 2) + (map_margin * 2 + maps_gap)
        self.height = map_size + map_margin * 2

        self.c = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height, 
            bg=self.settings.colors["canvas_bg"]
        )
        self.c.pack()

        x = lines_margin
        y = lines_margin
        while x < self.width:
            if y < self.height:
                self.c.create_line(0, y, self.width, y, 
                    fill=self.settings.colors["canvas_lines"]
                )
                y += self.settings.cell_size

            self.c.create_line(x, 0, x, self.height, 
                fill=self.settings.colors["canvas_lines"]
            )
            x += self.settings.cell_size

        x1 = map_margin
        x2 = x1 + map_size
        y1 = map_margin
        y2 = y1 + map_size
        self.c.create_rectangle(x1, y1, x2, y2)
        x1 = x2 + maps_gap
        x2 = x1 + map_size
        self.c.create_rectangle(x1, y1, x2, y2)

        x1 = map_margin + map_size + maps_gap + 1
        x2 = x1 + self.settings.cell_size - 1
        y1 = map_margin + 1
        y2 = y1 + self.settings.cell_size - 1
        for y in range(self.settings.map_dim):
            for x in range(self.settings.map_dim):
                self.c.create_rectangle(x1, y1, x2, y2, 
                    fill="gray70", 
                    activefill="gray30",
                    width=0
                )
                x1 += self.settings.cell_size
                x2 = x1 + self.settings.cell_size - 1

            x1 = map_margin + map_size + maps_gap + 1
            x2 = x1 + self.settings.cell_size - 1
            y1 += self.settings.cell_size
            y2 = y1 + self.settings.cell_size - 1



        # self.game_is_active = True
        self.root.mainloop()


    def show_settings(self):
        # self.settings_screen.show()
        pass


    def click_cell(self, event):
        for cell in self.game_field.hided_cells:
            rect = self.game_field.hided_cells[cell]["screen_block"]["rect"]
            coords = self.c.coords(rect)
            if (coords[0] <= event.x <= coords[2]) and (coords[1] <= event.y <= coords[3]):
                # print(self.game_field.hided_cells[cell])
                self.selected_cell = cell
                self.c.itemconfig(rect, fill=self.settings.colors["cell_bg"]["selected"])
                self.input_screen.show(
                    self.game_field.hided_cells[cell]["input_value"]
                )
                break


    def change_cell_value(self, digit):
        rect = self.game_field.hided_cells[self.selected_cell]["screen_block"]["rect"]
        self.c.itemconfig(rect, fill=self.settings.colors["cell_bg"]["hided"])

        if digit is not None:
            text = self.game_field.hided_cells[self.selected_cell]["screen_block"]["text"]

            if digit == 0: # click Clear
                self.c.itemconfig(text, text="")
            else: # click digit
                self.c.itemconfig(text, text=digit)

            self.game_field.hided_cells[self.selected_cell]["input_value"] = digit
            y, x = self.game_field.hided_cells[self.selected_cell]["matrix_coords"]
            self.game_field.matrix[y][x] = digit

        if self.game_field.is_solved():
            print("Game solved!")

