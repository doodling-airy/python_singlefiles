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

