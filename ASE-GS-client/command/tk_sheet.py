import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from tksheet import Sheet
from collections import deque

class CSVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor")
        
        # CSV表示用フレーム
        csv_frame = tk.Frame(root)
        csv_frame.grid(row=0, column=0, sticky='nswe')
        csv_frame.grid_rowconfigure(0, weight=1)
        csv_frame.grid_columnconfigure(0, weight=1)
        
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
        self.sheet = Sheet(csv_frame, width=600, height=200)  # サイズを指定
        self.sheet.enable_bindings(("single_select", "row_select"))  # シングルセル選択のみを許可
        self.sheet.disable_bindings(("rc_select", "arrowkeys"))  # 右クリック選択と矢印キーによる選択を無効化
        self.sheet.extra_bindings([("cell_select", self.on_cell_select)])  # セル選択時のカスタムバインディング
        self.sheet.grid(row=0, column=0, sticky='nswe')
        
        # デフォルトの100行100列を設定
        self.default_data = [["" for _ in range(100)] for _ in range(100)]
        self.sheet.set_sheet_data(data=self.default_data)
        
        # 操作ボタン用フレーム
        button_frame = tk.Frame(root)
        button_frame.grid(row=0, column=1, sticky='ns')
        
        # ボタンの追加
        self.add_button = tk.Button(button_frame, text="Add Selected Row", command=self.add_selected_row)
        self.add_button.pack(fill='x', padx=10, pady=5)
        
        self.show_button = tk.Button(button_frame, text="Show FIFO Queue", command=self.show_fifo_queue)
        self.show_button.pack(fill='x', padx=10, pady=5)
        
        self.clear_button = tk.Button(button_frame, text="Clear FIFO", command=self.clear_fifo)
        self.clear_button.pack(fill='x', padx=10, pady=5)

        # バイナリ/ASCII選択用のラジオボタン
        self.data_type_var = tk.StringVar()
        self.data_type_var.set("ASCII")  # 初期値をASCIIに設定
        self.binary_radio = tk.Radiobutton(button_frame, text="Binary", variable=self.data_type_var, value="Binary")
        self.binary_radio.pack(fill='x', padx=10, pady=5)
        self.ascii_radio = tk.Radiobutton(button_frame, text="ASCII", variable=self.data_type_var, value="ASCII")
        self.ascii_radio.pack(fill='x', padx=10, pady=5)

        # FIFO表示用テキストエリア
        fifo_frame = tk.Frame(root)
        fifo_frame.grid(row=1, column=0, columnspan=2, sticky='nswe')
        fifo_frame.grid_rowconfigure(0, weight=1)
        fifo_frame.grid_columnconfigure(0, weight=1)
        
        self.fifo_text = tk.Text(fifo_frame, height=10, state='disabled')
        self.fifo_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.fifo_queue = deque(maxlen=10)  # FIFO配列の設定

        self.current_file = None

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

    def clear_fifo(self):
        self.fifo_queue.clear()
        self.update_fifo_text()

    def update_fifo_text(self):
        self.fifo_text.config(state='normal')
        self.fifo_text.delete(1.0, tk.END)
        for index, row in enumerate(self.fifo_queue):
            self.fifo_text.insert(tk.END, f"Row {index}: {row}\n")
        self.fifo_text.config(state='disabled')

    def show_fifo_queue(self):
        data_type = self.data_type_var.get()
        if data_type == "Binary":
            for index, row in enumerate(self.fifo_queue):
                print(f"Row {index} (Binary): {self.convert_to_binary(row)}")
        elif data_type == "ASCII":
            for index, row in enumerate(self.fifo_queue):
                print(f"Row {index} (ASCII): {row}")

    def convert_to_binary(self, data):
        # ここにバイナリ変換のロジックを実装する
        pass

    def on_cell_select(self, event):
        # セル選択時のカスタムハンドラー
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditor(root)
    root.mainloop()
