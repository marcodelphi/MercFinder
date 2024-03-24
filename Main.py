from time import sleep
import winsound
import easygui
import pyautogui  
import json
import psutil
import win32ui, win32con
from python_imagesearch.imagesearch import r, imagesearch, imagesearch_click
from config import Config
from file_to_search import FileToSearch
from hotkeys import HotKeysService
from constants import title

found = "TotalBattle.exe" in (p.name() for p in psutil.process_iter())

if (not found):
  win32ui.MessageBox('Total Battle was not found. Please, start it before use MercFinder', title, win32con.MB_OK)
  exit()
  
easygui.msgbox(title=title, msg="Este é um programa em desenvolvimento para busca de qualquer imagem em sua tela.\n\n"+
               "Para trocar a imagem padrão aperte a tecla HOME 2x e siga as instruções\n\n"+
               "Para pausar a execução da busca, aperta a tecla PAUSE 2x e para continuar, novamente PAUSE 2x")
 
with open("config.json", "r") as file:
    config: Config = json.load(file)
    
    fileToSearch = FileToSearch(r"Images\default_image.png")

    hotkeysService = HotKeysService(fileToSearch, config)

    hotkeysService.start()
    
    try:
        while True:
          if (hotkeysService.choosingFile == True):
            sleep(1)
            continue
          
          hotkeysService.wait_to_continue()
          
          pos = imagesearch(fileToSearch.filename, precision=config['precision'])
          
          if pos[0] != -1:
              winsound.Beep(config['alert_frequency'], config['alert_duration_ms'])
              
              if (config['stop_when_found']):
                casaEncontrada = win32ui.MessageBox("Você está vendo a casa de troca?", "Casa Encontrada", win32con.MB_SYSTEMMODAL + win32con.MB_YESNO)
                
                if (casaEncontrada == win32con.IDYES):
                  pyautogui.click(button='middle')
                  imagesearch_click(fileToSearch.filename, action="left", delay=1.5, precision=config['precision'])
                  pyautogui.leftClick()
                  
                  sleep(5)
                  
                sleep(1)
              del pos
              
          sleep(config['wait_time'])
    except KeyboardInterrupt:
        print('\n')
  
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)    
