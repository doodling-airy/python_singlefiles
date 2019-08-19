import pyperclip as pc

def print_copy(replacestring, sets):
    replacestring = rep(replacestring, sets)
    return replacestring

def rep(rs, sets):
    for i in range(len(sets)):
        pre, post = sets[i]
        rs = rs.replace(pre, post)
    return rs

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
    replacestring = igui.inputtext.get("1.0", "end-1c")
    replaceset = [["tmp", "w_tmp"], ["(H", "(r_H"], ["(N", "(w_N"]]
    replacestring = print_copy(replacestring, replaceset)
    print(replacestring)
    pc.copy(replacestring)

if __name__ == "__main__":
    import tkinter as tk
    igui = Cgui()

    


