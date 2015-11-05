import queue
import threading
import mysql.connector

class ThreadGrader(threading.Thread):
  """Threaded Url Grab"""
  def __init__(self, q, sql, table='grades'):
    threading.Thread.__init__(self)
    self.queue = q
    self.conn  = sql
    self.cursor = conn.cursor()

  def run(self):
    while True:
      #grabs job from queue
      file_name  = self.queue.get()
      basename   = re.search('/(.{8})\\.zip$', file_name).group(1)
      submission = Grader(file_name)

      '''
      Values for result:
       -1: not graded
        0: good(complete)
        1: compile error
        2: no main class found
        3: run time error
        4: ran for too long
        5: outputs do not match
        other: error
      '''

      if submission.extract_info():
        if submission.compile():
          result = submission.run()
        else
          result = 1 #could not compile
      else:
        result = 2 #main not found

      #updates results into 'graded' column of /table/
      cursor.execute('UPDATE %s SET graded=%d WHERE name=%s', (self.table, result, basename))

      #signals to queue job is done
      self.queue.task_done()
