from time import sleep
import threading

class ThreadManager:
    def __init__(self,maxThread,**kwargs):
        self.maxThread = maxThread
        self.delay = kwargs.get('delay',.001)
        self.threadCount = 0
        
    def queueThread(self,**kwargs):
 
        t = ThreadWrap(target=self._startThread,threadArgs=kwargs)

        while self.threadCount >= self.maxThread:
            sleep(self.delay)
        
        
        t.start()

        return t

    def _startThread(self,threadArgs):
        fxn = threadArgs['target']
        args = threadArgs['args']

        self.threadCount += 1
        fxn(*args)
        self.threadCount -= 1

        
class ThreadWrap:
    def __init__(self,**kwargs):
        self.target = kwargs['target']
        self.args = kwargs['threadArgs']
        self.delay = kwargs.get('delay',.001)
        self.isStarted=False
        self.thread = self._genThread()


    def _genThread(self):
        return threading.Thread(target=self.target,args=(self.args,))

    def start(self):
        self.isStarted = True
        self.thread.start()

    def join(self):
        while not self.isStarted:
            sleep(self.delay)
        return self.thread.join()

            


    

        

