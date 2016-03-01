import re
import time
import queue
import datetime
import mysql.connector
from multiprocessing import Process
from Gui import App
from Grader import Grader
from ThreadGrader import ThreadGrader
from SubmissionWatcher import SubmissionWatcher
from watchdog.observers import Observer
import threading

def main(args):
  #create a queue
  q = queue.Queue()
  done = []

  #connect to mysql server
  try:
    conf = {
      'user'    : args['username'],
      'password': args['password'],
      'host'    : args['host'],
      'database': args['database']
    }
    print(conf)
    cnx = mysql.connector.connect(**conf)
  except mysql.connector.Error as e:
    print(e)

  #file watcher
  observer = Observer()
  observer.schedule(SubmissionWatcher(cnx, args['table']), path=args['submission'])
  observer.start()

  #grader manager
  grade_manager = ThreadGrader(q, cnx, done,
                               args['table'],
                               args['problems'])
  grade_manager.setDaemon(True) #do not exit until all things needed
  grade_manager.start()         #  to be graded are graded, and start it

  #TODO - istatiate/start GUI
  app = App(observer, q, done, args['end_time'])
  app.mainloop()

  #close mysql
  cnx.close()

  #end watchdog
  observer.stop()
  observer.join()
