import os


bigwords = []
file = open("loremipsum.txt",'r')
for line.strip() in file:
    words = line.strip().split():
    for word in words:
        bigwords.append(word)
file.close()

