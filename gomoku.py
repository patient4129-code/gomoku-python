"""A small two-player Gomoku game built with Python's standard library."""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass, field
from tkinter import messagebox


BOARD_SIZE = 15
EMPTY = 0
BLACK = 1
WHITE = 2


@dataclass
class GomokuGame:
    """Store the board state and implement the rules independently of the UI."""

    size: int = BOARD_SIZE
    board: list[list[int]] = field(init=False)
    current_player: int = field(default=BLACK, init=False)
    winner: int = field(default=EMPTY, init=False)
    moves: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        if self.size < 5:
            raise ValueError("Board size must be at least 5")
        self.reset()

    def reset(self) -> None:
        self.board = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = BLACK
        self.winner = EMPTY
        self.moves = 0

    def place_stone(self, row: int, col: int) -> bool:
        """Place a stone. Return True when the move is legal and accepted."""
        if self.winner != EMPTY or not self.is_inside(row, col):
            return False
        if self.board[row][col] != EMPTY:
            return False

        player = self.current_player
        self.board[row][col] = player
        self.moves += 1

        if self._has_five(row, col, player):
            self.winner = player
        else:
            self.current_player = WHITE if player == BLACK else BLACK
        return True

    def is_inside(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    @property
    def is_draw(self) -> bool:
        return self.moves == self.size * self.size and self.winner == EMPTY

    def _has_five(self, row: int, col: int, player: int) -> bool:
        for row_step, col_step in ((1, 0), (0, 1), (1, 1), (1, -1)):
            count = 1
            count += self._count(row, col, row_step, col_step, player)
            count += self._count(row, col, -row_step, -col_step, player)
            if count >= 5:
                return True
        return False

    def _count(
        self,
        row: int,
        col: int,
        row_step: int,
        col_step: int,
        player: int,
    ) -> int:
        count = 0
        row += row_step
        col += col_step
        while self.is_inside(row, col) and self.board[row][col] == player:
            count += 1
            row += row_step
            col += col_step
        return count


class GomokuApp:
    """Tkinter desktop interface for a local two-player game."""

    CELL_SIZE = 40
    MARGIN = 30
    STONE_RADIUS = 16

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.game = GomokuGame()

        root.title("五子棋 · Gomoku")
        root.resizable(False, False)
        root.configure(bg="#f3e2b3")

        self.status = tk.StringVar()
        board_pixels = self.MARGIN * 2 + self.CELL_SIZE * (self.game.size - 1)

        top = tk.Frame(root, bg="#f3e2b3")
        top.pack(fill="x", padx=14, pady=(12, 4))
        tk.Label(
            top,
            textvariable=self.status,
            font=("Arial", 13, "bold"),
            bg="#f3e2b3",
            fg="#3d2b1f",
        ).pack(side="left")
        tk.Button(top, text="重新开始", command=self.restart, padx=12).pack(side="right")

        self.canvas = tk.Canvas(
            root,
            width=board_pixels,
            height=board_pixels,
            bg="#d9a95b",
            highlightthickness=1,
            highlightbackground="#704214",
        )
        self.canvas.pack(padx=14, pady=(4, 14))
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()
        self.update_status()

    def draw_board(self) -> None:
        self.canvas.delete("all")
        last = self.MARGIN + self.CELL_SIZE * (self.game.size - 1)
        for index in range(self.game.size):
            point = self.MARGIN + index * self.CELL_SIZE
            self.canvas.create_line(self.MARGIN, point, last, point, fill="#4f341d")
            self.canvas.create_line(point, self.MARGIN, point, last, fill="#4f341d")

        for row, col in ((3, 3), (3, 11), (7, 7), (11, 3), (11, 11)):
            x, y = self.to_canvas(row, col)
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#4f341d")

    def on_click(self, event: tk.Event) -> None:
        col = round((event.x - self.MARGIN) / self.CELL_SIZE)
        row = round((event.y - self.MARGIN) / self.CELL_SIZE)
        if not self.game.is_inside(row, col):
            return

        x, y = self.to_canvas(row, col)
        if abs(event.x - x) > self.CELL_SIZE / 2 or abs(event.y - y) > self.CELL_SIZE / 2:
            return

        player = self.game.current_player
        if not self.game.place_stone(row, col):
            return

        self.draw_stone(row, col, player)
        self.update_status()

        if self.game.winner:
            name = "黑棋" if self.game.winner == BLACK else "白棋"
            messagebox.showinfo("游戏结束", f"{name}获胜！")
        elif self.game.is_draw:
            messagebox.showinfo("游戏结束", "棋盘已满，本局平局。")

    def draw_stone(self, row: int, col: int, player: int) -> None:
        x, y = self.to_canvas(row, col)
        radius = self.STONE_RADIUS
        fill = "#151515" if player == BLACK else "#f5f5f5"
        outline = "#050505" if player == BLACK else "#777777"
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=fill,
            outline=outline,
            width=2,
        )

    def to_canvas(self, row: int, col: int) -> tuple[int, int]:
        return (
            self.MARGIN + col * self.CELL_SIZE,
            self.MARGIN + row * self.CELL_SIZE,
        )

    def update_status(self) -> None:
        if self.game.winner:
            name = "黑棋" if self.game.winner == BLACK else "白棋"
            self.status.set(f"{name}获胜")
        elif self.game.is_draw:
            self.status.set("平局")
        else:
            name = "黑棋" if self.game.current_player == BLACK else "白棋"
            self.status.set(f"当前回合：{name}")

    def restart(self) -> None:
        self.game.reset()
        self.draw_board()
        self.update_status()


def main() -> None:
    root = tk.Tk()
    GomokuApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
