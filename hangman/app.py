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
        print(f" / \ ")

# ======================================================

# function that takes a guess of a letter
def selector(word):
    # set length of word
    l = len(word)
    # set count of empty spots
    count = l
    # initial print
    print('_ ' * l)
    # https://stackoverflow.com/questions/10712002/create-an-empty-list-in-python-with-certain-size
    # set shadow list
    shadow = ['_'] * l
    # a list that will fill with guessed letters
    guessed = []
    # will increase each time guessed wrong
    x = 0
    # number of limbs on wordman
    limbs = 6

    # loop until it runs out of limbs
    while x < limbs and count > 0:
        # prints already guessed letters
        print(', '.join(guessed))
        # input a letter
        letter = input('Enter a letter: ')
        # append it to guessed
        guessed.append(letter)

        

        # if letter is in word
        if letter in word:
            # get location of letter in word in form of list
            # https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python
            location = [pos for pos, char in enumerate(word) if char == letter]
            lol = len(location)
            # for each location in list
            for i in location:
                # add letter to corisponding spot in shadow list
                shadow[i] = letter
                # drop down count of remaining letters
                count = count - 1
            


            print(' '.join(shadow))
            # print('')

            if count == 0:
                print("Success")

        # if letter is not in word
        else:
            # print filled out string
            print(' '.join(shadow))
            # increase number of wrong guesses
            x = x + 1
            # draw wordman
            doodle(x)
            # if game is over
            if x == 6:
                print('Wordman')
                print(f"Word was {word}")
        # tells you status
        print(f'Limbs is at {x}/{limbs} and Letter count is {l-count}/{l}')

    # https://stackoverflow.com/questions/12495218/using-user-input-to-call-functions

    # ask if you want to play again
    if input('Play again? (y/n): ') == 'y':
        # if yes it runs recursion of function
        selector(runner())
        # if not the function ends, thus the program ends


selector(the_word)





