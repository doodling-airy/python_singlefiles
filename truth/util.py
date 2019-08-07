
    #uniqueなリストを作る
def get_unique_list(tmp):
    relist = []
    seen = []
    tmp = [x for x in tmp if x not in seen and not seen.append(x)]
    for i in tmp:
        if len(i) != 0:
            relist.append(i)
    return relist

def get_duplicate_list(seq):
    seen = []
    return [x for x in seq if not seen.append(x) and seen.count(x) >= 2]