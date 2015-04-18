from bs4 import BeautifulSoup
import math
import random

random.seed(1)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def getTransform(g):
    transformString = g['transform']
    start = transformString.find('(')
    comma = transformString.find(',')
    end = transformString.find(')')
    x = float(transformString[start+1:comma])
    y = float(transformString[comma+2:end])
    return (x,y)

def formatTime((h,m,s)):
    return '%02d:%02d:%08.5f' % (h, m, s)

def timeDifference((h1,m1,s1), (h2,m2,s2)):
    t1 = s1 + m1 * 60 + h1 * 3600
    t2 = s2 + m2 * 60 + h2 * 3600
    return t1 - t2

# Convert speed of sound to miles per second
speed_of_sound = 761.207 / (60 * 60)

# Read all locations from the SVG so that we can change the SVG and rebuild the puzzle easily.
svg = BeautifulSoup(open('solution-map.svg'))

listening_stations_group = svg.find(id='Listening-stations').contents[1]
(x,y) = getTransform(listening_stations_group)
stations = listening_stations_group.find_all('ellipse')
stations = map(lambda station: (station['id'], ((float(station['cx']) + x) / 100, (float(station['cy']) + y) / 100)), stations)

print 'Listening Stations'
char_index = 'A'
for station in stations:
    station_name = station[0].replace('-',' ')
    print '%s. %s (%f, %f)' % (char_index, station_name, station[1][0], station[1][1])
    char_index = chr(ord(char_index) + 1)

print '\n761.207 mph\n'

all_letters_group = svg.find(id='Letters').contents[1]
(x,y) = getTransform(all_letters_group)
letter_groups = all_letters_group.find_all('g')
letters = []
for letter_group in letter_groups:
    letter = letter_group['id']
    (x2,y2) = getTransform(letter_group)
    circles = letter_group.find_all('circle')
    circles = sorted(map(lambda circle: (circle['id'], ((float(circle['cx']) + x + x2) / 100, (float(circle['cy']) + y + y2) / 100)), circles))
    letters.append((letter, circles))
letters = letters[::-1]

original_points = []
original_strike_times = []
all_time_offsets = []
all_times_heard = []
hour = 0
minute = 0
second = 0
for letter in letters:
    minute = random.randint(0, 30)
    second = random.randint(0, 59)
    for coord in letter[1]:
        time_offsets = []
        times_heard = []
        (lx,ly) = coord[1]
        original_points.append((lx, ly))
        original_strike_times.append((hour, minute, second))
        for station in stations:
            (sx, sy) = station[1]
            d = math.sqrt((sx - lx) * (sx - lx) + (sy - ly) * (sy - ly))
            time_offset = d / speed_of_sound
            time_offsets.append(time_offset)

            second_heard = second + time_offset
            minute_heard = minute
            if second_heard >= 60:
                second_heard -= 60
                minute_heard = minute + 1
            times_heard.append((hour, minute_heard, second_heard))

        all_time_offsets.append(time_offsets)
        all_times_heard.append(times_heard)

        second += max(time_offsets) + random.randint(1, 10)
        if second >= 60:
            second -= 60
            minute += 1
    hour += 1

(ax, ay) = stations[0][1]
(bx, by) = stations[1][1]
(cx, cy) = stations[2][1]
(dx, dy) = stations[3][1]

print 'Thunder times'
print '\tA\tB\tC\tD'
for i in range(len(original_strike_times)):
    time_offsets = all_time_offsets[i]
    times_heard = all_times_heard[i]

    ta = times_heard[0]
    tb = times_heard[1]
    tc = times_heard[2]
    td = times_heard[3]

    print '%d\t%s\t%s\t%s\t%s' % (i+1, formatTime(ta), formatTime(tb), formatTime(tc), formatTime(td))

print '\nSolution locations and strike times'
for i in range(len(original_points)):
    strike_time = original_strike_times[i]
    (lx, ly) = original_points[i]
    print '%d\t(%f,%f)\t%s' % (i+1, lx, ly, formatTime(strike_time))

