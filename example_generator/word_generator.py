from random import choice


def word_generator(length):
    word = ''
    i = 0
    while i < length:
        word += choice('1234567890qwertyuiopasdfghjklzxcvbnm')
        i += 1
    return word
