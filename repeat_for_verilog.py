import re
import os

class Verilog:
    def __init__(self):
        self.verilog_filename = input("verilog file name : ")
        self.verilog_filestream = open(self.verilog_filename, "r")
        self.filedata = []
        self.seeds = set(['x', 'h'])
    def __del__(self):
        self.verilog_filestream.close()

    def mainstream(self):
        for self.line in self.verilog_filestream:
            self.finder()

    def finder(self):
        self.sharp = self.line.find("#")
        if(self.sharp != -1): 
            self.x = self.line[self.sharp+2]
            self.replaceting(self.line[self.sharp+1])
        else:
            self.filedata.append(self.line)

    def replaceting(self, seed):
        if(seed in self.seeds):
            for i in range(int(re.sub("\\D", "", self.line[self.sharp+3:self.sharp+3 + int(self.x)]))):
                print(format(i, "02" + seed ).upper())
                self.lined = self.line.replace("#" + seed + self.line[self.sharp+2:self.sharp+2 + int(self.x) + 1], format(i, "02" + seed ).upper())
                self.filedata.append(self.lined)
    
    def out(self):
        path = r"C:\Users\iwaha\Documents\practice_6_14\\" + self.verilog_filename
        with open(path, mode='w') as f:
            f.write("".join(self.filedata))
                
        cmd = 'code ' + self.verilog_filename 
        os.system(cmd)

vlog = Verilog()
vlog.mainstream()
vlog.out()
del vlog

