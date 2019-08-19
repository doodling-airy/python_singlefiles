import os

def opener(openfile_names):
    if (type(openfile_names) in (list, set, tuple)):
        pass
    else:
        if type(openfile_names) is str:
            openfile_names = openfile_names.split('\n')
        else:
            return None

    for i in range(len(openfile_names)):
        n_module = openfile_names[i]
        path = n_module + ".v" #samplepath        
        cmd = 'code '+ path
        os.system(cmd)

#####################################################################################################

class Cgui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("700x700")
        self.n_module = tk.Entry(self.root, justify="left", width=5)
        self.n_module.place(x=0,y=0)
        self.inputtext = tk.Text(self.root, height=55, width=100, wrap=tk.CHAR)
        self.inputtext.place(x=0, y=0)
        self.outbutton = tk.Button(self.root, text="out", width=5, command=lambda:out(self))
        self.outbutton.place(x=100, y=270)
        self.root.mainloop()


def out(igui):
    openfile_names = igui.inputtext.get("1.0", "end-1c").split("\n")
    opener(openfile_names)
        
if __name__ == "__main__":
    import tkinter as tk
    igui = Cgui()

    


