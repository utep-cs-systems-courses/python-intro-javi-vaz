#! /usr/bin/env python3

import os, stat
from sys import stderr, argv
from collections import OrderedDict

infile=argv[1]
outfile=argv[2]
word_count = {}

def populateWordDic():
    fd = os.open(infile, os.O_RDONLY, stat.S_IRWXU);
    assert fd >= 0
    word = ""
    char = os.read(fd,1).decode()
    while len(char) >0:
        if char.isalpha():
            word = word + char
        else:
            if word:
                word = word.lower()
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            word = ""
        char = os.read(fd,1).decode()
    os.close(fd)

def countWords():
    populateWordDic()
    
    if len(word_count)== 0:
        os.write(2,"No words found\n".encode())
        return
    ordered_words = OrderedDict(sorted(word_count.items()))
    fd = os.open(outfile, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRWXU);
    for key in ordered_words:
        os.write(fd, f"{key} {word_count[key]}\n".encode())

countWords()
