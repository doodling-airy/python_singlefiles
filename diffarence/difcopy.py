import pyperclip as pc
import re
import os

def difcopy(wanna):
    path = input("copy to modulename : ")
    copylist = wanna.split('\n')
    lines_strip = [line.strip() for line in copylist]
    li = []
    for i in lines_strip:
        reg = re.sub(r'module tb_[\w]*;', 'module tb_'+path+';', str(i))
        reg = re.sub(r'[\w]* u_[\w]*\(', path + ' u_' + path + '(', str(reg))
        li.append(reg)
    with open(path+'.v', 'w') as f:
        try:
            joinedcopy = '\n'.join(li)
            f.write(joinedcopy)
            print(joinedcopy)
            
        except:
            os.system('code ' + path + '.v')

while(True):
    difcopy(pc.paste())
