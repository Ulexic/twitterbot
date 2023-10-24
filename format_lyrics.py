import re

lyrics_file = open("lyrics.csv", "a")

with open("lyrics.txt", "r") as file:
   lyrics = file.read()
   lyrics = re.sub("\n\n+", "\n\n", lyrics)

with open("lyrics.txt", "w") as file:
   file.write(lyrics + '\n')

with open("lyrics.txt", "r") as file:
   lyrics = file.readlines()
   added_lyrics = []
   res = ""
   for line in lyrics:
      if line == "\n":
         if res[:-1] in added_lyrics:
            res = ""
            continue
         lyrics_file.write("\n" + res[:-1])
         added_lyrics.append(res[:-1])
         res = ""
      else:
         res += line[:-1] + ";"

   # print(res[:-1])
   if res[:-1] not in added_lyrics:
      lyrics_file.write(res[:-1])
   lyrics_file.close()