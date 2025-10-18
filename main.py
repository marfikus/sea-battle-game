
from game import Game


def main():
    gui = None
    # cmd = input("Select version please (1 - console, 2 - gui): ")
    cmd = "2"
    if cmd == "1":
        gui = False
    elif cmd == "2":
        gui = True
    else:
        print("Unknown command!")
        return

    game = Game(gui)
    # game.start()


if __name__ == "__main__":
    main()

