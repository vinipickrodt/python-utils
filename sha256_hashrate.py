#!/usr/bin/python

import threading
import time
import hashlib
from multiprocessing import Process

threadLock = threading.Lock()

def test(loops):
	t = time.time()
	for x in xrange(loops):
		hashlib.sha256(str(x))
	return time.time() - t

class Sha256Thread (threading.Thread):
	def __init__(self, loops):
		threading.Thread.__init__(self)
		self.loops = loops
	def run(self):
		#print "Starting " + self.name
		# Get lock to synchronize threads
		#threadLock.acquire()
		test(self.loops)
		# Free lock to release next thread
		#threadLock.release()

def run():
	loops = 1200000
	thread_count = 4
	
	start_time = time.time()
	#threads = [ Sha256Thread(loops) for x in xrange(thread_count) ]
	threads = [ Process(target=test, args=(loops, )) for x in xrange(thread_count) ]
	
	for t in threads:
		t.start()
	
	for t in threads:
		t.join()
	
	tempo = time.time() - start_time
	
	print "Tempo: " + str(tempo) + " --- HashRate: " + str((loops * thread_count) / tempo) + "sec"

if __name__ == '__main__':
	for x in xrange(10):
		run()
