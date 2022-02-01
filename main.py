import curses, random
words = open("words.txt","r").read().split("\n")
def writeWord(s, word, remark, y):
    s.addstr(y, 0, "│ │ │ │ │ │\n├─┼─┼─┼─┼─┤")
    for i, (letter, color) in enumerate(zip(word, remark)): s.addstr(y, i*2+1, letter.upper(), curses.color_pair({"c":2,"w":3,"n":7,"u":6}[color]))
def score(guess, word, alphabet):
    res = [" "]*5
    counts = [0]*26
    for i, c in enumerate(guess):
        if c == word[i]:
            counts[ord(c)-97] += 1
            res[i] = "c" # correct spot
            alphabet[ord(c)-97] = "c"
    for i, c in enumerate(guess):
        if c != word[i]:
            counts[ord(c)-97] += 1
            if c in word and word.count(c) >= counts[ord(c)-97]:
                res[i] = "w" # wrong spot
                if alphabet[ord(c)-97] != "c": alphabet[ord(c)-97] = "w"
            else:
                res[i] = "n" # not in word
                alphabet[ord(c)-97] = "n"
    return "".join(res), alphabet
def render(s, guesses, alphabet):
    s.addstr(0, 0, "=== WORDLE ===", curses.color_pair(2))
    for i, c in enumerate(alphabet): s.addstr(1+int(i//7), (i%7)*2, chr(65+i), curses.color_pair({"c":2,"w":3,"n":7,"u":6}[c]))
    s.addstr(6, 0, "╭─┬─┬─┬─┬─╮")
    for i, (w, r) in enumerate(guesses): writeWord(s, w, r, i*2+7)
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
    alphabet = ["u"]*26
    while not(len(guesses)) or (guesses[-1][1] != "ccccc" and len(guesses) < 6):
        render(s, guesses, alphabet)
        guess = getWord(s, len(guesses)*2+7).lower()
        if not(guess in words): continue
        res, alphabet = score(guess, word, alphabet)
        guesses.append([guess, res])
    render(s, guesses, alphabet)
    s.addstr(len(guesses)*2+6, 0, "╰─┴─┴─┴─┴─╯\n\n"+["", "Genius!", "Unbelievable!", "Splendid!", "Amazing!", "Great!", "Good!", "No more tries - the word was "+word.upper()][len(guesses)+(guesses[-1][1]!="ccccc")]+"\n[esc] to quit, [enter] to play again")
    if s.getch() == 27: exit()
def main(s):
    for p in [(2,curses.COLOR_GREEN),(3,curses.COLOR_YELLOW),(7,curses.COLOR_WHITE),(6,curses.COLOR_CYAN)]: curses.init_pair(p[0], p[1], curses.COLOR_BLACK)
    while True: run(s)
curses.wrapper(main)