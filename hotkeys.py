import os, signal
import subprocess
import easygui
import psutil
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
 
  def __init__(self, fileToSearch: FileToSearch, config: Config) -> None:
    self.choosingFile = False
    self.paused = False
    self.__fileToSearch = fileToSearch
    self.__config = config
    
    self.__bindings = [
        ["home, home", None, self.change_file, True],
        ["pause, pause", None, self.toggle_pause, True]
    ]
    
  def start(self):
    register_hotkeys(self.__bindings)
    start_checking_hotkeys() 
    self.start_move_with_cursor_process() 
    
  def toggle_pause(self):
    self.paused = not self.paused
    if (self.paused):
      self.kill_move_with_cursor_process()
      return
    self.start_move_with_cursor_process()
    
  def change_file(self):
    self.choosingFile = True
    easygui.msgbox(title=title, msg="Certifique-se que o arquivo de imagem seja capturado de tal forma que apenas o centro dela seja visível (excluir partes irrelevantes como grama, areia, etc)\n\n" +
              "Utilize as seguintes teclas de atalho do windows para fazer a captura da imagem: SHIFT+Window+S\n\n"     
              "Veja o arquivo image_capture_example.mp4 para mais detalhes.")
    
    if (self.__config['show_video_tutorial'] == True):
      startfile("image_capture_example.mp4")
      self.__config['show_video_tutorial'] = False
    
    path = easygui.fileopenbox(
      title="Escolha o arquivo de imagem que deseja procurar", 
      default=".png", 
      filetypes=["*.png", "*.jpg"])
    
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
