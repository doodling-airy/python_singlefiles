from util import get_unique_list
from debug import pr

class cPreQuine:
    def __init__(self, recevegui):
        self.re = recevegui

    def preprocess(self, li_relation):
        li_predata = li_relation
        li_postdata = []
        while(True):
            li_postdata = get_unique_list(self.compareloop(li_predata))
            pr(li_postdata)
            if len(li_postdata) == 0:
                break
            li_predata = li_postdata
        return li_predata

    def compareloop(self, li_selected):
        relist = []
        li_Cinput = []
        li_Cin_pre = []
        for i in range(self.re.inputcount):
            li_Cinput = self.countone(li_selected, i)
            if (len(li_Cinput) * len(li_Cin_pre)) != 0 :
                relist.extend(self.compare(li_Cinput, li_Cin_pre))
            li_Cin_pre = li_Cinput
        return relist

    #1の数によって振り分ける
    def countone(self, li_selected, i):
        relist = []
        for c in range(len(li_selected)):
            if li_selected[c].count('1') == i :
                if len(li_selected[c]) == 0:
                    continue
                relist.append(li_selected[c])
        return relist

    def compare(self, li_pre, li_post):
        relist = []
        for pre in li_pre:
            for post in li_post:
                tmp = self.comparecore(pre, post)
                relist.append(tmp)
                pr(relist)
        return relist

    def comparecore(self, pre, post):
        tmp = []
        bb = 0
        for i, j in zip(pre, post):
            if(i == '_' or j == '_'):
                if(i == '_' and j == '_'):
                    tmp.append('_')
                    continue
                else:
                    if len(list(set(pre)-set(post))) == 1:
                        if (pre.count('_')-post.count('_')) >= 0:
                            return pre
                        else: 
                            return post
                    else:
                        return post
            if i != j :
                bb += 1
                tmp.append('_')
            else:
                tmp.append(i)
        return tmp if bb==1 else post
        