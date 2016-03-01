import re
import time
import queue
from Getch import _Getch
import datetime
import mysql.connector
from multiprocessing import Process
from Grader import Grader
from ThreadGrader import ThreadGrader
from SubmissionWatcher import SubmissionWatcher
from watchdog.observers import Observer
import threading

class Prompt(threading.Thread):
  def __init__(self, end):
    threading.Thread.__init__(self)
    self.end     = end
    self.command = ''
    #print(str(self.end))
  
  def run(self):
    while True:
      self.command += _Getch().impl()
      if ord(self.command[-1]) == 127:
        if len(self.command) > 1:
          self.command = self.command[:-2]
        else:
          self.command = self.command[:-1]
      elif ord(self.command[-1]) == 12:
        print('\n'*50)
        self.command = self.command[:-1]
      elif ord(self.command[-1]) == 133:
        print()
        if self.command[0] == 'h':
          print('self.commands:')
          print('  h                     - this message')
          print('  q                     - stop watching(grading alreading submitted works will continue')
          print('  {+,-} <num>{h,m,s}... - add or subract time from duartion')
        elif self.command[0] in '+-':
          try:
            h = float(re.search('([\\d\\.]+)h', self.command).group(1))
          except:
            h = 0
          try:
            m = float(re.search('([\\d\\.]+)m', self.command).group(1))
          except:
            m = 0
          try:
            s = float(re.search('([\\d\\.]+)s', self.command).group(1))
          except:
            s = 0
          delta = datetime.timedelta(hours=h, seconds=m, minutes=s)
          if self.command[0] == '-':
            self.end -= delta
          else:
            self.end += delta
        elif self.command[0] == 'q':
          self.end = datetime.datetime.now()
          return
        self.command = ''

def main(args):
  #create a queue
  q = queue.Queue()

  #connect to mysql server
  try:
    conf = {
      'user'    : args['username'],
      'password': args['password'],
      'host'    : args['host'],
      'database': args['database']
    }

    cnx = mysql.connector.connect(conf)
  except Error as e:
    print(e)
  finally:
    #close connection no matter what
    cnx.close()

  #file watcher
  observer = Observer()
  observer.schedule(SubmissionWatcher(), path=args['submission'])
  print(args['submission'])
  observer.start()

  #grader manager
  grade_manager = ThreadGrader(q, cnx,
                               args['table'],
                               args['problems'])
  grade_manager.setDaemon(True) #do not exit until all things needed
  grade_manager.start()         #  to be graded are graded, and start it

  #wait until end of compitition
  p = Prompt(args['end_time'])
  p.start()
  while datetime.datetime.now() < p.end:
    sec = (p.end - datetime.datetime.now()).seconds
    h   = int(sec / 3600)
    m   = int(sec / 60) % 60
    s   = int(sec % 60)
    print('\r{:02}:{:02}:{:02} > {}'.format(h, m, s, p.command), end='')
    time.sleep(0.1)

  #end watchdog
  observer.stop()
  observer.join()
