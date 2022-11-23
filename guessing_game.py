# A simple guessing game

import random

LOWER_BOUND = 1
UPPER_BOUND = 20
MAX_NUM_OF_GUESSES = 10

print(f'Guess a number between {LOWER_BOUND} and {UPPER_BOUND}')

x = random.randint(LOWER_BOUND, UPPER_BOUND)

num_of_guesses = 0

while num_of_guesses < MAX_NUM_OF_GUESSES:
    g = int(input('Your guess: '))
    num_of_guesses += 1
    if g == x:
        print('Correct!')
        print(f'You found the number with {num_of_guesses} guesses')
        break
    elif g < x:
        print(f'The hidden number is larger than {g}')
    else:
        print(f'The hidden number is smaller than {g}')