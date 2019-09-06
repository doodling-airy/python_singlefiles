import sys
import os
import re
import shutil

class grep:
    #入力されたオプションと検索文字列を振り分ける役割
    def __init__(self, args):
        #検索したい文字列は最後に入力される仕様
        self.search_word = args.pop(-1)
        query_options = args
        
        ###default
        self.d = False
        self.r = False
        self.c = ""
        self.p = os.getcwd()
        self.option_decoder(query_options)
        ###

        shutil.copytree(self.p, "../" + self.p + "-backup")
        if(self.r):
            #正規表現に当てはめる
            self.search_word = r"{}".format(self.search_word)
        if(self.d):
            self.file_admin_deep(self.p)
        else:
            self.file_admin_wd(self.p)
    #オプションリスト
        # -s 配下にあるディレクトリも検索対象に入れる
        # -e 正規表現(regular Expression)で検索する
        # -r 検索に当てはまった文字列を後続の文字列にreplaceする
        # -p 後続のpathで検索を行う。デフォルトはカレントディレクトリ
        # -b backup cwdの上にできる。
    def option_decoder(self, query_optionset):
        option_list = list(["-s","-e","-r","-p","-b"])
        # -c -pを設定するときは検索文字列以外にも
        # ユーザー任意の文字列がquery_optionsetに入り込むため
        # option_onlyに取捨したものを入れる
        option_only = set(query_optionset) & set(option_list)
        for option in option_only:
            if(option == option_list[0]):
                self.d = True
            if(option == option_list[1]):
                self.r = True
            if(option == option_list[2]):
                #設定したオプションの位置を取得、その後ろにある文字列を取得
                self.c = query_optionset[query_optionset.index(option) + 1]
            if(option == option_list[3]):
                self.p = query_optionset[query_optionset.index(option) + 1]
            if(option == option_list[4]):
                self.b = True

    #検索する対象fileの管理・受け渡しを行う
    #下記のwdとの違いは配下のディレクトリも走査するかどうか
    def file_admin_deep(self, search_path):
        directory_contents = os.listdir(search_path)
        for content in directory_contents:
            path = search_path + "/" + content
            if os.path.isdir(path):
                self.file_admin_deep(path)
            if os.path.isfile(path):
                self.search_on_file(path)

    #検索する対象fileの管理・受け渡しを行う
    def file_admin_wd(self, search_path):
        directory_contents = os.listdir(search_path)
        for content in directory_contents:
            path = search_path + "/" + content
            if os.path.isfile(path):
                self.search_on_file(path)

    def search_on_file(self,path):
        with open(path) as f:
            lines = f.readlines()
            k = []
            if(self.c != ""):
                for line in lines:
                    k.append(re.sub(self.search_word, self.c, line))
                    with open(path, mode='w') as fi:
                        fi.writelines(k)
                        print(path, " replace complete!")
            else:
                for line in lines:
                    ismatch = re.search(self.search_word, line)
                    if ismatch != None:
                        print(path)
                        return None
                print("no matches")




g = grep(sys.argv[1:])
