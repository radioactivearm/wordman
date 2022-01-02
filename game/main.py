import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QVBoxLayout, QWidget, QPushButton)

# ===============================================================

# pull straight from bash version of game

import pandas as pd
import numpy as np
import string

# reading csv into pandas df
words = pd.read_csv('../data/WikiWords.csv')

# smallest word
miniword = 3
# biggest word
maxiword = 21

# dropping all words under 3 letters
wordz = words.loc[words.name.str.len() >= miniword, :]
# wordz = wordz.loc[wordz.name.str.len() <= maxiword, :]
# # incase you want all the letters
# wordz = words.copy()

wordz = wordz.rename(columns={"name": "word"})

# ========================================================
# creating a dictionary of df's
# where each df is a different lenght
# of word
levels = {}

# end length
end = wordz.word.str.len().max() + 1 # grabbing this for down below

# start point
start = wordz.word.str.len().min() # grabbing this for down below

# loop over df and pull out smaller dfs
for i in range(start, end):
    df = wordz.loc[wordz.word.str.len() == i, :]
    levels[str(i)] = df.reset_index()

# ======================================================================

alphabet = list(string.ascii_lowercase)

# =========================================================================

#

# start button
class Start(QPushButton):

    def __init__(self):
        super(Start, self).__init__()

        self.setText('Start Game')

# enter
class Guess(QLineEdit):

    def __init__(self):
        super(Guess, self).__init__()

# the object for the _ _ _ _ display
class Display(QLabel):

    def __init__(self, text):
        super(Display, self).__init__()

        self.setText(text)

# object for the guessed letters
class Bucket(QLabel):

    def __init__(self, text):
        super(Bucket, self).__init__()

        self.setText(text)

class Hangman(QLabel):

   

    def __init__(self, limbs):
        super(Hangman, self).__init__()
        # the recipe for a wordman
        doods = [["", "", "", "", ""],
            ["", "('>')", "", "", ""], 
            ["", "('>')", "   |   ", "   |   ", ""],
            ["", "('>')", "--|  ", "   |   ", ""],
            ["", "('>')", "--|--", "   |   ", ""],
            ["", "('>')", "--|--", "   |   ", " /  "],
            ["", "('>')", "--|--", "   |   ", " / \ "],
            ["_|W|_", "('>')", "--|--", "   |   ", " / \ "]]
        self.setText('\n'.join(doods[limbs]))
        
# ["_|W|_", "('>')", "--|--", "  |  ", " / \ "]
        

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Wordman")


        layout = QVBoxLayout()

        self.man =layout.addWidget(Hangman(7))
        self.display = layout.addWidget(Display('_ _ _'))
        self.bucket = layout.addWidget(Bucket('a, b, c, d'))
        self.enter = layout.addWidget(Guess())
        layout.addWidget(Start())
        

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # writing a function to pull out a random word
    def wordman(number):
        df = levels[str(number)]
        length = df.word.count()
        windex = np.ceil(length*np.random.uniform(0,1,1))
        word = df.iloc[windex]
        return word.word.item()
    
    # fucntion that takes input and runs wordman
    def runner(self):
        length = 'Andy'
        while type(length) != int:
            self.enter.placeholderText((f'Enter a word length ({start}/{end-1}): '))
            length = self.enter.text()
            try:
                length = int(length)
            except:
                e = 2
        word = wordman(int(length))
        return word

    # function that takes a guess of a letter
    def selector(word):
        # set length of word
        l = len(word)
        # set count of empty spots
        count = l

        # https://stackoverflow.com/questions/10712002/create-an-empty-list-in-python-with-certain-size
        # set shadow list
        shadow = ['_'] * l
        # initial print
        print(' '.join(shadow))
        # a list that will fill with guessed letters
        guessed = []
        # will increase each time guessed wrong
        x = 0
        # number of limbs on wordman
        limbs = 6
        

        # easter egg hat happens randomly on 42
        randman = np.ceil(42*np.random.uniform(0,1,1))

        if randman == 42:
            limbs = 7

        # loop until it runs out of limbs
        while x < limbs and count > 0:
            # sorts the guess bin for ease of reading
            guessed.sort()
            # prints already guessed letters
            print(', '.join(guessed))
            # input a letter
            letter = '@'
            while letter.lower() not in alphabet or letter.lower() in guessed:
                letter = input('Enter a letter: ')

            print(' ')

            # append it to guessed
            guessed.append(letter.lower())

            

            # if letter is in word
            if letter.lower() in word:
                # get location of letter in word in form of list
                # https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python
                location = [pos for pos, char in enumerate(word) if char == letter.lower()]
                lol = len(location)
                # for each location in list
                for i in location:
                    # add letter to corisponding spot in shadow list
                    shadow[i] = letter.lower()
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
                if x == limbs:
                    print('Wordman')
                    print(f"Word was {word}")
            # tells you status
            print(f'{x}/{limbs}:{l-count}/{l}')


        # https://stackoverflow.com/questions/12495218/using-user-input-to-call-functions

        # ask if you want to play again
        if input('Play again? (y/n): ') == 'y':
            # if yes it runs recursion of function
            selector(runner())
            # if not the function ends, thus the program ends

   
app =  QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec())
