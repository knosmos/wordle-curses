import curses, random
from curses import wrapper
words = open("words.txt","r").read().split("\n")
def writeWord(s, word, remark, y):
    s.addstr(y, 0, "│ │ │ │ │ │\n├─┼─┼─┼─┼─┤")
    for i, (letter, color) in enumerate(zip(word, remark)): s.addstr(y, i*2+1, letter.upper(), curses.color_pair({"c":2,"w":3,"n":7,"u":6}[color]))
def score(guess, word):
    res = [" "]*5
    counts = [0]*26
    for i, c in enumerate(guess):
        if c == word[i]:
            counts[ord(c)-97] += 1
            res[i] = "c" # correct spot
    for i, c in enumerate(guess):
        if c != word[i]:
            counts[ord(c)-97] += 1
            if c in word and word.count(c) >= counts[ord(c)-97]: res[i] = "w" # wrong spot
            else: res[i] = "n" # not in word
    return "".join(res)
def render(s, guesses):
    s.addstr(0, 0, "=== WORDLE ===", curses.color_pair(6))
    s.addstr(1, 0, "╭─┬─┬─┬─┬─╮")
    for i, (w, r) in enumerate(guesses): writeWord(s, w, r, i*2+2)
def getWord(s, y):
    word = ""
    while True:
        writeWord(s, word, "u"*len(word), y)
        k = s.getch()
        if chr(k) == "\b": word = word[:-1]
        elif k == 27: exit()
        elif chr(k) == "\n" and len(word) == 5: return word
        elif chr(k).isalpha() and len(word) < 5: word += chr(k)
def run(s):
    s.clear()
    word = random.choice(words)
    guesses = []
    while not(len(guesses)) or (guesses[-1][1] != "ccccc" and len(guesses) < 6):
        render(s, guesses)
        guess = getWord(s, len(guesses)*2+2).lower()
        if not(guess in words): continue
        guesses.append([guess, score(guess, word)])
    render(s, guesses)
    s.addstr(len(guesses)*2+2+1, 0, ["", "Genius!", "Unbelievable!", "Splendid!", "Amazing!", "Great!", "Good!", "No more tries - the word was "+word.upper()][len(guesses)+(guesses[-1][1]!="ccccc")])
    s.addstr(len(guesses)*2+2+2, 0, "[esc] to quit, [enter] to play again", curses.color_pair(3))
def main(s):
    for p in [(2,curses.COLOR_GREEN),(3,curses.COLOR_YELLOW),(7,curses.COLOR_WHITE),(6,curses.COLOR_CYAN)]: curses.init_pair(p[0], p[1], curses.COLOR_BLACK)
    while True:
        run(s)
        if s.getch() == 27: break
wrapper(main)