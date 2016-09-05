import os
import sys

path = sys.argv[1]
dirs = os.listdir(path)

fout = open(sys.argv[2],'w')
for names in dirs:
    names = names.split('.')
    name = names[0]
    fout.write(name+'\n')

fout.close()

