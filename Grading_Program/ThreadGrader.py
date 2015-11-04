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
      cursor.execute("SELECT * FROM %s WHERE team_id = %d", ('foo', info[0]))
      row = cursor.fetchone() #TODO - figure out what 'row' is
                              #  current assumpion - dictionary
      
      attempt = row['attempts'] #TODO- get the correct number
      
      if not submission.compile():
        #TODO - send back the feedback(compile failed)
        return #TODO archive this submission instead of ending this procces
      
      result = submission.run() #TODO use the result for something
      
      #TODO - updates results?   maybe in another thread/queue or program
      #TODO - send back results? maybe in another thread/queue or program
      
      #signals to queue job is done
      self.queue.task_done()
