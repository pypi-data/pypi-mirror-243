import logging
import re
import httpx
import logging
import threading
import time
import queue
from rich.logging import RichHandler

from tenacity import retry,stop_after_attempt,wait_fixed

import ofscraper.utils.paths as paths
import ofscraper.utils.config as config_
import ofscraper.utils.args as args
import ofscraper.utils.console as console
import ofscraper.constants as constants
senstiveDict={}
discord_queue=queue.Queue()


class DebugOnly(logging.Filter):
    def filter(self, record):
        if record.levelname=="DEBUG" or record.levelname=="TRACEBACK":
            return True
        return False
class NoDebug(logging.Filter):
    def filter(self, record):
        if record.levelname=="DEBUG" or record.levelname=="TRACEBACK":
            return False
        return True
class DiscordHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        log_entry = self.format(record)
        url=config_.get_discord(config_.read_config())
        log_entry=f"{log_entry}\n\n"
        if url==None or url=="":
            return
        #convert markup
        log_entry=re.sub("\[bold\]|\[/bold\]","**",log_entry)
        discord_queue.put((url,log_entry))



class TextHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self._widget=None
    def emit(self, record):
        # only emit after widget is set
        if self._widget==None:
            return
        log_entry = self.format(record)
        log_entry=f"{log_entry}"
        self._widget.write(log_entry)
        
    @property
    def widget(self):
        return self._widget
    @widget.setter
    def widget(self,widget):
        self._widget=widget


def discord_messenger():
    with httpx.Client() as c:
        while True:
            url,message=discord_queue.get()   
            if url=="exit":
                return
            try:
                discord_pusher(url,message,c)
            except httpx.HTTPError as E:
                console.shared_console.print("Discord Error")

@retry(stop=stop_after_attempt(constants.NUM_TRIES),wait=wait_fixed(constants.DISCORDWAIT),reraise=True) 
def discord_pusher(url,message,c):
    c.post(url, headers={"Content-type": "application/json"},json={"content":message})



def discord_cleanup():
    logging.getLogger("ofscraper").info("Pushing Discord Queue")
    with httpx.Client() as c:
        while True:
            if discord_queue.empty:
                discord_queue.put(("exit",None))
                break
            time.sleep(.5)
             
def start_discord_queue():
    worker_thread = threading.Thread(target=discord_messenger)
    worker_thread.start()
class SensitiveFormatter(logging.Formatter):
    """Formatter that removes sensitive information in logs."""
    @staticmethod
    def _filter(s):
        if s.find("Avatar :")!=-1:
            None
        else:
            s=re.sub("&Policy=[^&\"]+", "&Policy={hidden}", s)
            s=re.sub("&Signature=[^&\"]+", "&Signature={hidden}", s)
            s=re.sub("&Key-Pair-Id=[^&\"]+", "&Key-Pair-Id={hidden}", s)
            for ele in senstiveDict.items():
                s=re.sub(re.escape(str(ele[0])),str(ele[1]),s)
        return s

    def format(self, record):
        original = logging.Formatter.format(self, record)  # call parent method
        return self._filter(original)


class LogFileFormatter(SensitiveFormatter):
    """Formatter that removes sensitive information in logs."""

    @staticmethod
    def _filter(s):
        s=SensitiveFormatter._filter(s)
        s=re.sub("\[bold\]|\[/bold\]","",s)
        return s
    


def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG+5):
            self._log(logging.DEBUG+5, message, args, **kwargs)
def logToRoot(message, *args, **kwargs):
        logging.log(logging.DEBUG+5, message, *args, **kwargs)   

def addtrackback():

    logging.addLevelName(logging.DEBUG+5, "TRACEBACK")
    logging.TRACEBACK = logging.DEBUG+5
    setattr(logging.getLoggerClass(),"traceback", logForLevel)
    setattr(logging, "traceback",logToRoot)

def updateSenstiveDict(word,replacement):
     global senstiveDict
     senstiveDict[word]=replacement


def getLevel(input):
    """
    CRITICAL 50
    ERROR 40
    WARNING 30
    INFO 20
    DEBUG 10
    """
    return {"OFF":100,
            "PROMPT":"CRITICAL",
            "STATS":"ERROR",
            "LOW":"WARNING",
            "NORMAL":"INFO",
            "DEBUG":"DEBUG"}.get(input,100)

def init_logger(log):
    format=' \[%(module)s.%(funcName)s:%(lineno)d]  %(message)s'
    log.setLevel(1)
    addtrackback()
    # # #log file
      # #discord
    cord=DiscordHandler()
    cord.setLevel(getLevel(args.getargs().discord))
    cord.setFormatter(SensitiveFormatter('%(message)s'))
    #console
    sh=RichHandler(rich_tracebacks=True,markup=True,tracebacks_show_locals=True,show_time=False,show_level=False,console=console.shared_console)
    sh.setLevel(getLevel(args.getargs().output))
    sh.setFormatter(SensitiveFormatter(format))
    sh.addFilter(NoDebug())
    tx=TextHandler()
    tx.setLevel(getLevel(args.getargs().output))
    tx.setFormatter(SensitiveFormatter(format))
    log.addHandler(cord)
    log.addHandler(sh)
    log.addHandler(tx)
    if args.getargs().log!="OFF":
        stream=open(paths.getlogpath(), encoding='utf-8',mode="a",)
        fh=logging.StreamHandler(stream)
        fh.setLevel(getLevel(args.getargs().log))
        fh.setFormatter(LogFileFormatter('%(asctime)s - %(message)s',"%Y-%m-%d %H:%M:%S"))
        fh.addFilter(NoDebug())
        log.addHandler(fh)

    
    if args.getargs().output=="DEBUG":
        sh2=RichHandler(rich_tracebacks=True, console=console.shared_console,markup=True,tracebacks_show_locals=True,show_time=False)
        sh2.setLevel(args.getargs().output)
        sh2.setFormatter(SensitiveFormatter(format))
        sh2.addFilter(DebugOnly())
        log.addHandler(sh2)
    if args.getargs().log=="DEBUG":
        fh2=logging.StreamHandler(stream)
        fh2.setLevel(getLevel(args.getargs().log))
        fh2.setFormatter(LogFileFormatter('%(asctime)s - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S"))
        fh2.addFilter(DebugOnly())
        log.addHandler(fh2)
    

    return log


def add_widget(widget):
    [setattr(ele,"widget",widget) for ele in list(filter(lambda x:isinstance(x,TextHandler),logging.getLogger("ofscraper").handlers))]
