
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
        self.c = None
        self.selected_cell = None
        self.lb_state = None
        self.bt_fire_text = None
        self.bt_fire_rect = None


    def start_gui(self):
        map_margin = 50
        maps_gap = 60
        lines_margin = 10

        map_size = self.settings.cell_size * self.settings.map_dim
        self.width = (map_size * 2) + (map_margin * 2 + maps_gap)
        self.height = map_size + map_margin * 2 + 20

        self.c = tk.Canvas(
            self.root, 
            width=self.width, 
            height=self.height, 
            bg=self.settings.colors["canvas_bg"]
        )
        self.c.pack()

        # add lines
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

        # add maps borders
        x1 = map_margin
        x2 = x1 + map_size
        y1 = map_margin
        y2 = y1 + map_size
        self.c.create_rectangle(x1, y1, x2, y2)
        self.player.own_map.screen_coords = {
            "x1": x1, "y1": y1, "x2": x2, "y2": y2
        }
        x1 = x2 + maps_gap
        x2 = x1 + map_size
        self.c.create_rectangle(x1, y1, x2, y2)
        self.player.opponent_map.screen_coords = {
            "x1": x1, "y1": y1, "x2": x2, "y2": y2
        }

        # add letter-digit lines
        letters = None
        if self.settings.language == "EN":
            letters = self.settings.LETTERS_EN
        elif self.settings.language == "RU":
            letters = self.settings.LETTERS_RU

        m1_x = self.player.own_map.screen_coords["x1"]
        m1_y = self.player.own_map.screen_coords["y1"]
        m1_x_letter = m1_x - self.settings.cell_size / 2
        m1_y_letter = m1_y + self.settings.cell_size / 2
        m1_x_digit = m1_x + self.settings.cell_size / 2
        m1_y_digit = m1_y - self.settings.cell_size / 2

        m2_x = self.player.opponent_map.screen_coords["x1"]
        m2_y = self.player.opponent_map.screen_coords["y1"]
        m2_x_letter = m2_x - self.settings.cell_size / 2
        m2_y_letter = m2_y + self.settings.cell_size / 2
        m2_x_digit = m2_x + self.settings.cell_size / 2
        m2_y_digit = m2_y - self.settings.cell_size / 2

        for i in range(self.settings.map_dim):
            if i == len(letters):
                print("Letters is over!")
                break

            letter = self.c.create_text(
                m1_x_letter, 
                m1_y_letter, 
                text=letters[i], 
                justify=tk.CENTER
            )
            digit = self.c.create_text(
                m1_x_digit, 
                m1_y_digit, 
                text=i + 1, 
                justify=tk.CENTER
            )
            m1_y_letter += self.settings.cell_size
            m1_x_digit += self.settings.cell_size

            letter = self.c.create_text(
                m2_x_letter, 
                m2_y_letter, 
                text=letters[i], 
                justify=tk.CENTER
            )
            digit = self.c.create_text(
                m2_x_digit, 
                m2_y_digit, 
                text=i + 1, 
                justify=tk.CENTER
            )
            m2_y_letter += self.settings.cell_size
            m2_x_digit += self.settings.cell_size

        # add cells borders
        # for own map:
        m1_x1 = map_margin + 1
        m1_x2 = m1_x1 + self.settings.cell_size - 1
        # for opponent map:
        m2_x1 = map_margin + map_size + maps_gap + 1
        m2_x2 = m2_x1 + self.settings.cell_size - 1

        y1 = map_margin + 1
        y2 = y1 + self.settings.cell_size - 1
        for y in range(self.settings.map_dim):
            for x in range(self.settings.map_dim):
                rect = self.c.create_rectangle(m1_x1, y1, m1_x2, y2, 
                    fill=self.settings.colors["cell_bg"]["default"], 
                    width=0
                )
                self.player.own_map.map[y][x].screen_block = rect
                m1_x1 += self.settings.cell_size
                m1_x2 = m1_x1 + self.settings.cell_size - 1

                rect = self.c.create_rectangle(m2_x1, y1, m2_x2, y2, 
                    fill=self.settings.colors["cell_bg"]["default"], 
                    width=0
                )
                self.player.opponent_map.map[y][x].screen_block = rect
                m2_x1 += self.settings.cell_size
                m2_x2 = m2_x1 + self.settings.cell_size - 1

            m1_x1 = map_margin + 1
            m1_x2 = m1_x1 + self.settings.cell_size - 1

            m2_x1 = map_margin + map_size + maps_gap + 1
            m2_x2 = m2_x1 + self.settings.cell_size - 1
            y1 += self.settings.cell_size
            y2 = y1 + self.settings.cell_size - 1

        # add ships to own map
        for ship in self.player.own_map.ships:
            x = ship.parts[0].map_x
            y = ship.parts[0].map_y
            rect = self.player.own_map.map[y][x].screen_block
            coords = self.c.coords(rect)
            x1 = coords[0] - 1
            y1 = coords[1] - 1

            x = ship.parts[-1].map_x
            y = ship.parts[-1].map_y
            rect = self.player.own_map.map[y][x].screen_block
            coords = self.c.coords(rect)
            x2 = coords[2]
            y2 = coords[3]

            self.c.create_rectangle(x1, y1, x2, y2,
                # fill="gray60",
                # width=1
            )
            ship.screen_coords = {
                "x1": x1, "y1": y1, "x2": x2, "y2": y2
            }

        self.c.bind("<Button-1>", self.click_cell)

        # add label state
        map_coords = self.player.own_map.screen_coords
        x1 = map_coords["x1"] + (map_size / 2)
        y1 = map_coords["y2"] + 30
        self.lb_state = self.c.create_text(
            x1, y1, 
            text="Your step"
        )

        # add button fire
        map_coords = self.player.opponent_map.screen_coords
        x1 = map_coords["x1"] + (map_size / 2)
        y1 = map_coords["y2"] + 30
        self.bt_fire_text = self.c.create_text(x1, y1, text="")

        text_coords = self.c.bbox(self.bt_fire_text)
        x1 = text_coords[0] - 5
        x2 = text_coords[2] + 5
        y1 = map_coords["y2"] + 20
        y2 = y1 + 20
        self.bt_fire_rect = self.c.create_rectangle(x1, y1, x2, y2, 
            width=1, 
            activefill="gray30", 
            stipple="gray25"
        )

        self.hide_bt_fire()
        self.c.tag_bind(self.bt_fire_rect, "<Button-1>", self.fire)

        # self.game_is_active = True
        self.root.mainloop()


    def update_bt_fire(self, text):
        self.c.itemconfig(self.bt_fire_text, 
            text=text,
            state="normal"
        )

        text_coords = self.c.bbox(self.bt_fire_text)
        rect_coords = self.c.coords(self.bt_fire_rect)
        x1 = text_coords[0] - 5
        x2 = text_coords[2] + 5
        y1 = rect_coords[1]
        y2 = rect_coords[3]

        self.c.coords(self.bt_fire_rect, x1, y1, x2, y2)
        self.c.itemconfig(self.bt_fire_rect, state="normal")


    def hide_bt_fire(self):
        self.c.itemconfig(self.bt_fire_text, state="hidden")
        self.c.itemconfig(self.bt_fire_rect, state="hidden")


    def show_bt_fire(self):
        self.c.itemconfig(self.bt_fire_text, state="normal")
        self.c.itemconfig(self.bt_fire_rect, state="normal")


    def fire(self, event):
        if self.selected_cell is None:
            return
        print(self.coords_to_code(self.selected_cell.y, self.selected_cell.x))


    def click_cell(self, event):
        map_coords = self.player.opponent_map.screen_coords
        if event.x < map_coords["x1"] or event.x > map_coords["x2"] or \
         event.y < map_coords["y1"] or event.y > map_coords["y2"]:
            return

        # print(event)

        if self.selected_cell is not None:
            rect = self.selected_cell.screen_block
            coords = self.c.coords(rect)
            if (coords[0] <= event.x <= coords[2]) and \
             (coords[1] <= event.y <= coords[3]):
                self.c.itemconfig(rect, 
                    fill=self.settings.colors["cell_bg"]["default"]
                )
                self.selected_cell = None
                self.hide_bt_fire()
                return

        for y in range(self.settings.map_dim):
            for x in range(self.settings.map_dim):
                cell = self.player.opponent_map.map[y][x]
                if cell.content is not None:
                    continue
                rect = cell.screen_block
                coords = self.c.coords(rect)
                if (coords[0] <= event.x <= coords[2]) and \
                 (coords[1] <= event.y <= coords[3]):
                    # print(y, x)
                    if self.selected_cell is not None:
                        self.c.itemconfig(self.selected_cell.screen_block, 
                            fill=self.settings.colors["cell_bg"]["default"]
                        )

                    self.selected_cell = cell
                    self.c.itemconfig(rect, 
                        fill=self.settings.colors["cell_bg"]["selected"]
                    )
                    code = self.coords_to_code(
                        self.selected_cell.y, 
                        self.selected_cell.x
                    )
                    self.update_bt_fire(f"Fire to {code}")

                    break


    def coords_to_code(self, y, x):
        letters = None
        if self.settings.language == "EN":
            letters = self.settings.LETTERS_EN
        elif self.settings.language == "RU":
            letters = self.settings.LETTERS_RU

        return f"{letters[y]}{x + 1}"


