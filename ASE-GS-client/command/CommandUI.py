import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from tksheet import Sheet
import queue

class CSVEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Editor with FIFO Queue")

        self.setup_ribbon()
        self.setup_sheet()
        self.setup_fifo_queue()
        self.setup_send_options()

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_ribbon(self):
        # Create ribbon frame
        self.ribbon = ttk.Notebook(self.root)
        self.ribbon.grid(row=0, column=0, sticky="ew")

        # Create frames for ribbon tabs
        self.file_frame = ttk.Frame(self.ribbon)
        self.ribbon.add(self.file_frame, text="File")

        # Add buttons to the file tab
        self.load_button = ttk.Button(self.file_frame, text="Load CSV", command=self.load_csv)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        self.save_button = ttk.Button(self.file_frame, text="Save CSV", command=self.save_csv)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        self.add_to_fifo_button = ttk.Button(self.file_frame, text="Add to FIFO", command=self.add_to_fifo)
        self.add_to_fifo_button.grid(row=0, column=2, padx=5, pady=5)

        self.send_fifo_button = ttk.Button(self.file_frame, text="Send FIFO", command=self.send_fifo)
        self.send_fifo_button.grid(row=0, column=3, padx=5, pady=5)

        self.clear_fifo_button = ttk.Button(self.file_frame, text="Clear FIFO", command=self.clear_fifo)
        self.clear_fifo_button.grid(row=0, column=4, padx=5, pady=5)
        
    def setup_sheet(self):
        # Create an empty 100x100 sheet
        data = [['' for _ in range(100)] for _ in range(100)]
        headers = [f"Column {i+1}" for i in range(100)]
        
        self.sheet = Sheet(self.root, data=data, headers=headers)
        self.sheet.enable_bindings(("single_select", 
                                    "row_select", 
                                    "column_select", 
                                    "drag_select", 
                                    "arrowkeys", 
                                    "row_height_resize", 
                                    "double_click_column_resize", 
                                    "right_click_popup_menu", 
                                    "rc_select", 
                                    "rc_insert_row", 
                                    "rc_delete_row", 
                                    "rc_insert_column", 
                                    "rc_delete_column", 
                                    "rc_select_delete", 
                                    "copy", 
                                    "cut", 
                                    "paste", 
                                    "delete", 
                                    "undo", 
                                    "edit_cell", 
                                    "edit_header", 
                                    "resize_columns_to_content", 
                                    "resize_rows_to_content"))
        self.sheet.grid(row=1, column=0, sticky="nsew")

    def setup_fifo_queue(self):
        self.fifo_queue = queue.Queue()
        
        self.queue_label = tk.Label(self.root, text="FIFO Queue:")
        self.queue_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.queue_listbox = tk.Listbox(self.root, width=50, height=5)
        self.queue_listbox.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

    def setup_send_options(self):
        self.send_option = tk.StringVar()
        self.send_option.set("ASCII")  # Default option

        self.send_options_frame = ttk.Frame(self.root)
        self.send_options_frame.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        ascii_radio = ttk.Radiobutton(self.send_options_frame, text="ASCII", variable=self.send_option, value="ASCII")
        ascii_radio.grid(row=0, column=0, padx=5, pady=5)

        binary_radio = ttk.Radiobutton(self.send_options_frame, text="Binary", variable=self.send_option, value="Binary")
        binary_radio.grid(row=0, column=1, padx=5, pady=5)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            # Read CSV file, treating empty strings as NaN
            df = pd.read_csv(file_path, na_values=[''])
            # Ensure the DataFrame has at least 100 rows and 100 columns
            df = self.ensure_min_size(df, 100, 100)
            # Replace NaN values with empty string
            df = df.fillna('')
            self.sheet.set_sheet_data(df.values.tolist(), reset_col_positions=True, reset_row_positions=True)
            self.sheet.headers(df.columns.tolist())

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            data = self.sheet.get_sheet_data()
            headers = self.sheet.headers()
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(file_path, index=False)

    def add_to_fifo(self):
        selected_row_indices = self.sheet.get_selected_rows()
        if selected_row_indices:
            for row_index in selected_row_indices:
                row_data = self.sheet.get_row_data(row_index)
                # Filter out empty strings from row_data
                filtered_row_data = [str(cell) for cell in row_data if str(cell).strip()]
                if filtered_row_data:
                    self.fifo_queue.put(filtered_row_data)
                    self.queue_listbox.insert(tk.END, ','.join(filtered_row_data))
                else:
                    print(f"Row {row_index + 1} contains only empty cells and will not be added to FIFO.")
        else:
            print("No row selected")

    def send_fifo(self):
        temp_queue = queue.Queue()
        while not self.fifo_queue.empty():
            row_data = self.fifo_queue.get()
            if self.send_option.get() == "ASCII":
                print(f"ASCII: {','.join(map(str, row_data))}")
            elif self.send_option.get() == "Binary":
                print(f"Binary: {','.join(map(str, row_data))}")
            temp_queue.put(row_data)

        # Put the data back into the original queue
        while not temp_queue.empty():
            row_data = temp_queue.get()
            self.fifo_queue.put(row_data)

    def clear_fifo(self):
        while not self.fifo_queue.empty():
            self.fifo_queue.get()

        self.queue_listbox.delete(0, tk.END)

    def ensure_min_size(self, df, min_rows, min_cols):
        current_rows, current_cols = df.shape

        if current_rows < min_rows:
            additional_rows = min_rows - current_rows
            extra_data = [['' for _ in range(current_cols)] for _ in range(additional_rows)]
            df = pd.concat([df, pd.DataFrame(extra_data)], ignore_index=True)

        if current_cols < min_cols:
            additional_cols = min_cols - current_cols
            extra_columns = [f"Column {current_cols + i + 1}" for i in range(additional_cols)]
            df = pd.concat([df, pd.DataFrame(columns=extra_columns)], axis=1)

        return df

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditorApp(root)
    root.mainloop()
