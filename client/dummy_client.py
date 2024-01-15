import json
import time
import write_db
import sys

database = write_db.WriteDb()

while True:
    print("sending...")
    try: 
        with open('dummy.json', 'r') as f:
            json_data = json.load(f)
            #database.write(json_data)
            database.write_bulk(json_data)
    except KeyboardInterrupt:
        sys.exit
    except:
        print(json_data)
        print("DBWriteError")
        continue
    time.sleep(1)
