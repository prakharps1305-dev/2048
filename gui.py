"""Tkinter GUI for the 2048 engine in game.py, with an optional expectimax bot.

Game logic lives in game.py and bot.py; this file only draws and drives it.
"""

import tkinter as tk

from game import move_up, move_down, move_left, move_right, spawn, is_game_over
from bot import best_move

# Tile colours keyed by value; brighter/warmer as the value grows.
TILE_COLOURS = {
    0:    ("#cdc1b4", "#cdc1b4"),
    2:    ("#eee4da", "#776e65"),
    4:    ("#ede0c8", "#776e65"),
    8:    ("#f2b179", "#f9f6f2"),
    16:   ("#f59563", "#f9f6f2"),
    32:   ("#f67c5f", "#f9f6f2"),
    64:   ("#f65e3b", "#f9f6f2"),
    128:  ("#edcf72", "#f9f6f2"),
    256:  ("#edcc61", "#f9f6f2"),
    512:  ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}
# Anything above 2048 falls back to this.
SUPER_COLOUR = ("#3c3a32", "#f9f6f2")

BG_COLOUR = "#bbada0"
BOT_INTERVAL_MS = 200


def tile_style(value):
    return TILE_COLOURS.get(value, SUPER_COLOUR)


def font_for(value):
    size = 32
    if value >= 1024:
        size = 22
    elif value >= 128:
        size = 26
    return ("Helvetica", size, "bold")


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.board = [[0] * 4 for _ in range(4)]
        self.bot_on = False
        self._bot_job = None

        # Top bar: highest tile + bot toggle.
        top = tk.Frame(root, bg=BG_COLOUR)
        top.pack(fill="x", padx=10, pady=(10, 0))

        self.high_label = tk.Label(top, text="Highest: 0", font=("Helvetica", 14, "bold"),
                                   bg=BG_COLOUR, fg="#f9f6f2")
        self.high_label.pack(side="left", padx=6, pady=6)

        self.bot_button = tk.Button(top, text="Bot: OFF", font=("Helvetica", 12, "bold"),
                                    command=self.toggle_bot)
        self.bot_button.pack(side="right", padx=6, pady=6)

        self.status_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"),
                                     bg=BG_COLOUR, fg="#776e65")
        self.status_label.pack(fill="x", padx=10)

        # Grid of tiles.
        grid = tk.Frame(root, bg=BG_COLOUR)
        grid.pack(padx=10, pady=10)
        self.cells = []
        for r in range(4):
            row_cells = []
            for c in range(4):
                cell = tk.Frame(grid, width=100, height=100, bg=TILE_COLOURS[0][0])
                cell.grid(row=r, column=c, padx=5, pady=5)
                cell.grid_propagate(False)
                label = tk.Label(cell, text="", bg=TILE_COLOURS[0][0],
                                 font=font_for(0))
                label.place(relx=0.5, rely=0.5, anchor="center")
                row_cells.append(label)
            self.cells.append(row_cells)

        # Arrow keys.
        root.bind("<Up>", lambda e: self.handle_move(move_up))
        root.bind("<Down>", lambda e: self.handle_move(move_down))
        root.bind("<Left>", lambda e: self.handle_move(move_left))
        root.bind("<Right>", lambda e: self.handle_move(move_right))

        spawn(self.board)
        spawn(self.board)
        self.draw()

    def draw(self):
        highest = 0
        for r in range(4):
            for c in range(4):
                value = self.board[r][c]
                highest = max(highest, value)
                bg, fg = tile_style(value)
                label = self.cells[r][c]
                label.master.config(bg=bg)
                label.config(text=str(value) if value else "",
                             bg=bg, fg=fg, font=font_for(value))
        self.high_label.config(text=f"Highest: {highest}")

    def apply_move(self, move):
        """Run a move; spawn only if the board actually changed. Returns True if changed."""
        new_board = move(self.board)
        if new_board != self.board:
            self.board = new_board
            spawn(self.board)
            return True
        return False

    def handle_move(self, move):
        # Ignore manual input while the bot is driving or the game is over.
        if self.bot_on or is_game_over(self.board):
            return
        self.apply_move(move)
        self.draw()
        self.check_game_over()

    def check_game_over(self):
        if is_game_over(self.board):
            self.status_label.config(text="Game Over")
            self.stop_bot()
            return True
        return False

    def toggle_bot(self):
        if self.bot_on:
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        if is_game_over(self.board):
            return
        self.bot_on = True
        self.bot_button.config(text="Bot: ON")
        self.bot_step()

    def stop_bot(self):
        self.bot_on = False
        self.bot_button.config(text="Bot: OFF")
        if self._bot_job is not None:
            self.root.after_cancel(self._bot_job)
            self._bot_job = None

    def bot_step(self):
        if not self.bot_on:
            return
        if self.check_game_over():
            return
        move = best_move(self.board)
        if move is not None:
            self.apply_move(move)
            self.draw()
        if self.check_game_over():
            return
        self._bot_job = self.root.after(BOT_INTERVAL_MS, self.bot_step)


def main():
    root = tk.Tk()
    root.configure(bg=BG_COLOUR)
    Game2048(root)
    root.mainloop()


if __name__ == "__main__":
    main()
