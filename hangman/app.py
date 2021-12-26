print('running ../hangman/app.py')

import pandas as pd
import numpy as np

# reading csv into pandas df
words = pd.read_csv('../data/WikiWords.csv')

# dropping all words under 3 letters
wordz = words.loc[words.name.str.len() > 2, :]

wordz = wordz.rename(columns={"name": "word"})

# ========================================================
# creating a dictionary of df's
# where each df is a different lenght
# of word
levels = {}

# end length
end = wordz.word.str.len().max() + 1

# start point
start = wordz.word.str.len().min() 

# loop over df and pull out smaller dfs
for i in range(start, end):
    df = wordz.loc[wordz.word.str.len() == i, :]
    levels[str(i)] = df.reset_index()

# =======================================================

 # writing a function to pull out a random word
def wordman(number):
    df = levels[str(number)]
    length = df.word.count()
    windex = np.ceil(length*np.random.uniform(0,1,1))
    word = df.iloc[windex]
    return word.word.item()

# =======================================================

# fucntion that takes input and runs wordman
def runner():
    length = input('Enter a word length: ')
    word = wordman(int(length))
    return word

# =======================================================

the_word = runner()
# print(the_word)

# ======================================================

# draws ascii stick figure

def doodle(limbs):
    if limbs > 0:
        print(f"('>')")
    if limbs == 3:
        print(f"--|")
    if limbs > 3:
        print(f"--|--")
    if limbs == 2:
        print(f"  |  ")
        print(f"  |  ")
    if limbs > 2:
        print(f"  |  ")
    if limbs == 5:
        print(f" /  ")
    if limbs > 5:
        print(f" /\ ")

# ======================================================

# function that takes a guess of a letter
def selector(word):
    l = len(word)
    count = l
    print('_ ' * l)
    # https://stackoverflow.com/questions/10712002/create-an-empty-list-in-python-with-certain-size
    shadow = ['_'] * l
    guessed = []
    x = 0
    limbs = 6
    while x < limbs and count > 0:
        print(', '.join(guessed))
        # print('')
        letter = input('Enter a letter: ')
        guessed.append(letter)

        # https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python
        if letter in word:
            location = [pos for pos, char in enumerate(word) if char == letter]
            lol = len(location)
            for i in location:
                shadow[i] = letter
                count = count - 1
            
            print(' '.join(shadow))
            # print('')
        else:

            print(' '.join(shadow))
            # print('')
            x = x + 1
            doodle(x)
            if x == 6:
                print('Wordman')
        print(f'Limbs is at {x}/{limbs} and Letter count is {count}/{l}')

    # https://stackoverflow.com/questions/12495218/using-user-input-to-call-functions

    if input('Play again? (y/n): ') == 'y':
        selector(runner())


selector(the_word)





