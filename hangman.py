import random
import os

# ASCII art for the 7 stages (0 to 6 incorrect guesses)
HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ========="""
]

# Default fallback list if words.txt is not found
FALLBACK_WORDS = [
    "PYTHON", "DEVELOPER", "ALGORITHM", "VARIABLE", 
    "FUNCTION", "DATABASE", "TERMINAL", "KEYBOARD"
]

def load_words(filename="words.txt"):
    """Loads words from a text file, or falls back to a default list."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            words = [line.strip().upper() for line in f if line.strip().isalpha()]
            if words:
                return words
    return FALLBACK_WORDS

def display_game_state(secret_word, guessed_letters, incorrect_guesses):
    """Displays the ASCII gallows, current word progress, and guessed letters."""
    print("\n" + "=" * 40)
    print(HANGMAN_PICS[len(incorrect_guesses)])
    print("=" * 40)
    
    # Generate masked word (e.g., '_ A _ H E O N')
    masked_display = " ".join([char if char in guessed_letters else "_" for char in secret_word])
    print(f"\nWord: {masked_display}\n")
    
    # Display guessed letter information
    wrong_display = ", ".join(sorted(incorrect_guesses)) if incorrect_guesses else "None"
    print(f"Incorrect guesses ({len(incorrect_guesses)}/6): {wrong_display}")
    print(f"All guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
    print("-" * 40)

def get_player_guess(all_guesses):
    """Prompts the user for a valid single-letter guess."""
    while True:
        guess = input("Enter a letter: ").strip().upper()
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single alphabetical letter.")
        elif guess in all_guesses:
            print(f"You already guessed '{guess}'. No penalty applied.")
        else:
            return guess

def play_hangman():
    """Main game loop."""
    word_list = load_words()
    secret_word = random.choice(word_list)
    secret_letters = set(secret_word)
    
    guessed_letters = set()
    incorrect_guesses = set()
    max_mistakes = 6

    print("\n*** WELCOME TO HANGMAN ***")

    while len(incorrect_guesses) < max_mistakes:
        display_game_state(secret_word, guessed_letters, incorrect_guesses)
        
        # Check victory condition
        if secret_letters.issubset(guessed_letters):
            print("\n" + "*" * 40)
            print("🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"You correctly revealed the word: {secret_word}")
            print("*" * 40 + "\n")
            return

        guess = get_player_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_letters:
            print(f"\nGood job! '{guess}' is in the word.")
        else:
            incorrect_guesses.add(guess)
            remaining = max_mistakes - len(incorrect_guesses)
            print(f"\nSorry, '{guess}' is not in the word. Remaining attempts: {remaining}")

    # Defeat screen if mistakes reach 6
    display_game_state(secret_word, guessed_letters, incorrect_guesses)
    print("\n" + "#" * 40)
    print("💀 GAME OVER! YOU LOST! 💀")
    print(f"The correct word was: {secret_word}")
    print("#" * 40 + "\n")

if __name__ == "__main__":
    while True:
        play_hangman()
        replay = input("Play again? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thanks for playing!")
            break