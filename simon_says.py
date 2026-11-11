import random
import tkinter as tk
from tkinter import messagebox, ttk


class SimonSays:
    MIN_GRID = 2
    MAX_GRID = 6

    def __init__(self, root):
        self.root = root
        self.root.title("Simon Says")
        self.root.configure(bg="#111318")
        self.root.resizable(False, False)

        self.palette = [
            "#ef5350", "#ec407a", "#ab47bc", "#7e57c2",
            "#5c6bc0", "#42a5f5", "#29b6f6", "#26c6da",
            "#26a69a", "#66bb6a", "#9ccc65", "#d4e157",
            "#ffca28", "#ffa726", "#ff7043", "#8d6e63",
            "#78909c", "#90a4ae", "#b0bec5", "#78909c",
            "#8e44ad", "#16a085", "#2980b9", "#d35400",
            "#c0392b", "#2c3e50", "#27ae60", "#f39c12",
            "#3498db", "#e74c3c", "#1abc9c", "#9b59b6",
        ]

        self.sequence = []
        self.player_index = 0
        self.score = 0
        self.grid_size = 3
        self.demo_running = False
        self.game_active = False
        self.buttons = []

        self.grid_var = tk.StringVar(value="3 x 3")
        self.speed_var = tk.StringVar(value="Normal")

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

    def add_setting(self, parent, label, variable, values, column):
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
            width=9,
        )
        combo.grid(row=0, column=column + 1, padx=(0, 8))
        combo.bind("<<ComboboxSelected>>", self.settings_changed)

    def create_grid(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()

        self.buttons.clear()
        self.grid_size = int(self.grid_var.get().split()[0])
        button_count = self.grid_size * self.grid_size

        for index in range(button_count):
            color = self.palette[index % len(self.palette)]
            button = tk.Button(
                self.grid_frame,
                bg=color,
                activebackground=self.lighten(color),
                activeforeground="#ffffff",
                relief="flat",
                bd=0,
                width=7 if self.grid_size <= 4 else 5,
                height=3 if self.grid_size <= 4 else 2,
                cursor="hand2",
                command=lambda cell=index: self.player_click(cell),
            )
            button.grid(
                row=index // self.grid_size,
                column=index % self.grid_size,
                padx=4 if self.grid_size <= 4 else 2,
                pady=4 if self.grid_size <= 4 else 2,
            )
            self.buttons.append(button)

    def settings_changed(self, _event=None):
        if not self.game_active:
            self.create_grid()

    def start_game(self):
        self.sequence = [random.randrange(self.grid_size * self.grid_size)]
        self.player_index = 0
        self.score = 0
        self.game_active = True
        self.demo_running = True

        self.update_score()
        self.start_button.config(state=tk.DISABLED)
        self.set_button_state(tk.DISABLED)
        self.status_label.config(text="Watch the sequence...")
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
            self.status_label.config(text="Your turn")
            return

        cell = self.sequence[step]
        button = self.buttons[cell]
        original = button.cget("background")
        button.config(bg=self.lighten(original))
        self.root.after(
            delay,
            lambda: self.restore_button(
                cell,
                original,
                lambda: self.root.after(
                    pause,
                    lambda: self.play_step(step + 1, delay, pause),
                ),
            ),
        )

    def restore_button(self, cell, color, callback):
        self.buttons[cell].config(bg=color)
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
            self.status_label.config(text=f"Level {self.score} complete!")
            self.sequence.append(random.randrange(self.grid_size * self.grid_size))
            self.demo_running = True
            self.set_button_state(tk.DISABLED)
            self.root.after(650, self.play_sequence)

    def game_over(self):
        self.game_active = False
        self.demo_running = False
        self.set_button_state(tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        messagebox.showinfo("Game Over", f"Final score: {self.score}")
        self.reset_game()

    def reset_game(self):
        self.sequence.clear()
        self.player_index = 0
        self.score = 0
        self.update_score()
        self.status_label.config(text="Choose your settings, then start a game.")
        self.set_button_state(tk.NORMAL)

    def highlight_delay(self):
        speed_delays = {"Slow": 720, "Normal": 520, "Fast": 340}
        return max(150, speed_delays[self.speed_var.get()] - self.score * 12)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def set_button_state(self, state):
        for button in self.buttons:
            button.config(state=state)

    @staticmethod
    def lighten(color):
        color = color.lstrip("#")
        red, green, blue = (
            int(color[index:index + 2], 16) for index in (0, 2, 4)
        )
        red = min(255, red + 55)
        green = min(255, green + 55)
        blue = min(255, blue + 55)
        return f"#{red:02x}{green:02x}{blue:02x}"


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
