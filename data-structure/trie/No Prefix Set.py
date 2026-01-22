#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'noPrefix' function below.
#
# The function accepts STRING_ARRAY words as parameter.
#

def noPrefix(words):
    # Write your code here
    END = "*"
    trie = {}

    for w in words:
        node = trie
        for ch in w:
            if END in node:  # an earlier word ends here => earlier word is prefix of w
                print("BAD SET")
                print(w)
                return
            node = node.setdefault(ch, {})
        # now we're at end of w
        if node:  # w is prefix of an earlier longer word OR duplicate (since node already has children)
            print("BAD SET")
            print(w)
            return
        if END in node:  # duplicate word
            print("BAD SET")
            print(w)
            return
        node[END] = True

    print("GOOD SET")

if __name__ == '__main__':
    n = int(input().strip())

    words = []

    for _ in range(n):
        words_item = input()
        words.append(words_item)

    noPrefix(words)
