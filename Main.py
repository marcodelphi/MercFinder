from time import sleep
import winsound
import pyautogui  
import json
from python_imagesearch.imagesearch import imagesearch
 
def remove_percentage(value, percentage):
  valueToRemove = value * percentage
  return value - valueToRemove  

class Config:
  precision: float
  alert_frequency: int
  alert_duration_ms: int

with open("config.json", "r") as file:
    config: Config = json.load(file)
    
    try:
        while True:
          pos = imagesearch(r"Images\exchange-zoom25-4k.png", precision=config['precision'])
          if pos[0] != -1:    
              winsound.Beep(config['alert_frequency'], config['alert_duration_ms'])
              del pos      
    except KeyboardInterrupt:
        print('\n')    
