import threading
from queue import Queue,Empty
import logging
import ctypes
import time

logging.basicConfig(level=logging.DEBUG,
		format ='%(asctime)s %(thread)d %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt ='%a, %d %b %Y %H:%M:%S',
		filename = 'download.log',
		filemode = 'a')

class worker_thread(threading.Thread):
	def __init__(self,worker_queue,result_queue):
		super(worker_thread,self).__init__()
		self.worker_queue = worker_queue
		self.result_queue = result_queue

		self.state = True 
		self.setDaemon(True)


	def run(self):
		logging.info("thread  %d starting"%(self.ident))
		try:
			while self.state is True:
				try:
					func,args,kargs = self.worker_queue.get(True,2)

				
					logging.info("%d has got a download job"%(self.ident))

					result = func(*args,**kargs)

					if result != None:
						self.result_queue.put(result)

					self.worker_queue.task_done()

				except Empty:
					continue

			

		except SystemExit :
			logging.info("thread  %d  has  exited "%(self.ident))


		
				
								
				


class thread_pool():
	def __init__(self,thread_num):
		self.thread_num = thread_num
		self.worker_queue = Queue(maxsize=100)
		self.result_queue = Queue(maxsize=100)
		self.threads=[]
		self.init_threads()
	
	def init_threads(self):
		for i in range(self.thread_num):
			self.threads.append(worker_thread(self.worker_queue,self.result_queue))
	

	def start_all(self):
		logging.info("main thread sends a start_all command")
		for t in self.threads:
			t.start()	
	

	def stop_all(self):
		logging.info("main thread  sends a stop_all command")
		for t in self.threads:
			if(t.is_alive()):
				self.ctype_async_raise(t.ident,SystemExit)
				if(t.is_alive()):
					t.join()
	

	def add_job(self,func,*args,**kargs):
		self.worker_queue.put((func,args,kargs))
	
	def wait_all_complete(self):
		while True:
			alive = False
			for i in self.threads:
				alive = alive or i.is_alive()
				if not alive:
					break
##########      do not use join() to wait for finish,because join will block the main thread,
##########      so the main thread can not catch  KeyboardInterrupt.
##########      PyThreadState_SetAsyncExc  is not a magic bullet because if the thread is busy outside the python interpreter, 
##########      it will not catch the interruption.

#		for t in self.threads:
#			if t.is_alive():
#				t.join()	
#
	def ctype_async_raise(self,thread_tid,exception):
		ret  = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_tid,ctypes.py_object(exception))

	
