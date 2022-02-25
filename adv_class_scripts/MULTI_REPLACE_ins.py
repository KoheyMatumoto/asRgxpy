
#Gspreadと連携したくはない…するならギャラクシー側で取得した値だけを辞書化して使いたいぐらい。

class MULTI_REPLACE():
    def __init__(self):
        super().__init__()
        print("multi replace rdy")

    def replace_by_dim2arr(self,string,dim2):
        resultstr = string

        for row in dim2:
            resultstr = resultstr.replace(row[0],row[1])
        return resultstr