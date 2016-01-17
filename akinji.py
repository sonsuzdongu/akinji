#!/usr/bin/env python

""" 
    Example usage:
    $ python akinji.py -n 100 -c 30 http://google.com
"""

__appName__ = "Akinji - Socket.io Stress testing tool"
__version__ = '0.0.1'

from threading import Thread
from optparse import OptionParser
from socketIO_client import SocketIO
import time

class Akinji:
    def __init__(self):
        options, args = self.parseOptions()
        
	startTime = time.time()
        threadList = []
        concurrentRequestCount = options.concurrentRequestCount

        for count in range(0, concurrentRequestCount):
            currentThread = AkinjiThread(count, options.host, options.port, options.waitFor, options.onMsg)
            threadList.append(currentThread)
            currentThread.start()

        # join threads
        for thread in threadList:
            try:
                thread.join()
            except Exception, error:
                print error;

        # end time tracker
        endTime = time.time()

        """ print results """
        totalRequstTime = endTime - startTime
        perRequst = totalRequstTime / options.concurrentRequestCount
        print " ------------------------------------------------- "
        print "Process took ", totalRequstTime , "seconds"


    """ print usage and help """
    def parseOptions(self):
        usage = "usage: %prog -c concurrentRequestCount --host host --port port --waitFor wait --on on_msg"
        parser = OptionParser(usage=usage, version=__appName__+" "+__version__)
        parser.add_option("-c", "--concurrentRequestCount", action="store", type="int", 
                          default=1, dest="concurrentRequestCount", help="input number of concurrent requests")

        parser.add_option("-H", "--host", action="store", type="string", 
                          default="localhost", dest="host", help="socket host")


        parser.add_option("-p", "--port", action="store", type="int", 
                          default=3000, dest="port", help="socket port")


        parser.add_option("-w", "--waitFor", action="store", type="int", 
                          default=3, dest="waitFor", help="socket waiting time")


        parser.add_option("-o", "--on", action="store", type="string", 
                          default=None, dest="onMsg", help="message key to listen")


        (options, args) = parser.parse_args()

        return options, args


""" Threads to send requests """
class AkinjiThread(Thread):
    def __init__ (self, count, host, port, waitFor, onMsg):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.waitFor = waitFor
        self.onMsg = onMsg
	
	print "trying socket #", count

    def run(self):

        try:
            def onMessage(*args):
                print "msg->", args
           
            socketIO = SocketIO(self.host, self.port)
	    socketIO.on(self.onMsg, onMessage);
	    socketIO.wait(seconds=self.waitFor)
	    self.completed = True
        except Exception, error:
            self.completed = False

if __name__ == '__main__':
    Akinji()
