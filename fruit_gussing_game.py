import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv

# here twinkter is the basics  builtin-library for the creating GUI
# PIL -> Python image Library, it is used for the opening, manipulating and saving
# various image file formats., Now days, pillow is used for this, mainly for the
# image processing and graphics design, and automated image
# Function to read fruits from a CSV file
def load_fruit_list(filename):
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            fruit_list = [row[0] for row in reader]  # Get the first column
            return fruit_list
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"The file '{filename}' was not found.")
        return []

# Load the fruit list from the CSV file
fruit_list = load_fruit_list('fruits.csv')
if not fruit_list:
    exit()  # Exit if the fruit list could not be loaded

selected_fruit = random.choice(fruit_list)  # Select a random fruit name

# Initialize variables
guessed_letters = ''
chances = len(selected_fruit) + 2

# Main GUI Class for the Game
class FruitGuessingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guess the Fruit!")
        self.geometry("500x500")

        # Initialize chances and word display
        self.remaining_chances = chances
        
        # Initialize the word display variable before calling the update function
        self.word_display_var = tk.StringVar()
        self.update_word_display()

        # Background image setup
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.update()  # Update to get the canvas dimensions
        self.setup_background()

        # Display word (with underscores)
        self.word_label = tk.Label(self, textvariable=self.word_display_var, font=("Arial", 24, "bold"), bg="#fce5cd")
        self.canvas.create_window(250, 150, window=self.word_label)

        # Entry box for guesses
        self.guess_entry = tk.Entry(self, font=("Arial", 14))
        self.canvas.create_window(250, 250, window=self.guess_entry)

        # Button for submitting guess
        self.guess_button = tk.Button(self, text="Guess", command=self.process_guess, font=("Arial", 14, "bold"), bg="#93c47d", fg="white")
        self.canvas.create_window(250, 300, window=self.guess_button)

        # Remaining chances display
        self.chances_label = tk.Label(self, text=f"Chances left: {self.remaining_chances}", font=("Arial", 14), bg="#fce5cd")
        self.canvas.create_window(250, 350, window=self.chances_label)

    def setup_background(self):
        """Setup the background image or default background color."""
        try:
            # Load and resize the background image
            bg_image = Image.open("background.jpg").resize((800, 800), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            # Calculate the center position for the background image
            canvas_center_x = int(self.canvas.winfo_width() / 2)
            canvas_center_y = int(self.canvas.winfo_height() / 2)

            # Adjust the position for centering the background image
            self.canvas.create_image(canvas_center_x, canvas_center_y, image=self.bg_photo, anchor="center")
        except FileNotFoundError:
            self.canvas.config(bg="lightblue")  # Default background color

    def update_word_display(self):
        """Update the word display with guessed letters and underscores."""
        display_text = " ".join([char if char in guessed_letters else "_" for char in selected_fruit])
        self.word_display_var.set(display_text)

    def process_guess(self):
        """Process the user's guess."""
        global guessed_letters
        guess = self.guess_entry.get().lower()

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return
        elif guess in guessed_letters:
            messagebox.showinfo("Already Guessed", "You've already guessed that letter.")
            return

        # Add to guessed letters and check for correctness
        guessed_letters += guess
        if guess in selected_fruit:
            self.update_word_display()
            if all([char in guessed_letters for char in selected_fruit]):
                messagebox.showinfo("Congratulations", f"Great job! You've guessed the fruit: {selected_fruit}")
                self.destroy()
        else:
            self.remaining_chances -= 1
            self.chances_label.config(text=f"Chances left: {self.remaining_chances}")
            if self.remaining_chances <= 0:
                messagebox.showinfo("Game Over", f"You've run out of chances. The fruit was: {selected_fruit}")
                self.destroy()

        # Clear the entry box after each guess
        self.guess_entry.delete(0, tk.END)

# Start the game
if __name__ == "__main__":
    app = FruitGuessingGame()
    app.mainloop()
