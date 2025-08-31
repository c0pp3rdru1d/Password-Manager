import secrets
from generators.wordlists import wordlist_loader as wordlist_loader

def generate_passphrase(words, num_words=4, separator='-'):
    passphrase_words = [secrets.choice(words) for _ in range(num_words)]
    return separator.join(passphrase_words)


# Usage:
words = wordlist_loader.load_wordlist('eff_large_wordlist.txt') #Loads wordlist first
passphrase = generate_passphrase(words) # Generate a passphrase from words
print(passphrase) # Print the final result