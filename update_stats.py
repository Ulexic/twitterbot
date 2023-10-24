import csv
import json
import sys


def get_number_of_lyrics():
   with open('lyrics.csv', "r") as file:
      reader = csv.reader(file, delimiter=';')
      lyrics = list(reader)
   return len(lyrics)

def reset_stats():
   size = get_number_of_lyrics()
   lyricOccurence = []
   latest = []

   for i in range(size):
      lyricOccurence.append(0)

   for i in range(24):
      latest.append(0)

   stats ={
      "averageOccurence": 0,
      "latest": latest,
      "lyricOccurence": lyricOccurence,
      "max": 0,
      "totalOccurence": 0
   }

   with open('stats.json', "w") as file:
      json.dump(stats, file, indent=3)

def updtate_stats():
   with open('stats.json', "r") as file:
      stats = json.load(file)

   size = get_number_of_lyrics()

   while len(stats['lyricOccurence']) < size:
      stats['lyricOccurence'].append(0)

   stats['averageOccurence'] = stats['totalOccurence'] / size

   with open('stats.json', "w") as file:
      json.dump(stats, file, indent=3, separators=(',', ': '))

def main():
   if sys.argv[1] == "-u":
      updtate_stats()
   elif sys.argv[1] == "-r":
      reset_stats()
   
if __name__ == "__main__":
   main()