i = 1
too_long = []
with open('lyrics.csv', 'r') as f:
   lyrics = f.readline()
   while lyrics:
      if len(lyrics) > 280:
         too_long.append(lyrics)
         print(i)
      i += 1
      lyrics = f.readline()

print(too_long)