import os, signal
import subprocess
import easygui
import numpy as np
import psutil
import cv2
import pyautogui
from constants import *
from config import Config
from file_to_search import FileToSearch
from constants import title
from os import startfile
from time import sleep
from global_hotkeys import *

class HotKeysService:
  __fileToSearch: FileToSearch
  __config: Config
  __bindings = []
  choosingFile: bool
  paused: bool
  running: bool
 
  def __init__(self, fileToSearch: FileToSearch, config: Config) -> None:
    self.choosingFile = False
    self.running = True
    self.paused = False
    self.__fileToSearch = fileToSearch
    self.__config = config
    
    self.__bindings = [
        ["home, home", None, self.change_file, True],
        ["pause, pause", None, self.toggle_pause, True],
        ["delete, delete", None, self.exit, True],
        ["control + m, control + m", None, self.capture_image_from_selection, True],
    ]
    
  def start(self):
    register_hotkeys(self.__bindings)
    start_checking_hotkeys() 
    self.start_move_with_cursor_process() 
    
  def stop(self):
    self.running = False
    clear_hotkeys()
    exit()    
    
  def toggle_pause(self):
    self.paused = not self.paused
    if (self.paused):
      self.kill_move_with_cursor_process()
      return
    self.start_move_with_cursor_process()
    
  def change_file(self):
    self.choosingFile = True
    
    path = easygui.fileopenbox(
      title="Escolha o arquivo de imagem que deseja procurar", 
      default=".png", 
      filetypes=["*.png", "*.jpg"])
    
    if (not path is None):
      self.__fileToSearch.filename = path
    
    self.choosingFile = False
    
  def wait_to_continue(self):
    while self.paused:
      sleep(1)  
      
  def kill_move_with_cursor_process(self):
      for p in psutil.process_iter():
        if (p.name() == move_with_cursor_process_name):
          os.kill(p.pid, signal.SIGTERM)
          
  def start_move_with_cursor_process(self):
    subprocess.Popen([move_with_cursor_process_name], stdout=subprocess.PIPE)
    
  def capture_image_from_selection(self):
    self.choosingFile = True
    self.paused = True
    self.kill_move_with_cursor_process()
    
    easygui.msgbox(title=title, msg="Certifique-se que o arquivo de imagem seja capturado de tal forma que apenas o centro dela seja visível (excluir partes irrelevantes como grama, areia, etc)\n\n" +
                   "Quando finalizar a seleção da área que deseja capturar, tecle ENTER\n\n"+
                   "Veja o arquivo image_capture_example.mp4 para mais detalhes.")
    
    if (self.__config['show_video_tutorial'] == True):
      startfile("image_capture_example.mp4")
      self.__config['show_video_tutorial'] = False
    
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    (x,y,w,h) = cv2.selectROI("Selecionar imagem", img=image, fromCenter=False, showCrosshair=False)
    ROI = image[y:y+h, x:x+w]
    
    if easygui.ynbox("Deseja salvar esta imagem?", "Salvar imagem"):
      filename = str.format("{}\Images\{}", os.getcwd(), temp_file_name)
      filename = easygui.filesavebox("Entre com o nome do arquivo", "Salvar imagem", filename, [filename])
      filename = filename if filename != "" else temp_file_name
      cv2.imwrite(filename, ROI)
      self.__fileToSearch.filename = filename
      
    self.choosingFile = False
    
    self.paused = False
    
    cv2.destroyAllWindows()
    
    self.start_move_with_cursor_process()
    pass     
    
  def exit(self):
    self.kill_move_with_cursor_process()
    self.stop()
