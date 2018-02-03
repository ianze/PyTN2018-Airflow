import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('redis', 6379))
    s.close()
    sys.exit(0)

except socket.error as ex:
    sys.exit(1)