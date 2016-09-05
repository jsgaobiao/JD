import os, sys

# open files
path1 = "fanhuahuangtu/"
path2 = "shaidanhuangtu/"
dirs1 = os.listdir(path1)
dirs2 = os.listdir(path2)
fout1 = open('result1.txt','w')
fout2 = open('result2.txt','w')

fin = open('result.txt')
for lines in fin :
    line = lines.rstrip('\n')
    line = line.split('\t')
    filedir = line[0].split('/')
    filename = filedir[2]
    filetype = filedir[1]
    if filetype == 'porn' :
        if filename in dirs1 :
            fout1.write(lines)
        if filename in dirs2 :
            fout2.write(lines)
    else :
        fout1.write(lines)
        fout2.write(lines)

fin.close()
fout1.close()
fout2.close()

