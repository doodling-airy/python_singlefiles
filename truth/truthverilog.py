import tkinter as tk
import os

from debug import pr
from text import cText
from prequine import cPreQuine
from quine import cQuine

'''
def pr(*args):
    names = {id(v):k for k,v in currentframe().f_back.f_locals.items()}
    print(', '.join(names.get(id(arg),'???')+' = '+repr(arg) for arg in args))
'''

class cReceveGui:
    def __init__(self, igui):
        self.n_module = igui.n_module.get()
        self.input_list = [list(i) for i in igui.inputtext.get("1.0", "end-1c").split("\n")]
        self.output_list = [list(i) for i in zip(*igui.outputtext.get("1.0", "end-1c").split("\n"))] #zip(*~~) => 転置
        self.inputcount = len(self.input_list[0])
        self.outputcount = len(self.output_list)
        self.c_truth = 2 ** len(self.output_list[0])
    def allout(self):
        pr(self.n_module)
        pr(self.input_list)
        pr(self.output_list)
        pr(self.inputcount)
        pr(self.outputcount)
        pr(self.c_truth)

def out(igui):
    recevegui = cReceveGui(igui)
    #recevegui.allout()

    prequine = cPreQuine(recevegui)
    quine = cQuine(recevegui, prequine)

    tex = cText(recevegui.inputcount, recevegui.outputcount)

    outconnect = quine.process()
    
    code = []
    code.append("//module\n")
    code.append("module " + recevegui.n_module + "(" + "input " + ', input '.join(tex.Hinput) + ", output " + ', output '.join(tex.Noutput) + ");\n")
    code.append("\n")
    code.extend(outconnect)
    code.append("\n")
    code.append("endmodule\n")
    code.append("\n")
    code.append("\n")
    code.append("//testbench\n")
    code.append("`timescale 1ps/1ps;\n")
    code.append("module tb_" + recevegui.n_module + ";\n")
    code.append("\n")
    code.append("parameter REP = " + str(recevegui.c_truth) + ";\n")
    code.append("parameter STEP = 100;\n")
    code.append("\n")
    code.append("reg " + ', '.join(tex.tbHinput) + ";\n")
    code.append("wire " + ', '.join(tex.tbNoutput) + ";\n")
    code.append("reg [3:0] r_tmp;\n")
    code.append("\n")
    code.append(recevegui.n_module + " u_" + recevegui.n_module + "(" + ', '.join(tex.tbconnect) + ");\n")
    code.append("\n")
    code.append("initial begin\n")
    code.append("    " + tex.chaintbHinput + " = " + str(tex.c_input) + "'b0;\n")
    code.append("    repeat(REP) begin\n")
    code.append("        " + tex.chaintbHinput + " = " + tex.chaintbHinput  + " + 1'b1;\n")
    code.append("    end\n")
    code.append("    #STEP;\n")
    code.append("end\n")
    code.append("\n")
    code.append("\n")
    code.append("initial begin\n")
    code.append("    #11;\n")
    code.append("    repeat(REP) begin\n")
    code.append("        #STEP;\n")
    #code.append("        if(" + ' & '.join(tex.tbiftext) + ") begin\n")
    outstring = ')&('.join(outconnect)
    outstring = outstring.replace('H', 'r_H')
    outstring = outstring.replace('N', 'w_N')
    outstring = outstring.replace('=', '==')
    outstring = outstring.replace('assign', '')
    outstring = outstring.replace(';', '')
    outstring = outstring.replace('\n', '')
    outstring = outstring.replace(' ', '')

    code.append("        if((" + outstring + ")) begin\n")
    code.append("            $display(\"[ %t]OK!\", $time);\n")
    code.append("        end else begin\n")
    code.append("            $display(\"[ %t]NG!\", $time);\n")
    code.append("            #1;\n")
    code.append("          $stop;\n")
    code.append("        end\n")
    code.append("    end\n")
    code.append("end\n")
    code.append("endmodule\n")
    print(code)
    emit(recevegui.n_module, code)

def emit(n_module, outlist):##############
    path = n_module + ".v" #samplepath
    with open(path, mode='w') as f:
       f.write(''.join(outlist))
            
    cmd = 'code '+ n_module +'.v'
    os.system(cmd)


class Cgui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x300")
        self.n_module = tk.Entry(self.root, justify="left", width=5)
        self.n_module.place(x=0,y=0)
        self.inputtext = tk.Text(self.root, height=15, width=15, wrap=tk.CHAR)
        self.inputtext.place(x=0, y=30)
        self.inputtext.insert( tk.END, "0011\n0110\n1010\n1110" ) 
        self.outputtext = tk.Text(self.root, height=15, width=15, wrap=tk.CHAR)
        self.outputtext.place(x=150, y=30)
        self.outputtext.insert( tk.END, "01\n01\n01\n11" ) 
        self.outbutton = tk.Button(self.root, text="out", width=5, command=lambda:out(self))
        self.outbutton.place(x=100, y=270)
        self.root.mainloop()

igui = Cgui()