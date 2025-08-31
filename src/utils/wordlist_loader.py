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
                