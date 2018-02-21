"""
This script assumes the following:
1. All of the names in your collection .csv are on the first column
2. All of those names are spelled correctly.
3. The .csv only contains cards that you have in your collection.
"""
import csv
import scrython
import time

# You can replace fileName here with your .csv file path if you only have one file.
fileName = input("Please enter the name of the file you'd like to scan: ")
searchQuery = input("Enter your Scryfall query: ")

search = scrython.cards.Search(q=searchQuery, page=1)

total = search.total_cards()

totalNames = []

for i in range(len(search.data())):
    totalNames.append(search.data()[i]['name'])

if total > len(search.data()):
    time.sleep(0.05)
    search2 = scrython.cards.Search(q=searchQuery, page=2)
    for i in range(len(search2.data())):
        totalNames.append(search.data()[i]['name'])

with open(fileName, 'r') as f:
    reader = csv.reader(f, delimiter=",")
    print("\nYou own of at least 1 copy of the following:\n")
    for value in reader:
        if value[0] in totalNames:
            print(value[0])
