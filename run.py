from IPScanner import Scanner
from time import time as now
start = now()
scanner = Scanner()

# print(scanner.baseIP)
# print(scanner.mask)
# print(scanner.hosts)


scanner.scanAlive()
stop = now()
print(stop-start)
#scanner.ping('10.0.0.5')

print(scanner.aliveHosts)

