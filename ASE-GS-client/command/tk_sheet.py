import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tksheet import Sheet
from collections import deque

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
        self.sheet = Sheet(root, width=600, height=200)  # サイズを指定
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

        # デフォルトの100行100列を設定
        self.default_data = [["" for _ in range(100)] for _ in range(100)]
        self.sheet.set_sheet_data(data=self.default_data)
        
        # FIFO配列の設定
        self.fifo_queue = deque(maxlen=10)  # ここで最大長を設定

        # ボタンの追加
        self.add_button = tk.Button(root, text="Add Selected Row", command=self.add_selected_row)
        self.add_button.grid(row=1, column=0, sticky='we')
        self.show_button = tk.Button(root, text="Show FIFO Queue", command=self.show_fifo_queue)
        self.show_button.grid(row=2, column=0, sticky='we')

        # FIFOの内容を表示するテキストボックス
        self.fifo_text = tk.Text(root, height=10, state='disabled')
        self.fifo_text.grid(row=3, column=0, sticky='nswe')

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                data = df.values.tolist()
                headers = df.columns.tolist()

                # CSVの行数・列数を取得
                csv_rows = len(data)
                csv_cols = len(headers)

                # デフォルトの行数・列数を100にする
                for _ in range(csv_rows, 100):
                    data.append(["" for _ in range(csv_cols)])
                for row in data:
                    row.extend(["" for _ in range(csv_cols, 100)])

                # データとヘッダーをシートに設定
                self.sheet.set_sheet_data(data=data)
                self.sheet.headers(headers)
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

    def add_selected_row(self):
        selected_indices = self.sheet.get_currently_selected()
        if selected_indices:
            selected_row_index = selected_indices[0]
            selected_row_data = self.sheet.get_row_data(selected_row_index)
            # 空のセルを除外してCSV形式に変換
            csv_row_data = [str(cell) for cell in selected_row_data if cell != ""]
            csv_row = ",".join(csv_row_data)
            self.fifo_queue.append(csv_row)
            print(f"Added row {selected_row_index}: {csv_row}")
            self.update_fifo_text()
        else:
            messagebox.showwarning("Warning", "No row selected")

    def update_fifo_text(self):
        self.fifo_text.config(state='normal')
        self.fifo_text.delete(1.0, tk.END)
        for index, row in enumerate(self.fifo_queue):
            self.fifo_text.insert(tk.END, f"Row {index}: {row}\n")
        self.fifo_text.config(state='disabled')

    def show_fifo_queue(self):
        for index, row in enumerate(self.fifo_queue):
            print(f"Row {index}: {row}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditor(root)
    root.mainloop()
