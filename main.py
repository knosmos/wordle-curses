import curses, random
from curses import wrapper
words = open("words.txt","r").read().split("\n")

def writeWord(s, word, remark, y):
    for i, (letter, color) in enumerate(zip(word, remark)):
        s.addstr(y, i*2, letter.upper(), curses.color_pair({"c":2,"w":3,"n":7}[color]))

def score(guess, word):
    res = ""
    counts = [0]*26
    for i, c in enumerate(guess):
        counts[ord(c)-97] += 1
        if c == word[i]: res += "c" # correct spot
        elif c in word and word.count(c) >= counts[ord(c)-97]: res += "w" # wrong spot
        else: res += "n" # not in word
    return res

def render(s, guesses):
    s.clear()
    s.addstr(0, 0, "=== WORDLE ===", curses.color_pair(2))
    for i, (w, r) in enumerate(guesses): writeWord(s, w, r, i+2)

def run(s):
    word = random.choice(words)
    y = 2
    result = ""
    guesses = []
    while result != "ccccc" and len(guesses) < 6:
        render(s, guesses)
        guess = s.getstr(y, 0, 5).decode("u8").lower()
        if not(guess in words): continue
        result = score(guess, word)
        guesses.append([guess, result])
        y += 1
    render(s, guesses)
    s.addstr(y+1, 0, ["Genius!", "Unbelievable!", "Splendid!", "Amazing!", "Great!", "Good!", "No more tries"][len(guesses)])
    s.addstr(y+2, 0, "[esc] to quit, [enter] to play again", curses.color_pair(3))

def main(s):
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
    while True:
        curses.echo()
        run(s)
        curses.noecho()
        cont = s.getch()
        if cont == 27: break
wrapper(main)