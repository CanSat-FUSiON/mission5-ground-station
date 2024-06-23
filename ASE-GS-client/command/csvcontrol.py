import csv
import tkinter.messagebox as messagebox
from tkinter import *
import tkinter.ttk as ttk
from csvview import CSVView
import os

class CSVLogic:
    """
    csvViewer読み込み、書き込みロジック
    """

    def __init__(self):
        """
        列とレコード用の配列を初期化
        """
        self.header =[]
        self.data =[]

    def readCsv(self,data_path):
        """
        csvを読み込んで内部にデータを反映する
        1行目を列名、他の行をデータとして取得する
        """
        ret = True
        header = []
        data =[]
        try :
            with open(data_path, "r",newline="") as csv_file:
                f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\n", quotechar='"', skipinitialspace=True)
                header = next(f)
                print(header)
                for row in f:
                    data.append(row)
        except IOError as e:
            print(e)
            ret = False
        self.header = header
        self.data = data
        return ret

    def writeCsv(self,data_path,columns,rows):
        """
        与えられた列名リストとレコードリストを書きだす
        """
        ret = True
        csv_file = open(data_path, "w",newline="")
        try:
            with open(data_path, 'w') as csv_file:
                writer = csv.writer(csv_file, lineterminator='\n')
                writer.writerow(columns)
                writer.writerows(rows)
        except IOError as e:
            print(e)
            ret = False
        return ret
    def getHeader(self):
        return self.header
    def getData(self):
        return self.data


class CSVControl:
    """
    csvViewerのコントローラー
    """

    def __init__(self):
        """
        アプリの立ち上げとイベント登録
        """
        master = Tk()
        master.title("CsvViewer")
        master.geometry("1000x400")
        self.view = CSVView(master)
        self.logic = CSVLogic()
        self.view.setReadButtonCommand(self.readButtonCommand)
        master.mainloop()

    def readButtonCommand(self):
        """
        csv読み込みボタン用コマンド
        csvから取得した列名、データをViewに反映する。
        csvが変更されるごとにRowDataフレームがリロードされるので、
        保存ボタンコマンドも再設定
        """

        columns,datas = self.readCsv()
        self.view.setNewColumnAndData(columns,datas)
        self.view.setSaveButtonCommand(self.saveButtonCommand)

    def saveButtonCommand(self):
        """
        保存ボタン用コマンド
        指定されたパスにviewで指定された情報をcsv形式で書きだす
        """
        file_path = self.view.getFilePath()
        columns = self.view.getColumns()
        rows =self.view.getRows()
        ret = self.logic.writeCsv(file_path,columns,rows)
        if ret:
            messagebox.showinfo("writecsv","succeed")
        else:
            messagebox.showerror("writecsv","failed")

    def readCsv(self):
        """
        csv読み込んで列名とデータを返却
        """
        ret = False;
        file_path = self.view.getFilePath()
        if os.path.exists(file_path) :
            ret = self.logic.readCsv(file_path)
        if ret:
            messagebox.showinfo("readcsv","succeed")
        else:
            messagebox.showerror("readcsv","failed")
        return self.logic.getHeader(),self.logic.getData()

if __name__ == '__main__':
    control =  CSVControl()
    # control.readCsv()