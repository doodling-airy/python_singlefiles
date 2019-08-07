from util import get_unique_list, get_duplicate_list
from debug import pr

class cQuine:
    def __init__(self, recevegui, prequine):
        self.re = recevegui
        #self.re.allout()
        self.pq = prequine

    def process(self):
        outconnect = []
        for i in range(len(self.re.output_list)):
            self.li_relation = self.relation_in_out(self.re.output_list[i])
            #mainitem : 主項
            mainitem = self.pq.preprocess(self.li_relation)
            results = self.minimain(mainitem, self.re.input_list)
            pr(mainitem)
            pr(results)
            outconnect.append('assign N'+ format(i+1, '02d') + ' = ' + self.trance(results) + ';\n')
        return outconnect

        #出力に関係のある入力だけにする
    def relation_in_out(self, outputrow):
        relist = []
        for index, num in enumerate(outputrow):
            if num == '1':
                relist.append(self.re.input_list[index])
        print("relation_in_out : ", relist)
        return relist
    

    def minimain(self, mainitems, miniitems):
        relist = []
        li_includeds = []
        for mainitem in mainitems:
            li_includeds.append(self.isincludeprocess(mainitem, miniitems))
            pr(li_includeds)
        uniqueelements = self.isduplicate(li_includeds)
        pr(uniqueelements)
        relist = self.haveunique(uniqueelements, li_includeds, mainitems)
        return get_unique_list(relist)
    
    def isincludeprocess(self, mainitem, miniitems):
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

    def isduplicate(self, li_includeds):
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

    def trance(self, results):
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


    def haveunique(self, uniqueelements, li_includeds, mainitems):
        relist = []
        for i in uniqueelements:
            for index, j in enumerate(li_includeds):
                if i in j:
                    relist.append(mainitems[index])
        return relist