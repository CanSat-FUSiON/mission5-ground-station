import json
import threading
import time
import sys
import write_db

# モジュールのインポート
import os, tkinter, tkinter.filedialog, tkinter.messagebox

# ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*")]
iDir = os.path.abspath(os.path.dirname(__file__))
file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
kill_flag = False
f = open(file, mode="r")
class TelemetryLoop:
    global kill_flag
    def __init__(self):
        database = write_db.WriteDb()

        in_json = False
        json_str = ""

        while not kill_flag:
            time.sleep(0.001)
            line_byte = f.readline()
            line_str = ""
            try:
                line_str = line_byte.strip()
                print(line_str)
            except:
                 continue
            if line_str == "{":
                in_json = True
            elif line_str == "}":
                in_json = False
                json_str += "}"
                try:
                    json_data = json.loads(json_str)
                except json.JSONDecodeError:
                    print(json_str)
                    print("JSONDecodeError")
                    json_str = ""
                    continue
                json_str = ""
                try:
                    database.write_bulk(json_data)
                except:
                    print(json_data)
                    print("DBWriteError")
                    continue
            if in_json:
                json_str += line_str
                continue

def close():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        kill_flag=True
        sys.exit

thread_Tlm = threading.Thread(target=TelemetryLoop, daemon=True)
thread_Tlm.start()


close()