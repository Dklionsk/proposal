def total(word):
    t = 0
    word = word.lower()
    for c in word:
        t += (ord(c) - ord('a') + 1)
    return t

for word in ['honeycomb', 'mjolnir', 'evernote', 'homesteaders']:
    print word, total(word)
