import secrets

def load_wordlist(filename):
    words = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line: # Skip empty lines
                parts = line.split('\t')
                if len(parts) == 2:
                    number, word = parts
                    words.append(word)
    return words

def generate_passphrase(words, num_words=4, separator='-'):
    passphrase_words = [secrets.choice(words) for _ in range(num_words)]
    return separator.join(passphrase_words)


# Usage:
words = load_wordlist('eff_large_wordlist.txt')
print(generate_passphrase(words))
