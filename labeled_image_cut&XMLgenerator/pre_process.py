import os
import sys
import time

path = './'
dirs = os.listdir(path)
cnt = 0

for names in dirs:
    names = names.split('.')
    if len(names) < 2:
        continue
    if names[1] in ['lbl','xml','py'] :
        continue
    name = names[0]
    if names[1] != 'jpg':
        os.system('mv ' + name + '.' + names[1] + ' '  + name + '.jpg')
    os.system('/usr/local/anaconda2/bin/python gen_xml.py ' + name + '.jpg '+ name + '.lbl ' + name + '.xml')
    cnt += 1
   # print cnt,':',names[0]
