import random
import tkinter as tk
from tkinter import ttk


class SimonSays:
    MIN_GRID = 2
    MAX_GRID = 6
    NORMAL_TILE = "#ffffff"
    HIGHLIGHT_TILE = "#ff0000"

    def __init__(self, root):
        self.root = root
        self.root.title("Simon Says")
        self.root.configure(bg="#111318")
        self.root.geometry("650x760")
        self.root.minsize(500, 600)
        self.root.resizable(True, True)

        self.sequence = []
        self.player_index = 0
        self.score = 0
        self.grid_size = 3
        self.demo_running = False
        self.game_active = False
        self.buttons = []

        self.grid_var = tk.StringVar(value="3 x 3")
        self.speed_var = tk.StringVar(value="Normal")
        self.mode_var = tk.StringVar(value="Classic")
        self.grid_var.trace_add("write", self.grid_selection_changed)

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="SIMON SAYS",
            font=("Segoe UI", 26, "bold"),
            fg="#f5f7fa",
            bg="#111318",
        )
        title.pack(pady=(22, 4))

        subtitle = tk.Label(
            self.root,
            text="Repeat the growing sequence",
            font=("Segoe UI", 10),
            fg="#9aa4b2",
            bg="#111318",
        )
        subtitle.pack(pady=(0, 14))

        settings = tk.Frame(self.root, bg="#111318")
        settings.pack(pady=(0, 12))

        self.add_setting(settings, "Grid", self.grid_var, [
            f"{size} x {size}" for size in range(self.MIN_GRID, self.MAX_GRID + 1)
        ], 0)
        self.add_setting(settings, "Speed", self.speed_var, [
            "Slow", "Normal", "Fast"
        ], 2)
        self.add_setting(settings, "Mode", self.mode_var, [
            "Classic", "Random sequence"
        ], 4, width=16)

        self.score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Segoe UI", 14, "bold"),
            fg="#dce3ed",
            bg="#111318",
        )
        self.score_label.pack(pady=(0, 12))

        self.grid_frame = tk.Frame(self.root, bg="#111318")
        self.grid_frame.pack(padx=18, pady=4)
        self.create_grid()

        self.status_label = tk.Label(
            self.root,
            text="Choose your settings, then start a game.",
            font=("Segoe UI", 10),
            fg="#9aa4b2",
            bg="#111318",
        )
        self.status_label.pack(pady=(14, 8))

        self.start_button = tk.Button(
            self.root,
            text="Start Game",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#315efb",
            activebackground="#5177ff",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=28,
            pady=11,
            cursor="hand2",
            command=self.start_game,
        )
        self.start_button.pack(pady=(0, 24))

    def add_setting(self, parent, label, variable, values, column, width=9):
        tk.Label(
            parent,
            text=f"{label}:",
            font=("Segoe UI", 10, "bold"),
            fg="#cbd5e1",
            bg="#111318",
        ).grid(row=0, column=column, padx=(8, 4))

        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly",
            width=width,
        )
        combo.grid(row=0, column=column + 1, padx=(0, 8))
        combo.bind("<<ComboboxSelected>>", self.settings_changed)

    def create_grid(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()

        self.buttons.clear()
        self.grid_size = int(self.grid_var.get().split()[0])
        button_count = self.grid_size * self.grid_size
        cell_size = self.cell_size()
        self.grid_frame.configure(
            width=self.grid_size * cell_size,
            height=self.grid_size * cell_size,
        )
        self.grid_frame.pack_propagate(False)

        for row in range(self.grid_size):
            self.grid_frame.grid_rowconfigure(row, minsize=cell_size, weight=0)
            self.grid_frame.grid_columnconfigure(row, minsize=cell_size, weight=0)

        for index in range(button_count):
            button = tk.Button(
                self.grid_frame,
                bg=self.NORMAL_TILE,
                activebackground=self.HIGHLIGHT_TILE,
                disabledforeground="#111318",
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                highlightthickness=3,
                highlightbackground="#111318",
                highlightcolor="#111318",
                width=1,
                height=1,
                cursor="hand2",
                command=lambda cell=index: self.player_click(cell),
            )
            button.grid(
                row=index // self.grid_size,
                column=index % self.grid_size,
                sticky="nsew",
                padx=3,
                pady=3,
            )
            self.buttons.append(button)

    def settings_changed(self, _event=None):
        if not self.game_active:
            self.create_grid()
            self.resize_for_grid()

    def grid_selection_changed(self, *_args):
        if not self.game_active and hasattr(self, "grid_frame"):
            self.root.after_idle(self.settings_changed)

    def resize_for_grid(self):
        grid_pixels = self.grid_size * self.cell_size()
        width = max(500, grid_pixels + 100)
        height = max(600, grid_pixels + 285)
        self.root.minsize(width, height)
        self.root.geometry(f"{width}x{height}")

    def cell_size(self):
        return max(58, 108 - (self.grid_size * 8))

    def start_game(self):
        self.sequence = [random.randrange(self.grid_size * self.grid_size)]
        self.player_index = 0
        self.score = 0
        self.game_active = True
        self.demo_running = True

        self.update_score()
        self.start_button.config(state=tk.DISABLED)
        self.set_button_state(tk.DISABLED)
        self.start_button.config(text="Game Running...")
        self.status_label.config(
            text="WATCH THE SEQUENCE",
            fg="#ff4d4d",
            font=("Segoe UI", 13, "bold"),
        )
        self.root.after(500, self.play_sequence)

    def play_sequence(self):
        if not self.game_active:
            return

        self.demo_running = True
        self.set_button_state(tk.DISABLED)
        delay = self.highlight_delay()
        pause = max(80, delay // 3)
        self.play_step(0, delay, pause)

    def play_step(self, step, delay, pause):
        if step >= len(self.sequence):
            self.demo_running = False
            self.player_index = 0
            self.set_button_state(tk.NORMAL)
            self.status_label.config(
                text="YOUR TURN",
                fg="#ffffff",
                font=("Segoe UI", 13, "bold"),
            )
            return

        cell = self.sequence[step]
        button = self.buttons[cell]
        button.config(
            bg=self.HIGHLIGHT_TILE,
            activebackground=self.HIGHLIGHT_TILE,
        )
        self.root.after(
            delay,
            lambda: self.restore_button(
                cell,
                lambda: self.root.after(
                    pause,
                    lambda: self.play_step(step + 1, delay, pause),
                ),
            ),
        )

    def restore_button(self, cell, callback):
        self.buttons[cell].config(
            bg=self.NORMAL_TILE,
            activebackground=self.HIGHLIGHT_TILE,
        )
        callback()

    def player_click(self, cell):
        if not self.game_active or self.demo_running:
            return

        if cell != self.sequence[self.player_index]:
            self.game_over()
            return

        self.player_index += 1
        if self.player_index == len(self.sequence):
            self.score += 1
            self.update_score()
            self.status_label.config(
                text=f"LEVEL {self.score} COMPLETE",
                fg="#7dff8a",
                font=("Segoe UI", 11, "bold"),
            )
            self.extend_sequence()
            self.demo_running = True
            self.set_button_state(tk.DISABLED)
            self.root.after(650, self.play_sequence)

    def game_over(self):
        self.game_active = False
        self.demo_running = False
        self.set_button_state(tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.start_button.config(text="Play Again")
        self.status_label.config(
            text=f"GAME OVER\nFinal score: {self.score}",
            fg="#ff4d4d",
            font=("Segoe UI", 15, "bold"),
        )

    def highlight_delay(self):
        speed_delays = {"Slow": 720, "Normal": 520, "Fast": 340}
        return max(150, speed_delays[self.speed_var.get()] - self.score * 12)

    def extend_sequence(self):
        length = self.score + 1
        cell_count = self.grid_size * self.grid_size

        if self.mode_var.get() == "Classic":
            self.sequence.append(random.randrange(cell_count))
            return

        old_sequence = self.sequence
        while True:
            new_sequence = [
                random.randrange(cell_count) for _ in range(length)
            ]
            if new_sequence != old_sequence:
                self.sequence = new_sequence
                return

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def set_button_state(self, state):
        for button in self.buttons:
            button.config(state=state)


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "TCombobox",
        fieldbackground="#20242c",
        background="#20242c",
        foreground="#111318",
        arrowcolor="#315efb",
    )
    SimonSays(root)
    root.mainloop()
