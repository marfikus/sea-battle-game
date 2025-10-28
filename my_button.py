
class MyButton:
    def __init__(self, canvas, x, y, text):
        self.c = canvas

        self.bt_text = self.c.create_text(x, y, text=text)

        text_coords = self.c.bbox(self.bt_text)
        x1 = text_coords[0] - 5
        x2 = text_coords[2] + 5
        y1 = y - 10
        y2 = y1 + 20
        self.bt_rect = self.c.create_rectangle(x1, y1, x2, y2, 
            width=1, 
            activefill="gray30", 
            stipple="gray25"
        )


    def bind(self, button, func):
        self.c.tag_bind(self.bt_rect, button, func)


    def update_and_show(self, text):
        self.c.itemconfig(self.bt_text, 
            text=text,
            state="normal"
        )

        text_coords = self.c.bbox(self.bt_text)
        rect_coords = self.c.coords(self.bt_rect)
        x1 = text_coords[0] - 5
        x2 = text_coords[2] + 5
        y1 = rect_coords[1]
        y2 = rect_coords[3]

        self.c.coords(self.bt_rect, x1, y1, x2, y2)
        self.c.itemconfig(self.bt_rect, state="normal")


    def hide(self):
        self.c.itemconfig(self.bt_text, state="hidden")
        self.c.itemconfig(self.bt_rect, state="hidden")


    def show(self):
        self.c.itemconfig(self.bt_text, state="normal")
        self.c.itemconfig(self.bt_rect, state="normal")


