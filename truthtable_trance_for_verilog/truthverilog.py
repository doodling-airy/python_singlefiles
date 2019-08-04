import tkinter as tk
import numpy as np
import os

from inspect import currentframe

def pr(*args):
    names = {id(v):k for k,v in currentframe().f_back.f_locals.items()}
    print(', '.join(names.get(id(arg),'???')+' = '+repr(arg) for arg in args))


class cText:
    def __init__(self, i, o):
        self.c_input = i #gg.tx_c_input.get()
        self.c_output = o #gg.tx_c_output.get()
        self.Hinput = []
        self.tbHinput = []
        self.Noutput = []
        self.tbNoutput = []
        self.tbiftext = []
        self.tbconnect = []
        
        self.inputprocess()
        self.outputprocess()
        self.inoutprocess()
    def inputprocess(self):
        for i in range(self.c_input):
            space = "0" if (i//9)==0 else ""
            self.Hinput.append("H" + space + str(i + 1))
        for st in self.Hinput:
            self.tbHinput.append("r_" + st)
        tmptbHinput = self.tbHinput.copy()
        tmptbHinput.reverse()
        self.chaintbHinput = '{' + ', '.join(tmptbHinput) + '}'
    def outputprocess(self):
        for i in range(self.c_output):
            space = "0" if (i//9)==0 else ""
            self.Noutput.append("N" + space + str(i + 1))
        for st in self.Noutput:
            self.tbNoutput.append("w_" + st)
        for st in self.tbNoutput:
            self.tbiftext.append("(" + st + " == )")
    def inoutprocess(self):
        for H, tbH in zip(self.Hinput, self.tbHinput):
            self.tbconnect.append("." + H + "(" + tbH + ")")
        for N, tbN in zip(self.Noutput, self.tbNoutput):
            self.tbconnect.append("." + N + "(" + tbN + ")")


def out(igui):
    n_module = igui.n_module.get()
    input_list = [list(i) for i in igui.inputtext.get("1.0", "end-1c").split("\n")]
    output_list = [list(i) for i in zip(*igui.outputtext.get("1.0", "end-1c").split("\n"))] #zip(*~~) => 転置
    global inputcount
    inputcount = len(input_list[0])
    outputcount = len(output_list)
    c_truth = 2 ** len(output_list[0])
    tex = cText(inputcount, outputcount)

    outconnect = process(igui)
    
    code = []
    code.append("//module\n")
    code.append("module " + n_module + "(" + "input " + ', input '.join(tex.Hinput) + ", output " + ', output '.join(tex.Noutput) + ");\n")
    code.append("\n")
    code.extend(outconnect)
    code.append("\n")
    code.append("endmodule\n")
    code.append("\n")
    code.append("\n")
    code.append("//testbench\n")
    code.append("`timescale 1ps/1ps;\n")
    code.append("module tb_" + n_module + ";\n")
    code.append("\n")
    code.append("parameter REP = " + str(c_truth) + ";\n")
    code.append("parameter STEP = 100;\n")
    code.append("\n")
    code.append("reg " + ', '.join(tex.tbHinput) + ";\n")
    code.append("wire " + ', '.join(tex.tbNoutput) + ";\n")
    code.append("reg [3:0] r_tmp;\n")
    code.append("\n")
    code.append(n_module + " u_" + n_module + "(" + ', '.join(tex.tbconnect) + ");\n")
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
    emit(n_module, code)

def emit(n_module, outlist):
    path = n_module + ".v" #samplepath
    with open(path, mode='w') as f:
       f.write(''.join(outlist))
            
    cmd = 'code '+ n_module +'.v'
    os.system(cmd)

def process(igui):
    input_list = [list(i) for i in igui.inputtext.get("1.0", "end-1c").split("\n")]
    output_list = [list(i) for i in zip(*igui.outputtext.get("1.0", "end-1c").split("\n"))] #zip(*~~) => 転置
    #confirm
    print("input_list : ", input_list)
    print("output_list : ", output_list)
    global inputcount
    outconnect = []
    for i in range(len(output_list)):
        li_relation = relation_in_out(input_list, output_list[i])
        #mainitem : 主項
        mainitem = prequine(li_relation)
        results = minimain(mainitem, input_list)
        pr(mainitem)
        pr(results)
        outconnect.append('assign N'+ format(i+1, '02d') + ' = ' + trance(results) + ';\n')
    return outconnect

def trance(results):
    strings = ''
    tttlist = []
    for result in results:
        tmplist = []
        for index, i in enumerate(result):
            if i == '0':
                tmplist.append('~H' + format(index+1, '02d'))
            elif i == '1':
                tmplist.append('H' + format(index+1, '02d'))
        tttlist.append('(' + '&'.join(tmplist) + ')')
    strings = '|'.join(tttlist)
    return strings


def minimain(mainitems, miniitems):
    relist = []
    li_includeds = []
    for mainitem in mainitems:
        li_includeds.append(isincludeprocess(mainitem, miniitems))
        pr(li_includeds)
    uniqueelements = isduplicate(li_includeds)
    pr(uniqueelements)

    relist = haveunique(uniqueelements, li_includeds, mainitems)
    return get_unique_list(relist)

def haveunique(uniqueelements, li_includeds, mainitems):
    relist = []
    for i in uniqueelements:
        for index, j in enumerate(li_includeds):
            if i in j:
                relist.append(mainitems[index])
    return relist

def isduplicate(li_includeds):
    allelement = []
    t = []
    relist = []
    for li_included in li_includeds:
        allelement.extend(li_included)
    t = get_duplicate_list(allelement)
    if len(t) != 0:
        for i in t:
            relist = [s for s in allelement if s != i]
    else: relist = allelement
    return relist

def isincludeprocess(mainitem, miniitems):
    relist = []
    pr(mainitem)
    pr(miniitems)
    for miniitem in miniitems:
        isinclude = True
        for i, j in zip(mainitem, miniitem):
            if i != '_':
                if i != j:
                    isinclude = False
        if isinclude == True:
            relist.append(miniitem)
    pr(relist)
    return relist

#出力に関係のある入力だけにする
def relation_in_out(input_list, output_list):
    relist = []
    for index, num in enumerate(output_list):
        if num == '1':
            relist.append(input_list[index])
    #print("relation_in_out : ", relist)
    return relist


######################################################################################################

def prequine(li_outtoin):
    li_predata = li_outtoin
    li_postdata = []
    while(True):
        li_postdata = get_unique_list(compareloop(li_predata))
        if len(li_postdata) == 0:
            break
        li_predata = li_postdata
    return li_predata

def compareloop(li_selected):
    relist = []
    li_Cinput = []
    li_Cin_pre = []
    global inputcount
    for i in range(inputcount):
        li_Cinput = countone(li_selected, i)
        if (len(li_Cinput) * len(li_Cin_pre)) != 0 :
            relist.extend(compare(li_Cinput, li_Cin_pre))
        li_Cin_pre = li_Cinput
    return relist
    
def compare(li_pre, li_post):
    relist = []
    for pre in li_pre:
        for post in li_post:
            tmp = []
            tmptwo = []
            bb = 0
            for i, j in zip(pre, post):
                if(i == '_' or j == '_'):
                    if(i == '_' and j == '_'):
                        tmp.append('_')
                        continue
                    else:
                        if len(list(set(pre)-set(post))) == 1:
                            if (pre.count('_')-post.count('_')) >= 0:
                                tmp.extend(pre)
                                break
                            else: 
                                tmp.extend(post)
                                break
                        else:
                            break
                if i != j :
                    bb += 1
                    tmptwo.append('_')
                else: tmptwo.append(i)
                '''
                if(i==j):
                    tmp.append(i)
                else:
                    tmp.append('_')
                '''
            if bb == 1:
                tmp.extend(tmptwo)
            else :
                tmp.extend(post)
                #tmp.append(pre)
            relist.append(tmp)
            pr(relist)
    return relist

#1の数によって振り分ける
def countone(input_list, i):
    relist = []
    for c in range(len(input_list)):
        if input_list[c].count('1') == i :
            if len(input_list[c]) == 0:
                continue
            relist.append(input_list[c])
    return relist


######################################################################################################


#uniqueなリストを作る
def get_unique_list(tmp):
    relist = []
    seen = []
    tmp = [x for x in tmp if x not in seen and not seen.append(x)]
    for i in tmp:
        if len(i) != 0:
            relist.append(i)
    #print("getuniquelist : ", relist)
    return relist

def get_duplicate_list(seq):
    seen = []
    return [x for x in seq if not seen.append(x) and seen.count(x) >= 2]


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
