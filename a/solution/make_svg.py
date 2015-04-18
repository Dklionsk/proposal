import random

"""
In this puzzle, you're shown an image with a grid of dots.
There are three dot sizes, large, medium, and small.
The trick is that the dots are encoding a message, and the encoding is actually multiple layers deep.
It would be tedious to decipher the message by hand, so the best thing is to parse the SVG and convert
it into a simpler encoding.

The dots in the SVG represent morse code. A small dot is a dot, a big dot is a dash, and a tiny dot is a space.
The morse code decodes to letter names in the military alphabet.
The military alphabet decoded reads out a clue to the answer.

In this case, the clue is "android three oh", or Android 3.0, which is Honeycomb.
"""

letterNames = {
    'a': ('alpha',[0,1]),
    'b': ('bravo',[1,0,0,0]),
    'c': ('charlie',[1,0,1,0]),
    'd': ('delta',[1,0,0]),
    'e': ('echo',[0]),
    'f': ('foxtrot',[0,0,1,0]),
    'g': ('golf',[1,1,0]),
    'h': ('hotel',[0,0,0,0]),
    'i': ('india',[0,0]),
    'j': ('juliet',[0,1,1,1]),
    'k': ('kilo',[1,0,1]),
    'l': ('lima',[0,1,0,0]),
    'm': ('mike',[1,1]),
    'n': ('november',[1,0]),
    'o': ('oscar',[1,1,1]),
    'p': ('papa',[0,1,1,0]),
    'q': ('quebec',[1,1,0,1]),
    'r': ('romeo',[0,1,0]),
    's': ('sierra',[0,0,0]),
    't': ('tango',[1]),
    'u': ('uniform',[0,0,1]),
    'v': ('victor',[0,0,0,1]),
    'w': ('whiskey',[0,1,1]),
    'x': ('xray',[1,0,0,1]),
    'y': ('yankee',[1,0,1,1]),
    'z': ('zulu',[1,1,0,0]),
}

width = 600
height = 1100
largeRadius = 16
smallRadius = 8
extraSmallRadius = 4
margin = 20
lineHeight = 40
spacing = 40

color = '#000000'

#sequence = [random.randint(0, 2) for x in range(100)]

clue = 'androidthreeoh'
print clue
militaryClue = ''.join([letterNames[c][0] for c in clue])
print militaryClue
morseClue = [letterNames[c][1] for c in militaryClue]
print morseClue
finalClue = morseClue[0]
for clue in morseClue[1:]:
    finalClue = finalClue + [2] + clue
print finalClue

outfile = open('layers.svg', 'w')
outfile.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg width="%dpx" height="%dpx" version="1.1" xmlns="http://www.w3.org/2000/svg">\n<g fill="%s">\n' % (width, height, color))

x = margin
y = margin

for value in finalClue:
    if value == 1:
        radius = largeRadius
    elif value == 0:
        radius = smallRadius
    else:
        radius = extraSmallRadius
    
    if x + 2 * radius > width - margin:
        x = margin
        y += lineHeight
    outfile.write('<ellipse cx="%d" cy="%d" rx="%d" ry="%d"></ellipse>\n' % (x,y,radius,radius))
    x += spacing

outfile.write('</g>\n</svg>')