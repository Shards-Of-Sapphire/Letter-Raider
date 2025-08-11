import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk, ImageEnhance
import random
import threading
import time
import csv
import os
import sys

class HangmanGame:
    def load_words_from_csv(self, file_path, limit=20):
        try:
            # Get the directory of the running script/executable
            if getattr(sys, 'frozen', False):
                # Running as executable
                base_path = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            abs_file_path = os.path.join(base_path, file_path)
            
            # Create the words.csv file if it doesn't exist
            if not os.path.exists(abs_file_path):
                with open(abs_file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Add some default words
                    writer.writerow(['epiphany', 'The sudden realization'])
                    writer.writerow(['blueprint', 'Detailed technical drawing or plan'])
                    writer.writerow(['carousel', 'Rotating amusement park ride'])
                messagebox.showinfo("Info", "Created empty words.csv file. Please add your words!")
                return []
            
            words = []
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for enc in encodings:
                try:
                    with open(abs_file_path, newline='', encoding=enc) as csvfile:
                        reader = csv.reader(csvfile)
                        for row in reader:
                            if len(row) >= 2:
                                word, meaning = row[0].strip(), row[1].strip()
                                words.append((word.lower(), meaning))
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    messagebox.showerror("Error", f"Error reading words.csv: {str(e)}")
                    return []
            
            if not words:
                messagebox.showerror("Error", "No valid words found in words.csv")
                return []
            
            random.shuffle(words)
            return words[:limit]
        except Exception as e:
            messagebox.showerror("Error", f"Could not load words.csv: {str(e)}")
            return []
    

    def __init__(self, root):
        self.root = root
        self.root.title("Letter Raider")
        self.root.resizable(False, False)
        
        # Set window icon
        try:
            # Get the directory of the running script/executable
            if getattr(sys, 'frozen', False):
                # Running as executable
                base_path = os.path.dirname(sys.executable)
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(base_path, 'icon.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not set window icon: {str(e)}")


        self.word_list = self.load_words_from_csv("words.csv")
        self.guessed_letters = []

        self.load_images()
        self.setup_ui()
        self.new_game()

    def load_images(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            bg_path = os.path.join(script_dir, "images", "bg_retro.png")
            win_path = os.path.join(script_dir, "images", "win.png")
            
            original_bg = Image.open(bg_path).convert("RGBA").resize((800,600))
            enhancer = ImageEnhance.Brightness(original_bg)
            dimmed_bg = enhancer.enhance(0.8)  # Reduce brightness by 20%
            self.bg_image = ImageTk.PhotoImage(dimmed_bg)

            self.win_image_raw = Image.open(win_path).resize((450, 450))
            self.win_image = ImageTk.PhotoImage(self.win_image_raw)
        except FileNotFoundError as e:
            print(f"Error loading images: {e}")
            messagebox.showerror("Error", f"Could not find required image files. Please ensure 'bg_retro.png' and 'win.png' are in the images directory.")
            self.root.quit()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
        self.canvas.pack()
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        try:
            # Try to create a test label with the font to check if it's available
            test_label = tk.Label(self.root, font=("Press Start 2P", 10))
            test_label.pack_forget()  # Create but don't show it
            
            # If we got here without error, the font is available
            self.word_display = self.canvas.create_text(400, 100, text='', font=("Press Start 2P", 24), fill='white')
            self.hint_text = self.canvas.create_text(400, 150, text='', font=("Press Start 2P", 12), fill='white')
            button_font = ("Press Start 2P", 10)
            label_font = ("Press Start 2P", 12)
        except tk.TclError:
            # Font not available, use Arial as fallback
            print("Press Start 2P font not found, using Arial instead")
            self.word_display = self.canvas.create_text(400, 100, text='', font=("Arial", 24), fill='white')
            self.hint_text = self.canvas.create_text(400, 150, text='', font=("Arial", 12), fill='white')
            button_font = ("Arial", 10)
            label_font = ("Arial", 12)

        self.letter_buttons = {}
        x_start, y_start = 140, 450
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            x = x_start + (i % 13) * 40
            y = y_start + (i // 13) * 50
            btn = tk.Button(self.root, text=letter, font=button_font, bg="#FFCC00", fg="black",
                            command=lambda l=letter: self.check_letter(l))
            btn.place(x=x, y=y, width=35, height=35)
            self.letter_buttons[letter] = btn

        self.score_label = tk.Label(self.root, text="Score: 0", font=label_font, bg="black", fg="lime")
        self.game_title = tk.Label(self.root, text="Letter Raider", font=("Press Start 2P", 28, "bold"), bg="black", fg="gold")
        self.game_title.place(x=150, y=10)
        self.score_label.place(x=10, y=10)

        self.reset_button = tk.Button(self.root, text="New Game", font=button_font, bg="hot pink", fg="black",
                                      command=self.new_game)
        self.reset_button.place(x=650, y=20)

        self.timer_label = tk.Label(self.root, text="Time: 60", font=label_font, bg="black", fg="red")
        self.timer_label.place(x=10, y=50)

    def new_game(self):
        self.word, self.hint = random.choice(self.word_list)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.score = 0
        self.time_left = 60

        self.update_displayed_word()
        self.canvas.itemconfig(self.hint_text, text=f"Hint: {self.hint}")

        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL)

        self.score_label.config(text="Score: 0")
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.start_timer()
        self.canvas.delete("win_image")
        self.canvas.delete("confetti")

    def update_displayed_word(self):
        display = ' '.join([letter if letter.upper() in self.guessed_letters else '_' for letter in self.word.upper()])
        self.canvas.itemconfig(self.word_display, text=display)

    def check_letter(self, letter):
        self.letter_buttons[letter].config(state=tk.DISABLED)
        if letter.lower() in self.word:
            self.guessed_letters.append(letter)
            self.update_displayed_word()
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            if all(l.upper() in self.guessed_letters for l in self.word):
                self.win_game()
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses == 6:
                self.lose_game()

    def win_game(self):
        self.canvas.create_image(400, 200, image=self.win_image, tags="win_image")
        self.launch_confetti()
        messagebox.showinfo("You Win!", f"You guessed it! The word was '{self.word}'.")
        self.disable_all_buttons()
        self.time_left = 0
        self.save_score("Won")


    def lose_game(self):
        messagebox.showinfo("You Lost", f"The word was '{self.word}'. Try again!")
        self.disable_all_buttons()
        self.time_left = 0
        self.save_score("Lost")

    def save_score(self, result):
        try:
            with open("scores.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), self.word, result, self.score])
        except Exception as e:
            print(f"Error saving score: {e}")


    def disable_all_buttons(self):
        for btn in self.letter_buttons.values():
            btn.config(state=tk.DISABLED)

    def start_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.root.after(1000, self.start_timer)
        else:
            if all(l.upper() in self.guessed_letters for l in self.word):
                return  # Already won
            self.lose_game()

    def launch_confetti(self):
        colors = ["red", "yellow", "blue", "green", "purple", "orange"]
        for _ in range(100):
            x = random.randint(100, 700)
            y = random.randint(0, 400)
            size = random.randint(5, 10)
            color = random.choice(colors)
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=color, tags="confetti")

if __name__ == '__main__':
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
