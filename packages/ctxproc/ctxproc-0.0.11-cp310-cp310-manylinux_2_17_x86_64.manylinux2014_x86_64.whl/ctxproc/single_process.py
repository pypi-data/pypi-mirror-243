import os ; 
import ctypes; 
import mmap ; 
import queue ;
import signal ;
import traceback ; 
import signal ;
import time ;
import numpy as np ; 
import multiprocessing as mp ;
import setproctitle ;

def clear_queue(q): 
  while(not q.empty()) : q.get(); 

def sigint_handler(signum, frame): global stop ; stop = True ; 


class _PrintContent: 
  def __init__(self): self.clear();  
  def xprint(self,*ws , end = '\n') : 
    for w in ws : 
      try :  self.print_content+=str(w) ; 
      except : pass ;
    self.print_content+=end;
  def clear(self): 
    self.print_content = ""; 


def single_process_main(name , qi, qo) : 
  """
    This is the main loop of a single process
    
    Parametrs : 
    _______________________
    qi is the input queue for this main function
    while qo is the output queue for this 
  """
  

  if(None != name ) : setproctitle.setproctitle(name);
  signal.signal(signal.SIGINT,sigint_handler);
  pc = _PrintContent() ; 
  _globals = {
    "xprint" : pc.xprint  
  } ;  # global dictionary
  _locals = {}  ; # local dictionary

  process_worker_running = True  ; 

  while(process_worker_running) :  
    pc.clear();
    try :
      W = qi.get(timeout = 0.01)  ; 
      if(isinstance(W, str)) : W = [W];

      for w in W : 
        if(isinstance(w, str)) :
          _locals = {} ; 
          exec(w, _globals, _locals  ) ; 
          _globals.update(_locals)
        elif(isinstance(w,dict)) : 
          _globals.update(w) ;
      qo.put( ["SUCCESS", pc.print_content , "" ]  )
    except queue.Empty: pass 
    except KeyboardInterrupt: pass ;
    except Exception as e :
        info = str(traceback.format_exc());
        qo.put( ["EXCEPTION", pc.print_content , info ]  )
  return 0 ; 


class SingleProcess: 
  def __init__(self,name = None ) : 
    self.qi =  mp.Queue(); 
    self.qo =  mp.Queue(); 
    self.proc = mp.Process(target = single_process_main , args = (name , self.qi, self.qo) )  
    self.proc.start() ;

  def blocked_put(self, w ): 
    self.qi.put(w) ; 
    return self.qo.get()

