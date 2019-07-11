import tkinter as tk
import numpy as np
import os

def notduplicate_toX(tmp): #Xは不定のことを指す。ここではXを''として扱う。
    if len(tmp) <= 1:#要素が一つしかない場合はそれをそのまんま通したい
        return tmp
    skip = []
    tmpara = []
    duplicate = []
    while True:
        
        axistmp = []
        print("tmp : ", tmp)
        for index, axis in enumerate(tmp):
            skipbool = False
            axistmp = axis[:]
            
            for i in skip:
                print("i : ", i, axis)
                if i == axis: skipbool = True
            if skipbool: 
                print(axis)
                continue
            for slices in tmp[index+1:]:
                NDcount = False #同じじゃない要素をカウント
                onezero = False
                sp = None
                print("axis, slices : ", axis, slices)
                for i, j in zip(enumerate(axis), slices):
                    if i[1] != j:
                        #他のやつをチェックしてそれらが全部同じならこの要素を''(不定)にして統合する
                        if i[1] == '' or j == '': 
                            NDcount = True
                            sp = i[0]
                        else:
                            if onezero == False:
                                NDcount = True
                                sp = i[0]
                                onezero = True
                            else:
                                NDcount = False

                        #else: NDcount = False
                if NDcount == True: #1箇所だけ違う場合の統合処理
                    print("axis 1 : ", axistmp, slices, sp)
                    axistmp[sp] = ''
                    print("axis a : ", axistmp, axis, slices)
                    duplicate.append(axistmp)
                    skip.append(axis)
                    skip.append(slices)
                else:
                    #if duplicate == []: #余り者同士で変な動作をする為それを回避
                    print("axis o : ", axis, slices)
                    duplicate.append(axis)
                    duplicate.append(slices)
        
    
        uniq = []
        for x in duplicate:
            if x not in uniq:
                uniq.append(x)
        print("duplicate notduplicate_toX : ", uniq, skip)
        if tmpara == uniq:
            break
        tmpara = uniq

    return uniq

'''
def notduplicate_toX(tmp, skip): #Xは不定のことを指す。ここではXを''として扱う。
    if len(tmp) <= 1:#要素が一つしかない場合はそれをそのまんま通したい
        return tmp

    duplicate = []
    axistmp = []
    print("tmp : ", tmp)
    for index, axis in enumerate(tmp):
        skipbool = False
        axistmp = axis[:]
        print("axistmp : ", axistmp)
        for i in skip:
            print("i : ", i, axis)
            if i == axis: skipbool = True
        if skipbool: 
            print(axis)
            continue
        for slices in tmp[index+1:]:
            NDcount = False #同じじゃない要素をカウント
            onezero = False
            sp = None
            for i, j in zip(enumerate(axis), slices):
                if i[1] != j:
                    #他のやつをチェックしてそれらが全部同じならこの要素を''(不定)にして統合する
                    if i[1] == '' or j == '': 
                        NDcount = True
                        sp = i[0]
                    else:
                        if onezero == False:
                            NDcount = True
                            sp = i[0]
                            onezero = True
                    #else: NDcount = False
            if NDcount == True: #1箇所だけ違う場合の統合処理
                print("axis 1 : ", axistmp, slices, sp)
                axistmp[sp] = ''
                print("axis a : ", axistmp, axis, slices)
                duplicate.append(axistmp)
                skip.append(axis)
                skip.append(slices)
            else:
                #if duplicate == []: #余り者同士で変な動作をする為それを回避
                print("axis o : ", axis, slices)
                duplicate.append(axis)
                duplicate.append(slices)
    uniq = []
    for x in duplicate:
        if x not in uniq:
            uniq.append(x)
    print("duplicate notduplicate_toX : ", uniq, skip)
    return uniq, skip
'''




def out(igui):
    #modulename
    module_name = igui.n_module.get()
    #
    input_list = [list(i) for i in igui.inputtext.get("1.0", "end-1c").split("\n")]
    output_list = [list(i) for i in zip(*igui.outputtext.get("1.0", "end-1c").split("\n"))] #zip(*~~) => 転置
    #confirm
    print("module_name : ", module_name)
    print("input_list : ", input_list)
    print("output_list : ", output_list)
    #
    booleans = []
    for col in output_list:
        tmp = []
        duplicate = []
        asss = []
        #trueを出力するinputをピックアップすることで加法標準形にする準備をしている。
        for index, num in enumerate(col):
            if int(num):
                tmp.append(input_list[int(index)])
        print("tmp : ", tmp)

        duplicate = tmp
        skip = []
        duplicate = notduplicate_toX(duplicate)
        '''
        while True :
            print("duplicate : ", duplicate)
            duplicate = notduplicate_toX(duplicate, skip)
            skip = duplicate[1:]
            duplicate = [duplicate[0]]
            print("uniq : ", duplicate, skip, tmp)
            if duplicate == tmp:
                break
            tmp = duplicate
        '''
        booleans.append(duplicate)
    print("booleans : ", booleans)

    for i in booleans:
        tmp = []
        for j in i:
            tex = []
            for index, m in enumerate(j):
                if m == '1':
                    tex.append('H0' + str(index+1))
                elif m == '0':
                    tex.append('~H0' + str(index+1))
            tmp.append('&'.join(tex))
        print('|'.join(tmp))
        
    
    
    
    

class Cgui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x300")
        self.n_module = tk.Entry(self.root, justify="left", width=5)
        self.n_module.place(x=0,y=0)
        self.inputtext = tk.Text(self.root, height=15, width=15, wrap=tk.CHAR)
        self.inputtext.place(x=0, y=30)
        self.inputtext.insert( tk.END, "0001\n0101\n1001\n1101" ) 
        self.outputtext = tk.Text(self.root, height=15, width=15, wrap=tk.CHAR)
        self.outputtext.place(x=150, y=30)
        self.outputtext.insert( tk.END, "01\n01\n01\n11" ) 
        self.outbutton = tk.Button(self.root, text="out", width=5, command=lambda:out(self))
        self.outbutton.place(x=100, y=270)
        self.root.mainloop()

igui = Cgui()
