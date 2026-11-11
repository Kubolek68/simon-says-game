import tkinter as tk
import unittest

from simon_says import SimonSays


class SimonSaysGridTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = SimonSays(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_all_supported_grid_sizes_create_the_expected_number_of_tiles(self):
        for size in range(self.game.MIN_GRID, self.game.MAX_GRID + 1):
            self.game.grid_var.set(f"{size} x {size}")
            self.root.update_idletasks()
            self.game.settings_changed()
            self.assertEqual(len(self.game.buttons), size * size)
            self.assertEqual(self.game.grid_size, size)
            self.assertEqual(
                self.game.grid_frame.winfo_width(),
                self.game.grid_frame.winfo_height(),
            )

    def test_random_mode_creates_a_new_sequence_with_one_more_step(self):
        self.game.grid_var.set("4 x 4")
        self.game.settings_changed()
        self.game.mode_var.set("Random sequence")
        self.game.sequence = [0, 1]
        self.game.score = 2
        self.game.extend_sequence()

        self.assertEqual(len(self.game.sequence), 3)
        self.assertNotEqual(self.game.sequence, [0, 1])


if __name__ == "__main__":
    unittest.main()
