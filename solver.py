words = open("words.txt").read().split("\n")

def partition(word, words):
    # Get how many words will remain for each possible response
    partitions = []
    for a in "MCW":
        for b in "MCW":
            for c in "MCW":
                for d in "MCW":
                    for e in "MCW":
                        partitions.append(len(reduce(word, a+b+c+d+e, words)))
    return partitions

def reduce(word, result, words):
    # word: 5-letter word (lowercase)
    # result: 5-letter str consisting of M, C, W (misplaced, correct, wrong)
    res = words[:]
    for i, s in enumerate(result):
        nres = []
        for w in res:
            if s == "M":
                if w[i] != word[i] and word[i] in w: nres.append(w)
            if s == "C":
                if w[i] == word[i]: nres.append(w)
            if s == "W":
                if w[i] != word[i]:
                    if not(word[i] in w) or word.count(word[i]) > 1:
                        nres.append(w)
        res = nres
    return res

print("WORDLE SOLVER")
print("=============")
# First guess is precomputed
opt = "raise"
result = ""
while result != "CCCCC":
    print(opt)
    result = input("> ").upper()
    words = reduce(opt, result, words)
    opt = ""
    opt_size = float("inf")
    for word in words:
        p = partition(word, words)
        avg_partition_size = sum(p)/len(p)
        if opt_size > avg_partition_size:
            opt_size = avg_partition_size
            opt = word
        # print(p)