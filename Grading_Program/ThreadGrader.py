import queue
import threading
import mysql.connector

class ThreadGrader(threading.Thread):
  """Threaded Url Grab"""
  def __init__(self, q, sql):
    threading.Thread.__init__(self)
    self.queue = q
    self.conn  = sql
    self.cursor = conn.cursor()
  
  def run(self):
    while True:
      #grabs job from queue
      file_name = self.queue.get()
      
      submission = Grader(file_name)
      
      #Get tuple (team_id, problem_number)
      info = submission.extract_info()
      
      #Select row of team_id
      #TODO - Change foo to correct table
      cursor.execute("SELECT * FROM foo WHERE team_id = %d", (info[0]))
      row = cursor.fetchone() #TODO - figure out what 'row' is
                              #  current assumpion - dictionary
      
      #TODO - updates results?   maybe in another thread/queue or program
      #TODO - send back results? maybe in another thread/queue or program
      
      #signals to queue job is done
      self.queue.task_done()