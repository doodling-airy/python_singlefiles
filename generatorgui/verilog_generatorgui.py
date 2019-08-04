import tkinter as tk
import os 

class gui:
    def __init__(self,ac):
        self.ac = ac

        self.root = tk.Tk()
        self.root.title(u"Tkinter Test")
        self.root.geometry("1500x750")

        self.tx_n_module = tk.Entry(width="10")
        self.tx_n_module.place(x=0, y=10)
        self.tx_c_input = tk.Entry(width="10")
        self.tx_c_input.place(x=100, y=10)
        self.tx_c_output = tk.Entry(width="10")
        self.tx_c_output.place(x=200, y=10)
        self.tx_c_truth = tk.Entry(width="10")
        self.tx_c_truth.place(x=300, y=10)

        self.positionbutton(0, 50, "always", self.ac.pushalways, "*")
        self.positionbutton(50, 50, "Palways", self.ac.pushalways, "posedge")
        self.positionbutton(100, 50, "Nalways", self.ac.pushalways, "negedge")
        self.positionbutton(150, 50, "assign", self.ac.pushassign, None)
        self.positionbutton(200, 50, "r_1", self.ac.pushregone, None)
        self.positionbutton(250, 50, "rr_1", self.ac.pushregsec, None)
        
        self.step = tk.Entry(width="15")
        self.step.place(x=350, y=50)
        self.positionbutton(510, 50, "printstep", self.ac.pushstep, None)
        
        self.tmpwindow = tk.Text(self.root, height=15, width=50, wrap=tk.CHAR)
        self.tmpwindow.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.tmpwindow.place(x=0,y=200)
        
        self.positionbutton(440, 200, "push", self.ac.pushtmptotx, None)
        self.positionbutton(440, 250, "elif", self.ac.pushelif, None)

        self.positionbutton(440, 300, "always", self.ac.tmpalways, "*")
        self.positionbutton(440, 350, "Palways", self.ac.tmpalways, "posedge")
        self.positionbutton(440, 400, "Nalways", self.ac.tmpalways, "negedge")


        self.txwindow = tk.Text(self.root, height=53, width=70, wrap=tk.CHAR)
        self.txwindow.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.txwindow.place(x=800,y=0)
        
        self.i = 2
    def rungui(self):
        self.root.mainloop()
    def positionbutton(self, x, y, text, cmd, arg):
        btn = tk.Button(self.root, text=text, width="5", command= lambda:cmd(arg))
        btn.place(x=x, y=y)
        
class action:
    def __init__(self, tex):
        self.tmparray = []
        self.tex = tex
    def initprocess(self, gg):
        self.gg = gg
        self.tex.n_module = self.gg.tx_n_module.get()
        self.tex.c_input = int(self.gg.tx_c_input.get())
        self.tex.c_output = int(self.gg.tx_c_output.get())
        self.tex.c_truth = int(self.gg.tx_c_truth.get())
        #print(self.tex.n_module)
        self.tex.inputprocess()
        self.tex.outputprocess()
        self.tex.inoutprocess()
        self.gg.txwindow.insert(tk.END, "//module\n")
        self.gg.txwindow.insert(tk.END, "module " + self.tex.n_module + "(" + "input " + ', input '.join(self.tex.Hinput) + ", output " + ', output '.join(self.tex.Noutput) + ");\n")
        self.gg.txwindow.insert(tk.END, "reg [3:0]tmp;\n")
        for i in range(self.tex.c_input):
            #print(self.tex.Hinput)
            self.gg.positionbutton(i*50,80, "H" + str(i+1), self.pushinput, self.tex.Hinput[i])
        for i in range(self.tex.c_input):
            #print(self.tex.Hinput)
            self.gg.positionbutton(i*50,110, "r_H" + str(i+1), self.pushinput, self.tex.tbHinput[i])
        for i in range(self.tex.c_output):
            #print(self.tex.Noutput)
            self.gg.positionbutton(i*50,140, "N" + str(i+1), self.pushinput, self.tex.Noutput[i])
        for i in range(self.tex.c_output):
            #print(self.tex.Noutput)
            self.gg.positionbutton(i*50,170, "w_N" + str(i+1), self.pushinput, self.tex.tbNoutput[i])
        self.tmpHNputs()
    def secondprocess(self, _):
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, "endmodule\n")
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, "//testbench\n")
        self.gg.txwindow.insert(tk.END, "`timescale 1ps/1ps;\n")
        self.gg.txwindow.insert(tk.END, "module tb_" + self.tex.n_module + ";\n")
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, "parameter REP = " + str(self.tex.c_truth) + ";\n")
        self.gg.txwindow.insert(tk.END, "parameter STEP = 100;\n")
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, "reg " + ', '.join(self.tex.tbHinput) + ";\n")
        self.gg.txwindow.insert(tk.END, "wire " + ', '.join(self.tex.tbNoutput) + ";\n")
        self.gg.txwindow.insert(tk.END, "reg [3:0] r_tmp;\n")
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, self.tex.n_module + " u_" + self.tex.n_module + "(" + ', '.join(self.tex.tbconnect) + ");\n")
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, "initial begin\n")
        self.gg.txwindow.insert(tk.END, "    " + self.tex.chaintbHinput + " = " + str(self.tex.c_input) + "'b0;\n")
        
    def thirdprocess(self, _):
        self.gg.txwindow.insert(tk.END, "    #STEP;\n")
        self.gg.txwindow.insert(tk.END, "end\n")
        self.gg.txwindow.insert(tk.END, "\n")
        self.pushtb(_)
        self.gg.txwindow.insert(tk.END, "\n")
        self.gg.txwindow.insert(tk.END, "initial begin\n")
        self.gg.txwindow.insert(tk.END, "    #11;\n")
        self.gg.txwindow.insert(tk.END, "    repeat(REP) begin\n")
        self.gg.txwindow.insert(tk.END, "        #STEP;\n")
        self.gg.txwindow.insert(tk.END, "        if(" + ' & '.join(self.tex.tbiftext) + ") begin\n")
        self.gg.txwindow.insert(tk.END, "            $display(\"[ %t]OK!\", $time);\n")
        self.gg.txwindow.insert(tk.END, "        end else begin\n")
        self.gg.txwindow.insert(tk.END, "            $display(\"[ %t]NG!\", $time);\n")
        self.gg.txwindow.insert(tk.END, "            #1;\n")
        self.gg.txwindow.insert(tk.END, "          $stop;\n")
        self.gg.txwindow.insert(tk.END, "        end\n")
        self.gg.txwindow.insert(tk.END, "    end\n")
        self.gg.txwindow.insert(tk.END, "end\n")
        self.gg.txwindow.insert(tk.END, "endmodule\n")
    def pushinput(self, text):
        self.gg.txwindow.insert('insert', str(text))
    def pushtmp(self, text):
        self.gg.tmpwindow.insert('insert', str(text))
    def pushalways(self, term):
        self.gg.txwindow.insert(tk.END, "always @(" + term + ") begin\n")
        self.gg.txwindow.insert(tk.END, "    if({} == 'b) begin\n")
        self.gg.txwindow.insert(tk.END, "        \n")
        self.gg.txwindow.insert(tk.END, "    end\n")
        self.gg.txwindow.insert(tk.END, "end\n")
    def tmpalways(self, term):
        self.gg.tmpwindow.insert(tk.END, "always @(" + term + ") begin\n")
        self.gg.tmpwindow.insert(tk.END, "    if({} == 'b) begin\n")
        self.gg.tmpwindow.insert(tk.END, "        \n")
        self.gg.tmpwindow.insert(tk.END, "    end\n")
        self.gg.tmpwindow.insert(tk.END, "end\n")
    def tmpHNputs(self):
        for i in range(self.tex.c_input):
            #print(self.tex.Hinput)
            self.gg.positionbutton(i*50,450, "H" + str(i+1), self.pushtmp, self.tex.Hinput[i])
        for i in range(self.tex.c_input):
            #print(self.tex.Hinput)
            self.gg.positionbutton(i*50,500, "r_H" + str(i+1), self.pushtmp, self.tex.tbHinput[i])
        for i in range(self.tex.c_output):
            #print(self.tex.Noutput)
            self.gg.positionbutton(i*50,550, "N" + str(i+1), self.pushtmp, self.tex.Noutput[i])
        for i in range(self.tex.c_output):
            #print(self.tex.Noutput)
            self.gg.positionbutton(i*50,600, "w_N" + str(i+1), self.pushtmp, self.tex.tbNoutput[i])
    def pushassign(self, _):
        self.gg.txwindow.insert(tk.END, "assign  = ;\n")
    def pushtmptotx(self, _):
        self.tmp = self.gg.tmpwindow.get("1.0", 'end -1c')
        self.gg.txwindow.insert(tk.END, self.tmp)
        self.tmparray.append(self.tmp)
        self.gg.tmpwindow.delete("1.0", tk.END)
    def pushelif(self, _):
        self.tmp = self.gg.tmpwindow.get("1.0", 'end -1c')
        inif = self.tmp[self.tmp.rfind("(")+1:self.tmp.rfind("end")]
        self.tmp = self.tmp.replace("end", "end else if(" + inif + " ", 1)
        self.gg.tmpwindow.delete("1.0", tk.END)
        self.gg.tmpwindow.insert(tk.END, self.tmp)
    def pushtb(self, _):
        for text in self.tmparray:
            text = text.replace("H", "r_H")
            text =text.replace("tmp", "r_tmp")
            #print(text)
            self.gg.txwindow.insert(tk.END, text)
    def pushregone(self, _):
        self.gg.txwindow.insert('insert', "tmp[]")
    def pushregsec(self, _):
        self.gg.txwindow.insert('insert', "r_tmp[]")  
    def pushstep(self, _):
        bits = str(self.gg.step.get())
        self.gg.txwindow.insert('insert', "    #STEP " + self.tex.chaintbHinput + " = " + str(self.tex.c_input) + "'b" + bits + ";\n")
    
class cText:
    def __init__(self):
        self.n_module = "" #gg.tx_n_module.get()
        self.c_input = 0 #gg.tx_c_input.get()
        self.c_output = 0 #gg.tx_c_output.get()
        self.c_truth = 0
        self.Hinput = []
        self.tbHinput = []
        self.Noutput = []
        self.tbNoutput = []
        self.tbiftext = []
        self.tbconnect = []
    def inputprocess(self):
        for i in range(self.c_input):
            space = "0" if (i//9)==0 else ""
            self.Hinput.append("H" + space + str(i + 1))
        for st in self.Hinput:
            self.tbHinput.append("r_" + st)
        self.chaintbHinput = '{' + ', '.join(self.tbHinput) + '}'
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
            

tex = cText()
ac = action(tex)
gg = gui(ac)

def out(txw):
    path = n_module + ".v" #samplepath
    with open(path, mode='w') as f:
       f.write(txw.get('1.0', tk.END ))
            
    cmd = 'code '+ ac.tex.n_module +'.v'
    os.system(cmd)
    txw.delete("1.0", tk.END)
    del tex
    del ac
    del gg

gg.positionbutton(400,10,"init",ac.initprocess, gg)
gg.positionbutton(450,10,"second",ac.secondprocess, None)
gg.positionbutton(500,10,"third",ac.thirdprocess, None)
gg.positionbutton(550,10, "out", out, gg.txwindow)
gg.rungui()
