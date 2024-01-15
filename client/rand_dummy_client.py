import json
import time
import write_db
import create_json
import sys

database = write_db.WriteDb()
cnt = 0

while True:
    print("Create rand json...")
    create_json.Create_Json()
    print("sending...")
    try: 
        with open('dummy_rand.json', 'r') as f:
            json_data = json.load(f)
            database.write(json_data)
            cnt += 1
    except KeyboardInterrupt:
        sys.exit
    except:
        print(json_data)
        print("DBWriteError")
        continue

    if cnt == 100:
        print("設定された実行数です")
        sys.exit()
    #time.sleep(0.001)