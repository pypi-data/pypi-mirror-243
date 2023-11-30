# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 23:44:27 2020

@author: JZST6G
"""

import os
import sys

path_parent = os.path.dirname(os.getcwd())
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, path_parent)

import mathstropy
from mathstropy.image_processing import load_image
from mathstropy.ml import decision_tree_model_training
from mathstropy import add_row

#test random word generator function
def randomword_tst():
    print('**************************************')
    print('randomword() testing...')
    word = ''
    word = mathstropy.randomword()
    if word != '':
        result = 'Passed'
    else:
        result = 'Failed'

    print('Description: Generate a random word.')
    print('Output:', word)
    print('Result:', result)

#test word mask function    
def wordmask_tst():
    print('**************************************')
    print('wordmask() testing...')
    word = 'mathstronauts'
    maskcounter = 0
    wordmasked = mathstropy.wordmask(word)
    for i in wordmasked:
        if i == '_':
            maskcounter+=1
    if maskcounter == 2:
        result = 'Passed'
    else:
        result = 'Failed'

    print('Description: Mask two letters in mathstronauts.')
    print('Output:', wordmasked)
    print('Result:', result)

#Execute unit testing
randomword_tst()
wordmask_tst()
print('**************************************')
          
