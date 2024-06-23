from tkinter import *
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

class FileOpenFrame(ttk.Frame):
    """
    ファイルの読み込み用フレーム
    """
    def __init__(self, master,file_entry_width=100):
        super().__init__(master)
        self.filePath = StringVar()
        self.createWidget(file_entry_width)
        self.pack()

    def createWidget(self,entry_width):
        filePathLabel = ttk.Label(self,text="FilePath")
        filePathLabel.grid(column=0,row=0)
        filepathEntry = ttk.Entry(self,textvariable=self.filePath,widt=entry_width)
        filepathEntry.grid(column=1,row=0)
        filepathButton = ttk.Button(self,text="open",command=self.openFileDialog)
        filepathButton.grid(column=2,row=0)
        self.readButton = ttk.Button(self,text="read")
        self.readButton.grid(column=3,row=0)

    def openFileDialog(self):
        """
        ファイルダイアログを開く
        """
        file  = filedialog.askopenfilename(filetypes=[("csv", "*.csv")]);
        self.filePath.set(file)

    def getFilePath(self):
        return self.filePath.get()

    def setReadButtonCommand(self,func):
        """
        読み込みを押したときのコマンドを指定する
        """
        self.readButton["command"] = func


class TreeView(ttk.Frame):
    """
    csvのデータを実際に表示するTreeview
    """
    def __init__(self,master):
        super().__init__(master)
        self.tree = None
        self.selected_iid = None
        self.columns =[]
        self.createWidget()
        self.pack()
        self.setSampleData()
    def createWidget(self):
        """
        icon列は不要なのでshow="headings"を指定
        """
        self.tree = ttk.Treeview(self)
        self.tree["show"] = "headings"
        self.tree.pack()

    def setColomns(self,columns):
        """
        テーブルの列名を指定
        """
        self.columns = columns
        self.tree["columns"] = self.columns
        for col in columns:
            self.tree.heading(col,text=col)

    def setRow(self,index ="" ,row_data=[]):
        """
        新規レコードの挿入
        """
        self.tree.insert("",index="end",text=index,values = row_data)

    def setRows(self,rows_data):
        """
        複数の新規レコードの挿入
        """
        for i,row_data in enumerate(rows_data):
            self.setRow(index = i,row_data = row_data)

    def setSampleData(self):
        """
        起動時のサンプルデータ
        """
        column_data = ("Name","Value")
        rows_data = [("None","None")]
        self.deleteRows()
        self.setColomns(column_data)
        self.setRows(rows_data)

    def deleteRows(self):
        """
        レコードの全削除
        """
        children = self.tree.get_children("")
        for child in children:
            self.tree.delete(child)

    def addSelectAction(self,func):
        """
        レコードが選択されたときに呼ばれるイベントを登録
        """
        self.tree.bind("<<TreeviewSelect>>",func)
    def getItem(self):
        """
        現在選択状態のレコードの取得
        """
        self.selcted_iid = self.tree.focus()
        return self.tree.item(self.selcted_iid,"values")
    def getRows(self):
        """
        全レコードの取得
        """
        rows =[]
        children = self.tree.get_children("")
        for child in children:
            item = self.tree.item(child,"values")
            rows.append(item)
        return rows

    def getColumn(self):
        """
        列名の取得
        """
        return self.columns

    def getDataMap(self):
        """
        現在選択されているレコードの
        列名と値のマップを取得
        """
        item = self.getItem()
        if len(self.columns) != len(item):
            return {"none":"none"}
        else:
            data_map = {}
            for i,column in enumerate(self.columns):
                data_map[column] = item[i]
            return data_map

    def updateValue(self,iid,new_values):
        """
        値の更新
        """
        self.tree.item(self.iid,values=new_values)
    def updateValue(self,new_values):
        """
        現在選択されているレコードの値の更新
        """
        self.tree.item(self.selcted_iid,values=new_values)
    def update(self,value_dict):
        """
        マップからリストに変更後
        値の更新
        """
        data =[]
        for column in self.columns:
            data.append(value_dict[column])
        self.updateValue(data)

    def insert(self,value_dict):
        """
        マップからリストに変更後
        新規レコードの挿入
        """
        data =[]
        for column in self.columns:
            data.append(value_dict[column])
        children = self.tree.get_children("")
        index = len(children)
        self.setRow(index = str(index), row_data=data)

class LabelEntryWidget(ttk.Frame):
    """
    LabelとEntryがくっついたWidget
    """
    def __init__(self, master,text="property"):
        super().__init__(master)
        self.value = StringVar()
        self.createWidgets(text)

    def createWidgets(self,text="property"):
        self.label = ttk.Label(self,text=text)
        self.label.pack(side="left")
        self.entry = ttk.Entry(self,textvariable=self.value)
        self.entry.pack(side="left")

    def getVar(self):
        """
        値を取得するためのWidget変数の取得
        """
        return self.value


    def setLabelOption(self,key_dict):
        """
        Labelのオプション指定(オプションはdictで渡す)
        """
        for k in key_dict.keys():
            self.label[k] = key_dict[k]


    def setEntryOption(self,key_dict):
        """
        Entryのオプション指定(オプションはdictで渡す)
        """
        for k in key_dict.keys():
            self.entry[k] = key_dict[k]


class PropertyView(ttk.Frame):
    """
    選択されたレコードの内容を修正、
    新規レコードなどを挿入するフレーム
    """
    def __init__(self,master):
        super().__init__(master)
        self.pack()
        self.param_dict={}

    def createWidget(self,columns):
        """
        列の要素数分入力ボックスの作成
        """
        self.delete()
        self.param_dict ={}
        for column in columns:
            option = {"width":10}
            param = LabelEntryWidget(self,text = column)
            param.setLabelOption(option)
            param.pack()
            self.param_dict[column] = param.getVar()
        self.createInsertUpdateButton()
        self.createSaveButton()

    def createInsertUpdateButton(self):
        """
        更新ボタンと挿入ボタンを作成
        """
        button_frame = ttk.Frame(self)
        button_frame.pack(anchor="e")
        self.update_button = update = ttk.Button(button_frame,text = "commit")
        self.insert_button = insert = ttk.Button(button_frame,text = "insert")
        update.pack(side="left")
        insert.pack(side="left")

    def createSaveButton(self):
        """
        保存ボタンを作成
        """
        save_frame = ttk.Frame(self)
        save_frame.pack(anchor="e")
        self.save_button = save = ttk.Button(save_frame,text = "Save")
        save.pack(side="left")

    def delete(self):
        """
        更新時用
        自身のフレームに紐づく子Widgetの削除
        """
        children = self.winfo_children()
        for child in children:
            child.destroy()

    def setUpdateButtonCommand(self,command):
        self.update_button["command"] = command

    def setInsertButtonCommand(self,command):
        self.insert_button["command"] = command

    def setSaveButtonCommand(self,command):
        self.save_button["command"] = command

    def setParameter(self,param):
        """
        取得したレコードデータを各入力ボックスのWidget変数に振り分け
        """
        for key in self.param_dict.keys():
            self.param_dict[key].set(param[key])

    def getParameter(self):
        """
        列名とWidget変数の値をマップにして返す
        """
        param_dict = {}
        for key,value in self.param_dict.items():
            param_dict[key] = value.get()
        return param_dict


class CSVView(ttk.Frame):
    """
    CsvViewerのメインView

    """
    def __init__(self, master):
        super().__init__(master,borderwidth=10)
        self.tree = None
        self.createWidget()
        self.setAction()
        self.pack()

    def createWidget(self):
        """
        viewの組み立て
        """
        self.createUpperFrame()
        self.createLowerFrame()

    def createUpperFrame(self):
        """
        Csv読み込み用フレーム
        """
        upper_frame = ttk.Frame(self)
        upper_frame.pack()
        self.file_path_frame = FileOpenFrame(upper_frame)

    def createLowerFrame(self):
        """
        Treeviewとレコード編集Widget用フレーム
        """
        lower_frame = ttk.Frame(self)
        lower_frame.pack()
        left_frame = ttk.LabelFrame(lower_frame,text="CsvData")
        left_frame.pack(side="left")
        self.tree = TreeView(left_frame)
        right_frame = ttk.LabelFrame(lower_frame,text="RowData")
        right_frame.pack(side = "right",anchor="n")

        self.property = PropertyView(right_frame)
        self.property.createWidget(self.tree.getColumn())


    def setAction(self):
        """
        ツリーアイテム選択アクションの登録
        """
        def _updateCommand():
            """
            更新アクション
            """
            param = self.property.getParameter()
            print(param)
            self.tree.update(param)
        def _insertCommand():
            """
            挿入アクション
            """
            param = self.property.getParameter()
            self.tree.insert(param)

        def _func(event):
            """
            レコード選択アクション
            レコード選択ごとに更新インサートコマンドを登録しなおす
            """
            self.property.setParameter(self.tree.getDataMap())
            self.property.setUpdateButtonCommand(_updateCommand)
            self.property.setInsertButtonCommand(_insertCommand)

        self.tree.addSelectAction(_func)

    def getFilePath(self):
        """
        ファイルパスの取得
        """
        return self.file_path_frame.getFilePath()
    def setReadButtonCommand(self,func):
        """
        読み込みボタンコマンド登録
        """
        self.file_path_frame.setReadButtonCommand(func)
    def setNewColumnAndData(self,columns,rows):
        """
        新しい列名とレコードを設定する。
        プロパティのWidgetも更新する。
        """
        self.tree.deleteRows()
        self.tree.setColomns(columns)
        self.tree.setRows(rows)
        self.property.createWidget(self.tree.getColumn())

    def setSaveButtonCommand(self,func):
        """
        保存ボタンコマンド登録
        """
        self.property.setSaveButtonCommand(func)
    def getColumns(self):
        """
        列名リスト取得
        """
        return self.tree.getColumn()
    def getRows(self):
        """
        レコードリスト取得
        """
        return self.tree.getRows()

if __name__ == '__main__':
    master = Tk()
    master.title("csvview")
    CSVView(master)
    master.geometry("800x400")
    master.mainloop()