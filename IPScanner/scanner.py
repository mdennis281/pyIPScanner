import threading
import ping3
from IPScanner.nethelper import NetHelper
from IPScanner.threadmanager import ThreadManager

MAXTHREAD = 200
TM = ThreadManager(MAXTHREAD)

class Scanner:
    def __init__(self,**kwargs):
        self.baseIP = kwargs.get('baseIP', NetHelper.getIP())
        self.mask = kwargs.get('mask','24')
        self.hosts = []
        self.aliveHosts = {}
        
        network = str(self.baseIP) + '/' + str(self.mask)

        self.hosts = NetHelper.getHosts(network)

    def testPorts(self,ip):
        threads = []
        for port in range(1,65535):
            t = TM.queueThread(target=self.testPort,args=(ip,port))
            threads.append(t)
            # threads[-1].start()
        for t in threads:
            t.join()

    def testPort(self,ip,port):
        result = NetHelper.testPort(ip,port)
        if result is not None:
            self.aliveHosts[ip]['ports'][port] = result

    def ping(self, ip):
        p = ping3.ping(ip)
        isAlive = True if p else False

        if isAlive:
            self.aliveHosts[ip] = {'ports':{},'host':NetHelper.getHost(ip),'isFinished':False}
            self.testPorts(ip)
            self.aliveHosts[ip]['isFinished'] = True
            print("{} scanned. {}".format(ip,self.computePercentScanned()))
        return isAlive

    def computePercentScanned(self):
        totalIPs = len(self.aliveHosts.keys())
        scannedIPs = 0
        for ip,ipInfo in self.aliveHosts.items():
            if ipInfo['isFinished']:
                scannedIPs += 1
        return round((scannedIPs/totalIPs)*100,0)

    def scanAlive(self,hosts=None):
        hosts = hosts if hosts else self.hosts
        threads = []
        for host in hosts:
            t = TM.queueThread(target=self.ping,args=(host, ))
            threads.append(t)
            #threads[-1].start()
        for t in threads:
            t.join()



