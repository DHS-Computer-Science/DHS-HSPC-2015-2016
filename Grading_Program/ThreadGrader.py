import queue
import threading
import mysql.connector

class ThreadGrader(threading.Thread):
  """Threaded Url Grab"""
  def __init__(self, q):
    threading.Thread.__init__(self)
    self.queue = q
  
  def run(self):
    while True:
      #grabs job from queue
      submission = self.queue.get()
      
      #TODO - process queue
      
      #TODO - updates results?   maybe in another thread/queue or program
      #TODO - send back results? maybe in another thread/queue or program
      
      #signals to queue job is done
      self.queue.task_done()
