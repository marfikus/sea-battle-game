
class Settings:
    def __init__(self):
        self.map_dim = 10 # размерность карты
        self.cell_size = 20 # размер ячейки карты

        self.colors = { # цвета, используемые в интерфейсе
            "canvas_bg": "gray70", # фон канваса
            "canvas_lines": "gray55", # 
            # "cell_bg": "gray70", # 
            # "active_cell_bg": "gray55", # 
            "cell_bg": {
                "default": "gray70", # 
                "selected": "gray55", # 
            },
        }



