import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tksheet import Sheet

class CSVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")
        
        # メニューを作成
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        
        # シートを作成
        self.sheet = Sheet(root)
        self.sheet.enable_bindings((
            "single_select",  # シングルクリックでセルを選択
            "column_select",
            "row_select",
            "toggle_select",  # Ctrl+クリックで選択をトグル
            "drag_select",  # ドラッグでセルを選択
            "column_drag_and_drop",
            "row_drag_and_drop",
            "column_select_and_drag",
            "row_select_and_drag",
            "rc_select",  # 右クリックでセルを選択
            "rc_insert_column",
            "rc_delete_column",
            "rc_insert_row",
            "rc_delete_row",
            "show_insert_column",
            "show_insert_row",
            "show_delete_column",
            "show_delete_row",
            "copy",  # Ctrl+Cでコピー
            "cut",  # Ctrl+Xでカット
            "paste",  # Ctrl+Vでペースト
            "delete",  # Deleteキーで削除
            "undo",  # Ctrl+Zで元に戻す
            "redo",  # Ctrl+Yでやり直す
            "edit_cell"  # ダブルクリックまたはEnterキーでセルを編集
        ))
        self.sheet.grid(row=0, column=0, sticky='nswe')
        
        # レスポンシブなグリッド設定
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.sheet.set_sheet_data(data=df.values.tolist())
                self.sheet.headers(df.columns.tolist())
                self.current_file = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        if self.current_file:
            try:
                headers = self.sheet.headers()
                data = self.sheet.get_sheet_data()
                df = pd.DataFrame(data, columns=headers)
                df.to_csv(self.current_file, index=False)
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                headers = self.sheet.headers()
                data = self.sheet.get_sheet_data()
                df = pd.DataFrame(data, columns=headers)
                df.to_csv(file_path, index=False)
                self.current_file = file_path
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditor(root)
    root.mainloop()
