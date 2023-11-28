#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 13:03:12 2021

@author: Jakob Lass

Tool to replace batch in order to fully port development to windows
"""

import os,sys,shutil

DIR = str(os.path.dirname(__file__))

try:
    os.remove(os.path.join('Tutorials','tutorialList.txt'))
except FileNotFoundError:
    pass

files = [f.path for f in os.scandir(DIR) if f.is_file()]

for f in files:
    if not f[-2:] == 'py':
        continue
    if 'tutorials.py' in f:
        continue
    os.system('python '+f)

    
    

for folder in ['.cache','.pyteste_cache','__pycache']:
    try:
        shutil.rmtree(os.path.join(DIR,folder))
    except FileNotFoundError:
        pass


# Generate correct tutorials.rst file
tutorialFile = os.path.join('docs','Tutorials','Tutorials.rst')

mainText = """.. _Tutorials:

Tutorials
---------
Main text about the tutorials below..

.. toctree::
   :maxdepth: 1
"""

with open(os.path.join('Tutorials','tutorialList.txt'),'r') as f:
    tutorials = f.readlines()
            
tutorialText = []
for tut in tutorials:
    common = os.path.commonpath([tut,os.path.abspath(tutorialFile)]).strip()
    tutorialText.append(str(os.path.relpath(tut,common)).replace('\\','/'))


text = mainText+'\n   '+'\n   '.join(tutorialText)+'\n\n'



with open(tutorialFile,'w') as f:
    f.write(text)

