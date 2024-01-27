import json
import sys
import time
import os

class CsvLogger:
   def __init__(self):
      os.makedirs("data", exist_ok=True)
      filename = time.strftime("data/%m%d_%H%M.csv")
      self.file = open(filename, "a")
      self.first = True

   def write_legend(self, json_data):
      self.file.write("time,")
      for tagkey,apps in json_data.items():
         for fieldkey,values in apps.items():
            self.file.write(tagkey+'_'+fieldkey)
            self.file.write(",")
      self.file.write("\n")

   def write_data(self, json_data):
      if self.first:
         self.write_legend(json_data)
         self.first = False
      self.file.write('{:.1f}'.format(time.time()))
      for tagkey, apps in json_data.items():
         for fieldkey, values in apps.items():
            self.file.write(str(values))
            self.file.write(",")
      self.file.write("\n")
   
   def close(self):
      self.file.close()
