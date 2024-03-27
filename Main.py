from time import sleep
import winsound
import easygui
import pyautogui  
import json
import psutil
import win32ui, win32con
from python_imagesearch.imagesearch import imagesearch, imagesearch_click
from config import Config
from file_to_search import FileToSearch
from hotkeys import HotKeysService
from constants import *

def make_sure_total_battle_is_running():
    found = tb_process_name in (p.name() for p in psutil.process_iter())

    if (not found):
      win32ui.MessageBox('Total Battle was not found. Please, start it before use MercFinder', title, win32con.MB_OK)
      exit()

class Main:
  __config: Config
  __fileToSearch: FileToSearch
  __hotkeyService: HotKeysService
  
  def __init__(self, config: Config, fileToSearch: FileToSearch, hotKeyService: HotKeysService) -> None:
    self.__config = config
    self.__fileToSearch = fileToSearch
    self.__hotkeyService = hotKeyService
    
  def make_sure_stop_when_found(self) -> None:
    if (config['stop_when_found']):
      casaEncontrada = win32ui.MessageBox("Você está vendo a casa de troca?", "Casa Encontrada", win32con.MB_SYSTEMMODAL + win32con.MB_YESNO)
                
      if (casaEncontrada == win32con.IDYES):
        pyautogui.click(button='middle')
        imagesearch_click(self.__fileToSearch.filename, action="left", delay=1.5, precision=config['precision'])
        pyautogui.leftClick()
                  
        sleep(5)
                  
      sleep(1)

  def main_loop(self):
      while self.__hotkeyService.running:
        if (self.__hotkeyService.choosingFile == True):
          sleep(1)
          continue
            
        self.__hotkeyService.wait_to_continue()
            
        pos = imagesearch(self.__fileToSearch.filename, precision=self.__config['precision'])
            
        if pos[0] != -1:
            winsound.Beep(self.__config['alert_frequency'], self.__config['alert_duration_ms'])
                
            self.make_sure_stop_when_found()
            del pos
                
        sleep(self.__config['wait_time'])
  
make_sure_total_battle_is_running()
 
easygui.msgbox(title=title, msg="Este é um programa em desenvolvimento para busca de qualquer imagem em sua tela.\n\n"+
               "Para trocar a imagem padrão aperte a tecla HOME 2x e siga as instruções\n\n"+
               "Para pausar a execução da busca, aperte a tecla PAUSE 2x e para continuar, novamente PAUSE 2x\n\n"+
               "Para capturar uma nova região a procurar, aperte a tecla CTRL + M 2x e siga as instruções\n\n"+
               "Você pode utilizar as teclas W, A, S e D para fazer rolagem na tela\n\n"+
               "Para sair da aplicação, aperte a tecla DEL 2x")

with open("config.json", "r") as file:
    config: Config = json.load(file)
    
    filename = str.format("Images\{}", default_image_filename)
    
    fileToSearch = FileToSearch(filename)

    hotkeysService = HotKeysService(fileToSearch, config)
    
    main = Main(config, fileToSearch, hotkeysService)

    hotkeysService.start()
    
    try:
        main.main_loop()
    except KeyboardInterrupt:
        print('\n')
  
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)    
