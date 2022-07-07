import socket
import ipaddress

class NetHelper:
    
    @staticmethod
    def getIP():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]


    @staticmethod
    def testPort(ip,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
         
        # returns an error indicator
        result = s.connect_ex((ip,port))


        s.close()

        if result == 0:
            return {'service':NetHelper.getPortService(port)}

        return None

        

    @staticmethod
    def getPortService(port):
        try:
            return socket.getservbyport(port)
        except OSError:
            return None

    @staticmethod
    def getHost(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return None

    @staticmethod
    def getHosts(network):
        return [str(ip) for ip in ipaddress.IPv4Network(network,False)]