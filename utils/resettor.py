from lib.TorCtl import TorCtl
import time


Tor_conn = TorCtl.connect(controlAddr='localhost', controlPort=9099)

try:
	TorCtl.Connection.send_signal(Tor_conn, "NEWNYM")
except:
	print("Control connection closed. Reconnect ...")
	Tor_conn = TorCtl.connect(controlAddr='localhost', controlPort=9099)
	print "Reset tor ....."
	TorCtl.Connection.send_signal(Tor_conn, "NEWNYM")
