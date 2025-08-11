import random
import csv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global score variable
score = 0

class HangmanGame:
    def __init__(self):
        self.word_list = self.load_words_from_csv("words.csv")
        if not self.word_list:
            print("Using default word list as words.csv not found")
            self.word_list = fallback_words
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.score = 0
        self.time_left = 60
        self.current_word = None
        self.current_hint = None

    def load_words_from_csv(self, file_path, limit=20):
        words = []
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for enc in encodings:
            try:
                with open(file_path, newline='', encoding=enc) as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) >= 2:
                            word, meaning = row[0], row[1]
                            words.append((word.lower(), meaning))
                break
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                print(f"Error: Could not find {file_path}")
                return []
        random.shuffle(words)
        return words[:limit]

    def new_game(self):
        if not self.word_list:
            print("No words available! Please check your words.csv file.")
            return False
            
        self.current_word, self.current_hint = random.choice(self.word_list)
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.score = 0
        self.time_left = 60
        return True

    def check_letter(self, letter):
        if letter.lower() in self.guessed_letters:
            return False
            
        self.guessed_letters.append(letter.lower())
        if letter.lower() not in self.current_word:
            self.wrong_guesses += 1
        return True

    def get_display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.current_word])

    def is_game_over(self):
        return self.wrong_guesses >= 6 or all(letter in self.guessed_letters for letter in self.current_word)

    def get_score(self):
        return self.score

    def get_time_left(self):
        return self.time_left

    def update_score(self, points):
        self.score += points

# Default word list if words.csv is not found
words_with_hints = {
    'breeze': 'A light and gentle wind 🌬️',
    'canvas': 'Used by painters to create art 🎨',
    'crystal': 'A shiny, transparent mineral 💎',
    'elegant': 'Graceful and stylish ✨',
    'meadow': 'A field full of grass and flowers 🌼',
    'twilight': 'Time between sunset and darkness 🌆',
    'guitar': 'A string instrument 🎸',
    'shadow': 'It follows you but isn’t alive 🕶️',
    'island': 'Land surrounded by water 🏝️',
    'whisper': 'A soft spoken word or sound 🤫',
    'abyss': 'a deep chasm',
    'epiphany': 'A sudden realization'
}

# Create a fallback word list from dictionary if CSV fails
fallback_words = [(word, hint) for word, hint in words_with_hints.items()]

# Hangman stages (ASCII Art)

# Hangman stages (ASCII Art)
stages = [
    """
     _______
    |/      |
    |
    |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |
    |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |       |
    |       |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|
    |       |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |      /
    |___
    """,
    """
     _______
    |/      |
    |      (_)
    |      \\|/
    |       |
    |      / \\
    |___
    """
]

# Main game function
def hangman():
    print(Fore.CYAN + Style.BRIGHT + "\nWelcome to Hangman Game! \n")
    print(Fore.YELLOW + "Rules:")
    print("1. Guess the word letter by letter")
    print("2. You have 6 chances to guess wrong")
    print("3. Each correct letter gives you points")
    print("4. Complete the word to win!")
    print("\n" + Fore.GREEN + "Let's play!")

    game = HangmanGame()
    
    while True:
        if not game.new_game():
            print("No words available. Exiting game.")
            break
        
        print("\n" + Fore.YELLOW + f"Hint: {game.current_hint}")
        print("\n" + Fore.CYAN + f"Word: {game.get_display_word()}")
        print(Fore.MAGENTA + f"\nScore: {game.get_score()}")
        print(Fore.RED + f"Wrong guesses: {game.wrong_guesses}/6")
        print(stages[game.wrong_guesses])
        
        while not game.is_game_over():
            guess = input(Fore.WHITE + "\nGuess a letter: ").lower()
            
            if len(guess) != 1 or not guess.isalpha():
                print(Fore.RED + "Please enter a single letter!")
                continue
                
            if not game.check_letter(guess):
                print(Fore.YELLOW + "You already guessed that letter!")
                continue
                
            if guess in game.current_word:
                print(Fore.GREEN + f"Good guess! {guess} is in the word!")
                game.update_score(10)
                
                if all(letter in game.guessed_letters for letter in game.current_word):
                    print(Fore.GREEN + "\nCongratulations! You won!")
                    print(Fore.CYAN + f"The word was: {game.current_word}")
                    print(Fore.MAGENTA + f"Final Score: {game.get_score()}")
                    break
                    
            else:
                print(Fore.RED + f"Sorry, {guess} is not in the word.")
                print(Fore.RED + f"Wrong guesses: {game.wrong_guesses}/6")
                print(stages[game.wrong_guesses])
                
        play_again = input(Fore.WHITE + "\nPlay again? (yes/no): ").lower()
        if play_again != 'yes':
            print(Fore.GREEN + "\nThanks for playing! Goodbye!")
            break

# Run the game
if __name__ == "__main__":
    hangman()
